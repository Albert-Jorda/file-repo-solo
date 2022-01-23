from django.shortcuts import  render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FileUploadForm
from .models import Folder, File, HeirData

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
    action = "Login"
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
            "action": action,
            "form": form
        })

    else:
        form = AuthenticationForm()
        return render(request, FORM_TEMPLATE, {
            "action": action,
            "form": form
        })


# DONE
def register_request(request):
    action = "Register"
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
            "action": action,
            "form": form
        })

    else:
        form = UserCreationForm()
        return render(request, FORM_TEMPLATE, {
            "action": action,
            "form": form
        })


# DONE
def logout_request(request):
    logout(request)
    return redirect('index')


# ???
def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(data=request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner(request.user)


# ???
def view_root_folder(request):
    root = Folder.objects.get(owner=request.user, is_root=True)
    heir_data = HeirData.objects.filter(parent=root)

    # Parenting logic
    children = []
    for child in heir_data:
        children.append(child.folder)

    files = File.objects.filter(folder=root)

    return render(request, FOLDER_VIEW_TEMPLATE, {
        "action": "View Repo",
        "root": root,
        "children": children,
        "files": files
    })


def view_folder(request):
    # TODO
    pass


def view_file(request):
    # TODO
    pass


def download_file(request):
    # TODO
    pass


