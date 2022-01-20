from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    # TODO
    pass

def login(request):
    if request.method == "POST":
        # TODO
        pass
    else:
        # TODO
        pass

def register(request):
    if request.method == "POST":
        # TODO
        pass
    else:
        # TODO
        pass

def logout(request):
    # TODO
    pass