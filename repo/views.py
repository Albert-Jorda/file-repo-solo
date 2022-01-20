from django.shortcuts import  render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, "repo/index.html", {})

def login_request(request):
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

        return render(request, "repo/auth_form.html", {
            "form": form
        })

    else:
        form = AuthenticationForm()
        return render(request, "repo/auth_form.html", {
            "form": form
        })

def register_request(request):
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.info(request, f"{user.username} is created!")
            return redirect("index")

        messages.error(request,"Invalid post data.")
        return render(request, "repo/auth_form.html", {
            "form": form
        })

    else:
        form = UserCreationForm()
        return render(request, "repo/auth_form.html", {
            "form": form
        })

def logout_request(request):
    logout(request)
    return redirect('index')