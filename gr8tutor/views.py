from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, Tutor, Student, StudentTutorRelationship

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
    
@login_required
def chat_view(request, other_party_id):
    current_user = request.user
    other_user = User.objects.get(id=other_party_id)

    sent_messages = Message.objects.filter(sender=current_user,
                                           recipient=other_user)
    received_messages = Message.objects.filter(sender=other_user,
                                               recipient=current_user)
    messages = sent_messages.union(received_messages).order_by("time")

    if request.method == "POST":
        text = request.POST.get("message")
        if text:
            Message.objects.create(sender=current_user, recipient=other_user,
                                   text=text)
            return redirect("chat", other_party_id=other_user.id)

    return render(request, "gr8tutor/chat.html", {"messages": messages,
                                                  "other_user": other_user})



