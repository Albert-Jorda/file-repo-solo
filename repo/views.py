from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from repo.forms import *
from repo.models import Folder, File, HeirData, User
from repo.helpers import determine_category
import logging

# Logger
logger = logging.getLogger(__name__)

# Template name strings
FORM_TEMPLATE = "repo/form.html"
INDEX_TEMPLATE = "repo/index.html"
FOLDER_VIEW_TEMPLATE = "repo/folder.html"
CONFIRMATION_TEMPLATE = "repo/confirmation.html"
PROFILE_VIEW_TEMPLATE = "repo/profile.html"

# Create your views here.
def index(request):
    return render(request, "repo/index.html", {"url_name": 'index'})


def login_request(request):
    form = AuthenticationForm()

    def auth_attempt(username, password):
        user = authenticate(
            username=username, password=password)
        if user is not None:
            login(request, user)

            logger.info(f'User "{ user.username }" logged in.')
            messages.info(
                request, f"You are now logged in as {user.username}.")
            return True

        return False

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        username: str = form['username'].value()
        password = form['password'].value()
        if(auth_attempt(username, password)):
            return redirect("index")
        else:
            try:
                email_attempt = User.objects.get(email=username.lower())
                if(auth_attempt(email_attempt.username, password)):
                    return redirect("index")
            except:
                pass

        logger.warning(
            f'Failed Login Attempt: User not found (Username or Email = "{ username }")')

    return render(request, FORM_TEMPLATE, {
        "action": "Login",
        "form": form,
        "url_name": 'login'
    })


def register_request(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            user: User = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            logger.info(f'User "{ user.username }" created.')
            messages.info(request, f"{user.username} is created!")
            
            return redirect("index")

        logger.warning(f"Invalid form submit on registration.")
        messages.error(request, "Invalid post data.")

    return render(request, FORM_TEMPLATE, {
        "action": "Register",
        "form": form,
        "url_name": 'register'
    })


@login_required
def logout_request(request):
    if request.method == "POST":
        if request.POST.get("confirmation") == "confirm":
            logger.info(f'User "{ request.user.username }" logged out.')
            logout(request)

        return redirect(request.GET.get("prev_url", ''))
    else:
        return render(request, CONFIRMATION_TEMPLATE, {
            "action": "Confirm Logout",
            "url_name": 'logout'
        })


@login_required
def upload_file(request):
    form = FileUploadForm(request.user)
    if request.method == "POST":
        form = FileUploadForm(request.user, request.POST, request.FILES)

        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.owner = request.user
            new_file.name = new_file.file.name
            new_file.category = determine_category(new_file.file.name)
            new_file.save()

            logger.info(
                f"{ request.user.username } uploaded { new_file.file.name }")

            messages.info(request, f"{ new_file.file.name } is uploaded!")
            return redirect('view-folder', new_file.folder.id)

        logger.warning(
            f'Error on uploading file from User "{ request.user.username }"')

    return render(request, FORM_TEMPLATE, {
        "form": form,
        "action": "Upload File",
        "url_name": 'upload-file'
    })


@login_required
def upload_file_to_folder(request, folder_id):
    if request.method == "POST":
        folder = Folder.objects.get(pk=folder_id)
        form = FileUploadToFolderForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.owner = request.user
            new_file.folder = folder
            new_file.name = new_file.file.name
            new_file.category = determine_category(new_file.file.name)
            new_file.save()

            logger.info(
                f"{ request.user.username } uploaded { new_file.file.name }")
            messages.info(request, f"{ new_file.file.name } is uploaded!")

    return redirect('view-folder', folder_id)


@login_required
def view_repo(request):
    folder = Folder.objects.get(owner=request.user, is_root=True)

    return render(request, FOLDER_VIEW_TEMPLATE, {
        "action": "View Repo",
        "current": None,
        "parent": None,
        "children": [folder],
        "files": None,
        "upload_form": None,
        "url_name": 'view-repo'
    })


@login_required
def view_folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)

    if folder.owner != request.user and not folder.is_shared:
        logger.warning(
            f'User {request.user.username} tried to view unshared folder { folder.name } without proper ownership')
        messages.warning(
            request, "Insufficient permissions to view the folder!")
        return redirect('view-repo')

    form = FileUploadToFolderForm()
    heir_data = HeirData.objects.filter(parent=folder)
    heir_data_parent = HeirData.objects.filter(folder=folder).first()

    # Parenting logic
    children = []
    for child in heir_data:
        children.append(child.folder)

    parent = heir_data_parent.parent if heir_data_parent else None

    files = File.objects.filter(folder=folder)

    category = request.GET.get('category', '')
    orderBy = request.GET.get('order_by', '')
    sequence = request.GET.get('sequence', '')
    search = request.GET.get('search', '')

    if category:
        files = File.objects.filter(folder=folder, category=category)

    if orderBy:
        files = File.objects.filter(folder=folder).order_by(orderBy)

    if search:
        files = File.objects.filter(folder=folder, name__icontains=search)

    if sequence:
        files = File.objects.filter(folder=folder).order_by(
            'uploaded_at' if sequence == 'increasing' else '-uploaded_at')
        if category:
            files = File.objects.filter(
                folder=folder, category=category).order_by('category' if sequence == 'increasing' else '-category')
        if orderBy:
            files = File.objects.filter(folder=folder).order_by(
                orderBy if sequence == 'increasing' else f'-{orderBy}')
        if search:
            files = File.objects.filter(folder=folder, name__icontains=search).order_by(
                'name' if sequence == 'increasing' else '-name')

    categories = sorted(
        list(set(File.objects.values_list('category', flat=True))))
    filesList = File.objects.filter(folder=folder)

    return render(request, FOLDER_VIEW_TEMPLATE, {
        "action": "View Repo",
        "current": folder,
        "parent": parent,
        "children": children,
        "files": files,
        "upload_form": form,
        "categories": categories,
        "order_by": ['name', 'category', 'uploaded_at'],
        "sequences": ['increasing', 'decreasing'],
        "filesList": filesList,
        "url_name": 'repo/view/folder/' + str(folder_id)
    })


