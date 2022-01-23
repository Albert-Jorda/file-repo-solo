import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import  render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from django.contrib import messages
from repo.forms import FileUploadForm
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
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            messages.info(request, f"{user.username} is created!")

            # Give user a root folder on registration
            new_root_folder = Folder(
                owner=request.user, 
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
def logout_request(request):
    logout(request)
    return redirect('index')

# ???
def upload_file(request):
    form = FileUploadForm(request.user)
    if request.method == "POST":
        form = FileUploadForm(request.user, request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.owner(request.user)
            return redirect('folder-view', file.folder)

    return render(request, FORM_TEMPLATE, {
        "form": form,
        "action": "Upload File"
    })

# ???
def view_repo(request):
    folder = Folder.objects.get(owner=request.user, is_root=True)

    return render(request, FOLDER_VIEW_TEMPLATE, {
        "action": "View Repo",
        "parent": None,
        "children": [folder],
        "files": None
    })

# ???
def view_folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    heir_data = HeirData.objects.filter(parent=folder)
    parent = HeirData.objects.get(folder=folder)

    # Parenting logic
    children = []
    for child in heir_data:
        children.append(child.folder)

    files = File.objects.filter(folder=folder)

    return render(request, FOLDER_VIEW_TEMPLATE, {
        "action": "View Repo",
        "parent": parent,
        "children": children,
        "files": files
    })

# ????????????????????????
def download_file(request, file_id):
    file = File.objects.get(id=file_id)
    response = HttpResponse(content_type='application/force-download')

    response['Content-Disposition'] = f'attachment; filename={smart_str(file.file.name)}'
    response['X-Sendfile'] = smart_str(file.file.url)

    return response

def create_folder(request):
    # TODO
    pass

def view_file(request, file_id):
    # TODO
    pass

