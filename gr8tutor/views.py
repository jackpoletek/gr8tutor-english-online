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

        # Invalid credentials
        if user is None:
            return render(
                request,
                "gr8tutor/login.html",
                {
                    "login_error": True,
                    "error_message": "This account does not exist or credentials are invalid.",
                },
            )

        # Login user
        auth_login(request, user)

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
        role = request.POST.get("role")

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

        # Password mismatch
        if password != password_again:
            return render(
                request,
                "gr8tutor/register.html",
                {
                    "registration_error": True,
                    "error_message": "Passwords do not match.",
                },
            )

        # Username exists
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

        # Create profile
        profile = UserProfile.objects.create(user=user)

        # Assign role
        if role in ("tutor", "student"):
            profile.role = role
            profile.save()

            if role == "tutor":
                Tutor.objects.get_or_create(user_profile=profile)
            else:
                Student.objects.get_or_create(user_profile=profile)

        return render(
            request,
            "gr8tutor/register.html",
            {
                "registration_success": True,
                "registration_message": f"Welcome {username}! Your account has been created.",
            },
        )

    return render(request, "gr8tutor/register.html")