@ login_required
def create_folder(request, parent_folder_id):
    if request.method == "POST":
        parent = Folder.objects.get(pk=parent_folder_id)
        folder_name = request.POST.get("folder-name")

        new_folder = Folder(
            owner=request.user,
            name=folder_name,
        )

        new_heir_data = HeirData(folder=new_folder, parent=parent)

        new_folder.save()
        new_heir_data.save()

        logger.info(
            f'User "{ request.user.username }" created folder  "{ folder_name }"')
        messages.info(request, f"{ folder_name } is created!")

        return redirect('view-folder', parent_folder_id)

    logger.error(f"Unhandled error on create folder request")
    messages.error(request, "Something went wrong.")
    return redirect('view-folder', parent_folder_id)


@ login_required
def view_file(request, file_id):
    file = File.objects.get(pk=file_id)

    if file.owner != request.user and not file.folder.is_shared:
        logger.warning(
            f'User {request.user.username} tried to view unshared file { file.name } without proper ownership')
        messages.warning(request, "Insufficient permissions to view the file!")
        return redirect('view-repo')

    filename = file.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


@ login_required
def delete_folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    heir_data = HeirData.objects.filter(folder=folder).first()
    parent = heir_data.parent

    if folder.owner != request.user:
        logger.warning(
            f'User {request.user.username} tried to delete folder { folder.name } without proper ownership')
        messages.warning(
            request, "Insufficient permissions to delete the folder!")
        return redirect('view-repo')

    if request.method == "POST":
        if request.POST.get("confirmation") == "confirm":
            logger.info(
                f'User {request.user.username} deleted folder { folder.name }')
            messages.info(request, f"Folder { folder.name } deleted!")
            folder.delete()

        return redirect('view-folder', parent.id)
    else:
        return render(request, CONFIRMATION_TEMPLATE, {
            "action": "Confirm Folder Delete",
            "url_name": 'delete-folder'
        })


@ login_required
def delete_file(request, file_id):
    file = File.objects.get(pk=file_id)
    folder = file.folder

    if file.owner != request.user:
        logger.warning(
            f'User {request.user.username} tried to delete file { file.name } without proper ownership')
        messages.warning(
            request, "Insufficient permissions to delete the file!")

        return redirect('view-repo')

    if request.method == "POST":
        if request.POST.get("confirmation") == "confirm":
            logger.info(
                f'User {request.user.username} deleted file { file.name }')
            messages.info(request, f"File { file.name } deleted!")
            file.delete()

        return redirect('view-folder', folder.id)
    else:
        return render(request, CONFIRMATION_TEMPLATE, {
            "action": "Confirm File Delete",
            "url_name": 'delete-file'
        })


