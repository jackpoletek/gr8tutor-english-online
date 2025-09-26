from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import render, redirect, authenticate, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import Message, Tutor, Student, StudentTutorRelationship, User, UserProfile

# Create your views here.
def index(request):
    return render(request, '/index.html')

def about(request):
    return render(request, 'gr8tutor/about.html')

def contact(request):
    return render(request, 'gr8tutor/contact.html')

def login(request):
    return render(request, 'gr8tutor/login.html')

def register(request):
    return render(request, 'gr8tutor/register.html')


# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check required fields
        if not username or not password:
            return render(request, "gr8tutor/login.html",
                          {"error": "Please enter your username and password."})
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # If role not set, redirect
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if not user_profile.role:
                return redirect("choose_role")

            return redirect("dashboard")
        else:
            return render(request, "gr8tutor/login.html",
                          {"error": "Invalid username or password."})

    return render(request, "gr8tutor/login.html")

# Logout view
def logout_view(request):
    if request.is_authenticated:
        logout(request)
    return redirect("index")

# Registration view
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        role = request.POST.get("role")
        password = request.POST.get("password")
        password_again = request.POST.get("password_again")

        # Check passwords
        if password != password_again:
            return render(request, "gr8tutor/register.html",
                          {"error": "Passwords do not match."})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "gr8tutor/register.html",
                          {"error": "Username already taken."})
        
        # Create user
        user = User.objects.create_user(username=username, password=password)

        # Create user profile with chosen role
        UserProfile.objects.create(user=user, role=role)

        # Redirect to login
        return redirect("login")

    return render(request, "gr8tutor/register.html")

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
    # Only tutors can have access
    if request.user.userprofile.role != "tutor":
        return HttpResponseForbidden("Only tutors can confirm students.")
    
    try:
        tutor = request.userprofile.tutor
    except Tutor.DoesNotExist:
        return HttpResponseForbidden("You must be registered as a tutor.")
    
    # Defensive check: making sure the id from the URL is valid
    student = get_object_or_404(Student, id=student_id)

    # Relationship must exist
    relationship, created = StudentTutorRelationship.objects.get_or_create(
        tutor=tutor, student=student
    )
    relationship.is_active = True
    relationship.save()

    return redirect("tutor_students")

# Student sending request to Tutor
@login_required
def request_tutor(request, tutor_id):
    if request.user.userprofile.role != "student":
        return HttpResponseForbidden("Only students can request tutors.")
    
    # Tutor must exist
    tutor = get_object_or_404(Tutor, id=tutor_id)

    student = request.user.userprofile.student

    # Don't allow duplilcate requests
    relationship, created = StudentTutorRelationship.objects.get_or_create(
        student=student, tutor=tutor
    )

    if not created:
        messages.info(request, "You have already requested this tutor.")
    else:
        messages.success(request, "Tutor request sent successfully.")
    
    return redirect("dashboard")

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
        return redirect("login")
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
        return HttpResponseForbidden("You cannot chat with yourself.")

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
        or current_user.is_staff  # Admin can chat with anyone
    )
    if not allowed:
        return HttpResponseForbidden(
            "Sorry, you aren't allowed to chat with this user."
            )

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
        request, "gr8tutor/chat.html",
        {"messages": messages, "other_user": other_user}
        )

@login_required
def choose_role(request):
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user
        )

    # Skip if user has a role
    if user_profile.role in ["tutor", "student"]:
        return redirect("dashboard")

    if request.method == "POST":
        role = request.POST.get("role")
        if role in ["tutor", "student"]:
            user_profile.role = role
            user_profile.save()
            return redirect("dashboard")
        else:
            messages.error(request,
                           "Invalid role. Please choose tutor or student.")

    return render(request, "gr8tutor/choose_role.html")