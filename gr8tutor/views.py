from django.shortcuts import render
from django.http import HttpResponse

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