@ login_required
def rename_folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    heir_data = HeirData.objects.filter(folder=folder).first()
    parent = heir_data.parent
    prev_name = folder.name

    if folder.owner != request.user:
        logger.warning(
            f'User {request.user.username} tried to rename folder { folder.name } without proper ownership')
        messages.warning(
            request, "Insufficient permissions to rename the folder!")
        return redirect('view-repo')

    if folder.is_root:
        logger.warning(
            f'User {request.user.username} tried to rename a root folder')
        messages.warning(request, "You cannot rename the root folder!")
        return redirect('view-repo')

    if request.method == "POST":
        form = FolderRenameForm(request.POST, instance=folder)
        if form.is_valid():
            folder = form.save()

            logger.info(
                f'User {request.user.username} renamed folder { prev_name } to { folder.name }')
            messages.info(
                request, f"Folder { prev_name } renamed to { folder.name }!")

        return redirect('view-folder', parent.id)

    else:
        form = FolderRenameForm(instance=folder)
        return render(request, FORM_TEMPLATE, {
            "action": "Rename Folder",
            "form": form,
            "url_name": 'rename-folder'
        })


@ login_required
def rename_file(request, file_id):
    file = File.objects.get(pk=file_id)
    folder = file.folder
    prev_name = file.name

    if file.owner != request.user:
        logger.warning(
            f'User {request.user.username} tried to rename file { file.name } without proper ownership')
        messages.warning(
            request, "Insufficient permissions to rename the file!")

        return redirect('view-repo')

    if request.method == "POST":
        form = FileRenameForm(request.POST, instance=file)
        if form.is_valid():
            file = form.save()

            logger.info(
                f'User {request.user.username} renamed folder { prev_name } to { file.name }')
            messages.info(
                request, f"Folder { prev_name } renamed to { folder.name }!")

        return redirect('view-folder', folder.id)

    else:
        form = FileRenameForm(instance=file)
        return render(request, FORM_TEMPLATE, {
            "action": "Rename File",
            "form": form,
            "url_name": 'rename-file'
        })


@login_required
def view_profile(request):
    return render(request, PROFILE_VIEW_TEMPLATE, {"url_name": 'view-profile'})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change-password')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = form = PasswordChangeForm(request.user)
    return render(request, FORM_TEMPLATE, {'action': 'Change Password', 'form': form, "url_name": 'change-password'})


@login_required
def change_username(request):
    user = request.user
    if request.method == "POST":
        form = ChangeUsernameForm(request.POST)
        if form.is_valid():
            if User.objects.exclude(pk=user.id).filter(username=form.cleaned_data['new_username']).exists():
                messages.warning(request, 'Username already exists!')
            else:
                if user.check_password(form.cleaned_data['password']):
                    user.username = form.cleaned_data['new_username']
                    user.save()
                    messages.success(request, 'Success!')
                else:
                    messages.warning(request, 'Password is incorrect!')
    else:
        form = ChangeUsernameForm()

    return render(request, FORM_TEMPLATE, {'action': 'Change Username', 'form': form, "url_name": 'change-username'})


@ login_required
def change_email(request):
    user = request.user
    if request.method == "POST":
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            if User.objects.exclude(pk=user.id).filter(email=form.cleaned_data['new_email']).exists():
                messages.warning(request, 'Email already exists!')
            else:
                if user.check_password(form.cleaned_data['password']):
                    user.email = form.cleaned_data['new_email']
                    user.save()
                    messages.success(request, 'Success!')
                else:
                    messages.warning(request, 'Password is incorrect!')
    else:
        form = ChangeEmailForm()

    return render(request, FORM_TEMPLATE, {'action': 'Change Email', 'form': form, "url_name": 'change-email'})


@login_required
def change_profile_picture(request):
    user = request.user
    if request.method == "POST":
        form = ChangeImageForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture changed successfully!')
        else:
            messages.warning(request, 'Unsuccessful!')
    else:
        form = ChangeImageForm()

    return render(request, FORM_TEMPLATE, {'action': 'Change Profile Picture', 'form': form, "url_name": 'change-profile-picture'})
