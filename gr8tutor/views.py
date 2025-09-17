from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

# Create your views here.
def home(request):
    return render(request, 'gr8tutor/home.html')

def about(request):
    return render(request, 'gr8tutor/about.html')

def tutors(request):
    return render(request, 'gr8tutor/tutors.html')

def contact(request):
    return render(request, 'gr8tutor/contact.html')

def login(request):
    return render(request, 'gr8tutor/login.html')

def register(request):
    return render(request, 'gr8tutor/register.html')
    

def index(request):
    if request.method == "POST":
        return HttpResponse("You must have POSTed something")
    else:
        return HttpResponse(request.method)

