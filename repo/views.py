from unicodedata import category
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from repo.forms import FileUploadForm, FileUploadToFolderForm, RegistrationForm, FolderRenameForm, FileRenameForm
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

# Create your views here.

# DONE


def index(request):
    return render(request, "repo/index.html", {})

# DONE


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
        username = form['username'].value()
        password = form['password'].value()
        if(auth_attempt(username, password)):
            return redirect("index")
        else:
            try:
                email_attempt = User.objects.get(email=username)
                if(auth_attempt(email_attempt.username, password)):
                    return redirect("index")
            except:
                pass

        logger.warning(
            f'Failed Login Attempt: User not found (Username or Email = "{ username }")')

    return render(request, FORM_TEMPLATE, {
        "action": "Login",
        "form": form
    })

# DONE


def register_request(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            user = form.save()

            logger.info(f'User "{ user.username }" created.')
            messages.info(request, f"{user.username} is created!")

            # Give user a root folder on registration
            new_root_folder = Folder(
                owner=user,
                name="root",
                is_root=True
            )

            new_root_folder.save()
            return redirect("index")

        logger.warning(f"Invalid form submit on registration.")
        messages.error(request, "Invalid post data.")

    return render(request, FORM_TEMPLATE, {
        "action": "Register",
        "form": form
    })

# DONE


@login_required
def logout_request(request):
    logger.info(f'User "{ request.user.username }" logged out.')
    logout(request)
    return redirect('index')

# DONE


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
        "action": "Upload File"
    })

# DONE


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

    return redirect('view-folder', folder_id, 'all')

# DONE


@login_required
def view_repo(request):
    folder = Folder.objects.get(owner=request.user, is_root=True)

    return render(request, FOLDER_VIEW_TEMPLATE, {
        "action": "View Repo",
        "current": None,
        "parent": None,
        "children": [folder],
        "files": None,
        "upload_form": None
    })

# DONE


@login_required
def view_folder(request, folder_id, category="all"):
    folder = Folder.objects.get(pk=folder_id)

    if folder.owner != request.user:
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
    if category != "all":
        files = File.objects.filter(folder=folder, category=category)

    # files = File.objects.filter(folder=folder).order_by('name')[0:]

    categories = File.objects.values_list('category', flat=True)

    return render(request, FOLDER_VIEW_TEMPLATE, {
        "action": "View Repo",
        "current": folder,
        "parent": parent,
        "children": children,
        "files": files,
        "upload_form": form,
        "categories": categories,
        "category": category,
    })

# DONE


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

        return redirect('view-folder', parent_folder_id, 'all')

    logger.error(f"Unhandled error on create folder request")
    messages.error(request, "Something went wrong.")
    return redirect('view-folder', parent_folder_id, 'all')

# DONE


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

# DONE


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

        return redirect('view-folder', parent.id, 'all')
    else:
        return render(request, CONFIRMATION_TEMPLATE, {
            "action": "Confirm Folder Delete"
        })

# DONE


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
            "action": "Confirm File Delete"
        })

# DONE


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
            "form": form
        })

# DONE


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
            "form": form
        })
