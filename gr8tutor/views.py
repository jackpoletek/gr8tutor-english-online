from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, Tutor, Student, StudentTutorRelationship

# Create your views here.
def home(request):
    return render(request, 'gr8tutor/home.html')

def about(request):
    return render(request, 'gr8tutor/about.html')

@login_required
def tutors(request):
    return render(request, 'gr8tutor/tutors.html')

def contact(request):
    return render(request, 'gr8tutor/contact.html')

def login(request):
    return render(request, 'gr8tutor/login.html')

def register(request):
    return render(request, 'gr8tutor/register.html')


# Tutor managing a student list
# List of students
@login_required
def tutor_students(request):
    try:
        tutor = request.user.userprofile.tutor
    except StudentTutorRelationship.DoesNotExist:
        return HttpResponse("You must be registered as a tutor.")
    
    pending = StudentTutorRelationship.objects.filter(tutor=tutor,
                                                      is_active=False)
    active = StudentTutorRelationship.objects.filter(tutor=tutor,
                                                     is_active=True)
    return render(request, "gr8tutor/tutor_students.html",
                  {"pending": pending,
                   "active": active})

# Confirm a student request
@login_required
def confirm_student(request, student_id):
    try:
        tutor = request.user.userprofile.tutor
    except Tutor.DoesNotExist:
        return HttpResponseForbidden("You must be registered as a tutor.")
    
    relationship = get_object_or_404(
        StudentTutorRelationship, tutor=tutor, student_id=student_id
    )
    relationship.is_active = True
    relationship.save()
    return redirect("tutor_students")

# Delete a student
@login_required
def delete_student(request, student_id):
    try:
        tutor = request.user.userprofile.tutor
    except Tutor.DoesNotExist:
        return HttpResponse("You must be registered as a tutor.")
    
    relationship = get_object_or_404(StudentTutorRelationship,
                                     tutor=tutor, student__id=student_id,)
    relationship.delete()
    return redirect("tutor_students")

# Permission to delete account
@login_required
def delete_profile(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

# Only the user or admin can delete the account
    if request.user != user_to_delete and request.user.userprofile.role != 'admin':
        raise PermissionDenied("You cannot delete this profile.")
    elif request.user.userprofile.role == "admin":
        user_to_delete()
        return redirect("home")
    else:
        user_to_delete.delete()
        return redirect("login")

@login_required
def admin_user_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("for admins only.")
    
    # For admins only
    users = User.objects.all()
    return render(request, "gr8tutor/admin_user_list.html", {"users": users})

# Chat view between Tutor and Student
@login_required
def chat_view(request, other_party_id):
    current_user = request.user
    other_user = get_object_or_404(User, id=other_party_id)

    # Don't allow chatting with yourself
    if current_user == other_user:
        raise PermissionDenied("You cannot chat with yourself.")

    # Ensure that the current user and other user have a relationship
    if not (
        StudentTutorRelationship.objects.get(
            tutor__user_profile__user=current_user,
            student__user_profile__user=other_user,
            is_active=True,
        ).exists()
        or
        StudentTutorRelationship.objects.get(
            tutor__user_profile__user=other_user,
            student__user_profile__user=current_user,
            is_active=True,
        ).exists()
        or current_user.userprofile.role == 'admin' # Admin can chat with anyone
    ):
        return HttpResponseForbidden("Sorry, you aren't allowed to chat with this user.")

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



