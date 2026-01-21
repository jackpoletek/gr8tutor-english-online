from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from .models import (
    Message,
    Tutor,
    Student,
    StudentTutorRelationship,
    User,
    UserProfile)


# Helper functions
def user_is_tutor(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "tutor"


def user_is_student(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "student"


def get_tutor_or_forbidden(user):
    if not user_is_tutor(user):
        return None, HttpResponseForbidden("You must be a tutor to access this page.")
    try:
        return user.userprofile.tutor, None
    except (AttributeError, Tutor.DoesNotExist):
        return None, HttpResponseForbidden("You must be registered as a tutor.")


def get_student_or_forbidden(user):
    if not user_is_student(user):
        return None, HttpResponseForbidden("You must be a student to access this page.")
    try:
        return user.userprofile.student, None
    except (AttributeError, Student.DoesNotExist):
        return None, HttpResponseForbidden("You must be registered as a student.")


# Basic views
def index(request):
    return render(request, "gr8tutor/index.html")


def about(request):
    return render(request, "gr8tutor/about.html")


def contact(request):
    return render(request, "gr8tutor/contact.html")


# Dashboard view
@login_required
def dashboard(request):
    return render(request, "gr8tutor/dashboard.html")


# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check required fields
        if not username or not password:
            return render(
                request,
                "gr8tutor/login.html",
                {"login_error": True, "error_message": "Both fields are required."},
            )

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        # Handle invalid login
        if user is None:
            return render(
                request,
                "gr8tutor/login.html",
                {
                    "login_error": True,
                    "error_message": "This account does not exist or credentials are invalid.",
                },
            )

        auth_login(request, user)

        # Ensure profile exists
        user_profile, _ = UserProfile.objects.get_or_create(user=user)

        # Redirect if role not set
        if not user_profile.role:
            return redirect("choose_role")

        return redirect("dashboard")

    return render(request, "gr8tutor/login.html")


# Logout view
def logout_view(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("index")


# Registration view
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_again = request.POST.get("password_again")
        role = request.POST.get("role") or request.GET.get("role")

        # Check required fields
        if not username or not password or not password_again:
            return render(
                request,
                "gr8tutor/register.html",
                {
                    "registration_error": True,
                    "error_message": "All fields are required.",
                },
            )

        # Check passwords
        if password != password_again:
            return render(
                request,
                "gr8tutor/register.html",
                {
                    "registration_error": True,
                    "error_message": "Passwords do not match.",
                },
            )

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "gr8tutor/register.html",
                {
                    "registration_error": True,
                    "error_message": "Username already taken.",
                },
            )

        # Create user
        user = User.objects.create_user(username=username, password=password)

        # Create user profile
        profile = UserProfile.objects.create(user=user)

        # Assign role if valid
        if role in ("tutor", "student"):
            profile.role = role
            profile.save()
            if role == "tutor":
                Tutor.objects.get_or_create(user_profile=profile)
            elif role == "student":
                Student.objects.get_or_create(user_profile=profile)

        return render(
            request,
            "gr8tutor/register.html",
            {"registration_success": True, "username": username, "role": role},
        )

    return render(request, "gr8tutor/register.html")


# Tutor managing a student list
@login_required
def tutor_students(request):
    tutor, error_response = get_tutor_or_forbidden(request.user)
    if error_response:
        return error_response

    pending_students = StudentTutorRelationship.objects.filter(
        tutor=tutor, is_active=False
    )
    active_students = StudentTutorRelationship.objects.filter(
        tutor=tutor, is_active=True
    )

    return render(
        request,
        "gr8tutor/tutor_students.html",
        {"pending_students": pending_students, "active_students": active_students},
    )


@login_required
def tutors(request):
    tutors = Tutor.objects.all()
    return render(request, "gr8tutor/tutors.html", {"tutors": tutors})


# Confirm a student request
@login_required
def confirm_student(request, student_id):
    tutor, error_response = get_tutor_or_forbidden(request.user)
    if error_response:
        return error_response

    student = get_object_or_404(Student, id=student_id)
    if student.user_profile.role != "student":
        raise Http404("The user is not a student.")

    relationship, _ = StudentTutorRelationship.objects.get_or_create(
        tutor=tutor, student=student
    )
    relationship.is_active = True
    relationship.save()

    messages.success(request, "Student confirmed.")
    return redirect("tutor_students")


# Student sending request to Tutor
@login_required
def request_tutor(request, tutor_id):
    student, error_response = get_student_or_forbidden(request.user)
    if error_response:
        return error_response

    tutor = get_object_or_404(Tutor, id=tutor_id)

    relationship, created = StudentTutorRelationship.objects.get_or_create(
        student=student, tutor=tutor
    )

    if not created:
        messages.info(request, "You have already requested this tutor.")
    else:
        messages.success(request, "Tutor request sent successfully.")

    return redirect("tutors")


# Permission to delete account
@login_required
def delete_profile(request, user_id):
    if request.method != "POST":
        raise Http404()

    user_to_delete = get_object_or_404(User, id=user_id)

    if request.user != user_to_delete and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this profile.")

    user_to_delete.delete()

    if request.user == user_to_delete:
        auth_logout(request)
        return redirect("login")

    return redirect("admin_user_list")


@login_required
def admin_user_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("For admins only.")

    users = User.objects.all()
    return render(request, "gr8tutor/admin_user_list.html", {"users": users})


# Chat view between Tutor and Student
@login_required
def chat_view(request, other_party_id):
    current_user = request.user
    other_user = get_object_or_404(User, id=other_party_id)

    if current_user == other_user:
        return HttpResponseForbidden("Chatting isn't allowed.")

    allowed = (
        StudentTutorRelationship.objects.filter(
            tutor__user_profile__user=current_user,
            student__user_profile__user=other_user,
            is_active=True,
        ).exists()
        or StudentTutorRelationship.objects.filter(
            tutor__user_profile__user=other_user,
            student__user_profile__user=current_user,
            is_active=True,
        ).exists()
        or current_user.is_staff
    )

    if not allowed:
        return HttpResponseForbidden("You are not allowed to chat with this user.")

    sent_messages = Message.objects.filter(sender=current_user, recipient=other_user)
    received_messages = Message.objects.filter(
        sender=other_user, recipient=current_user
    )
    chat_messages = sent_messages.union(received_messages).order_by("id")

    if request.method == "POST":
        text = request.POST.get("message", "").strip()

        if not text:
            messages.error(request, "Message cannot be empty.")
            return redirect("chat", other_party_id=other_user.id)

        Message.objects.create(sender=current_user, recipient=other_user, text=text)

        return redirect("chat", other_party_id=other_user.id)

    return render(
        request,
        "gr8tutor/chat.html",
        {"messages": chat_messages, "other_user": other_user},
    )


# Choose role view
@login_required
def choose_role(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if profile.role in ["tutor", "student"]:
        return redirect("dashboard")

    if request.method == "POST":
        role = request.POST.get("role")

        if role in ["tutor", "student"]:
            profile.role = role
            profile.save()

            if role == "tutor":
                Tutor.objects.get_or_create(user_profile=profile)
            else:
                Student.objects.get_or_create(user_profile=profile)

            return redirect("dashboard")

        messages.error(request, "Invalid role.")

    return render(request, "gr8tutor/choose_role.html")


# Tutor deleting a student
@login_required
def delete_student(request, student_id):
    if request.method != "POST":
        raise Http404()

    tutor, error_response = get_tutor_or_forbidden(request.user)
    if error_response:
        return error_response

    relationship = StudentTutorRelationship.objects.filter(
        tutor=tutor, student__id=student_id
    ).first()

    if not relationship:
        raise Http404("This student is not associated with you.")

    relationship.delete()
    messages.success(request, "Student removed successfully.")
    return redirect("tutor_students")
