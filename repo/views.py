from django.shortcuts import  render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from repo.forms import FileUploadForm, FileUploadToFolderForm, RegistrationForm
from repo.models import Folder, File, HeirData

# Template name strings
FORM_TEMPLATE = "repo/form.html"
INDEX_TEMPLATE = "repo/index.html"
FOLDER_VIEW_TEMPLATE = "repo/folder.html"
FILE_VIEW_TEMPLATE = "repo/file.html"

# Create your views here.

# DONE
def index(request):
    return render(request, "repo/index.html", {})

# DONE
def login_request(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request,"User not found.")

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
            messages.info(request, f"{user.username} is created!")

            # Give user a root folder on registration
            new_root_folder = Folder(
                owner=user, 
                name="root",
                is_root=True
            )
            new_root_folder.save()
            return redirect("index")

        messages.error(request,"Invalid post data.")

    return render(request, FORM_TEMPLATE, {
        "action": "Register",
        "form": form
    })

# DONE
@login_required
def logout_request(request):
    logout(request)
    return redirect('index')

# DONE (Could be better)
@login_required
def upload_file(request):
    form = FileUploadForm(request.user)
    if request.method == "POST":
        form = FileUploadForm(request.user, request.POST, request.FILES)

        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.owner = request.user
            new_file.save()

            messages.info(request, f"{ new_file.file.name } is uploaded!")
            return redirect('view-folder', new_file.folder.id)

    return render(request, FORM_TEMPLATE, {
        "form": form,
        "action": "Upload File"
    })

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
def view_folder(request, folder_id):
    form = FileUploadToFolderForm()
    folder = Folder.objects.get(pk=folder_id)
    heir_data = HeirData.objects.filter(parent=folder)
    heir_data_parent = HeirData.objects.filter(folder=folder).first()

    # Parenting logic
    children = []
    for child in heir_data:
        children.append(child.folder)

    parent = heir_data_parent.parent if heir_data_parent else None
    
    files = File.objects.filter(folder=folder)

    return render(request, FOLDER_VIEW_TEMPLATE, {
        "action": "View Repo",
        "current": folder,
        "parent": parent,
        "children": children,
        "files": files,
        "upload_form": form
    })

# DONE
@login_required
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
        messages.info(request, f"{ folder_name } is created!")

        return redirect('view-folder', parent_folder_id)

    messages.error(request, "Something went wrong.")
    return redirect('view-folder', parent_folder_id)

# ???
@login_required
def upload_file_to_folder(request, folder_id):
    if request.method == "POST":
        folder = Folder.objects.get(pk=folder_id)
        form = FileUploadToFolderForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.owner = request.user
            new_file.folder = folder
            new_file.save()
            messages.info(request, f"{ new_file.file.name } is uploaded!")

    return redirect('view-folder', folder_id)

# I DON'T WANT TO DO THIS
@login_required
def view_file(request, file_id):
    # TODO
    pass
