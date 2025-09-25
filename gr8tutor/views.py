from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, Tutor, Student, StudentTutorRelationship

# Create your views here.
def index(request):
    return render(request, 'gr8tutor/index.html')

def about(request):
    return render(request, 'gr8tutor/about.html')

def contact(request):
    return render(request, 'gr8tutor/contact.html')

# Authentication views are handled by allauth


# Tutor managing a student list
# List of students
@login_required
def tutor_students(request):
    try:
        tutor = request.user.userprofile.tutor
    except Tutor.DoesNotExist:
        return HttpResponseForbidden("You must be registered as a tutor.")
    
    pending = StudentTutorRelationship.objects.filter(
        tutor=tutor, is_active=False
        )
    active = StudentTutorRelationship.objects.filter(
        tutor=tutor, is_active=True
        )
    
    return render(
        request, "gr8tutor/tutor_students.html",
        {"pending": pending, "active": active}
                  )

@login_required
def tutors(request):
    tutors = Tutor.objects.all()
    return render(
        request, "gr8tutor/tutors.html", {"tutors": tutors}
        )

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
        return HttpResponseForbidden("You must be registered as a tutor.")
    
    relationship = get_object_or_404(
        StudentTutorRelationship, tutor=tutor, student__id=student_id
        )
    relationship.delete()
    return redirect("tutor_students")

# Student sending request to Tutor
@login_required
def request_tutor(request, tutor_id):
    try:
        student = request.user.userprofile.student
    except Student.DoesNotExist:
        return HttpResponseForbidden("You must be registered as a student.")
    
    tutor = get_object_or_404(Tutor, id=tutor_id)
    
    relationship, created = StudentTutorRelationship.objects.get_or_create(
        student=student, tutor=tutor, defaults={'is_active': False}
    )

    message = "Request sent to tutor."

    return HttpResponse(message)

# Permission to delete account
@login_required
def delete_profile(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

# Only the user or admin can delete the account
    if request.user != user_to_delete and not request.user.is_staff:
        raise PermissionDenied("You cannot delete this profile.")
    
    user_to_delete.delete()
    
    if request.user == user_to_delete:  # User deleting themselves
        logout(request)
        return redirect("account_login") # allauth login page
    else:
        return redirect("index")

@login_required
def admin_user_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("For admins only.")
    
    # For admins only
    users = User.objects.all()
    return render(
        request, "gr8tutor/admin_user_list.html", {"users": users}
        )

# Chat view between Tutor and Student
@login_required
def chat_view(request, other_party_id):
    current_user = request.user
    other_user = get_object_or_404(User, id=other_party_id)

    # Don't allow chatting with yourself
    if current_user == other_user:
        raise PermissionDenied("You cannot chat with yourself.")

    # Ensure that the current user and other user have a relationship
    allowed = (
        StudentTutorRelationship.objects.filter(
            tutor__user_profile__user=current_user,
            student__user_profile__user=other_user,
            is_active=True,
        ).exists()
        or
        StudentTutorRelationship.objects.filter(
            tutor__user_profile__user=other_user,
            student__user_profile__user=current_user,
            is_active=True,
        ).exists()
        or current_user.is_staff # Admin can chat with anyone
    )
    if not allowed:
        return HttpResponseForbidden("Sorry, you aren't allowed to chat with this user.")

    sent_messages = Message.objects.filter(
        sender=current_user, recipient=other_user
        )
    received_messages = Message.objects.filter(
        sender=other_user, recipient=current_user
        )
    messages = sent_messages.union(received_messages).order_by("time")

    if request.method == "POST":
        text = request.POST.get("message")
        if text:
            Message.objects.create(
                sender=current_user, recipient=other_user, text=text
                )
            return redirect(
                "chat", other_party_id=other_user.id
                )

    return render(
        request, "gr8tutor/chat.html", {"messages": messages, "other_user": other_user}
        )

def logout_view(request):
    logout(request)
    return render(request, 'gr8tutor/logout.html')
