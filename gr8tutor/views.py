from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponseForbidden, Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import Message, Tutor, Student, StudentTutorRelationship, User, UserProfile

# Create your views here.
def index(request):
    return render(request, 'gr8tutor/index.html')

def about(request):
    return render(request, 'gr8tutor/about.html')

def contact(request):
    return render(request, 'gr8tutor/contact.html')

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'gr8tutor/dashboard.html')

# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
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
            auth_login(request, user)
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
            return render(request, "gr8tutor/register.html",
                          {"error": "All fields are required."})

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
        profile, created = UserProfile.objects.create(user=user)
        
        # If role is valid, assign it
        if role in ("tutor", "student"):
            profile.role = role
            profile.save()
            if role == "tutor":
                # Create default Tutor profile
                Tutor.objects.get_or_create(user_profile=profile)
            elif role == "student":
                Student.objects.get_or_create(user_profile=profile)

        messages.success(request, "Account created. Please log in.")
        return redirect("login")

    # Pass role from GET parameters to template
    return render(request, "gr8tutor/register.html")

# Tutor managing a student list
# List of students
@login_required
def tutor_students(request):
    try:
        tutor = request.user.userprofile.tutor
    except (AttributeError, Tutor.DoesNotExist):
        return HttpResponseForbidden("You must be registered as a tutor.")
    
    pending_students = StudentTutorRelationship.objects.filter(
        tutor=tutor, is_active=False
        )
    active_students = StudentTutorRelationship.objects.filter(
        tutor=tutor, is_active=True
        )
    
    return render(
        request, "gr8tutor/tutor_students.html",
        {"pending_students": pending_students,
         "active_students": active_students
         })

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
    except (AttributeError, Tutor.DoesNotExist):
        return HttpResponseForbidden("You must be registered as a tutor.")
    
    # Defensive check: making sure the id from the URL is valid
    student = get_object_or_404(Student, id=student_id)
    if student.user_profile.role and student.user_profile.role != "student":
        # If the profile exists but is not a student
        raise Http404("The user is not a student.")

    # Relationship must exist
    relationship, created = StudentTutorRelationship.objects.get_or_create(
        tutor=tutor, student=student
    )
    relationship.is_active = True
    relationship.save()
    messages.success(request, f"{student.user_profile.user.username} confirmed as your student.")
    return redirect("tutor_students")

# Student sending request to Tutor
@login_required
def request_tutor(request, tutor_id):
    if request.user.userprofile.role != "student":
        return HttpResponseForbidden("Only students can request tutors.")
    
    # Tutor must exist
    tutor = get_object_or_404(Tutor, id=tutor_id)

    try:
        student = request.user.userprofile.student
    except (AttributeError, Student.DoesNotExist):
        return HttpResponseForbidden("You must be registered as a student.")

    # Don't allow duplilcate requests
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
    user_to_delete = get_object_or_404(User, id=user_id)

    # Only the user or admin can delete the account
    if request.user != user_to_delete and not request.user.is_staff:
        raise HttpResponseForbidden("You cannot delete this profile.")
    
    if request.user == user_to_delete:  # User deleting themselves
        user_to_delete.delete()
        auth_logout(request)
        return redirect("login")
    
    user_to_delete.delete()
    messages.success(request, "User deleted.")
    return redirect("admin_user_list")

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
        return HttpResponseForbidden("Chatting isn't allowed.")

    # Ensure that the current user and other user have a relationship
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

# Choose role view
@login_required
def choose_role(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
        )

    # Skip if user has a role
    if profile.role in ["tutor", "student"]:
        return redirect("dashboard")

    if request.method == "POST":
        role = request.POST.get("role")
        if role in ["tutor", "student"]:
            profile.role = role
            profile.save()
            # Create corresponding profile
            if role == "tutor":
                Tutor.objects.get_or_create(user_profile=profile)
            else:
                Student.objects.get_or_create(user_profile=profile)
            messages.success(request, "Role set. Thank you.")
            return redirect("dashboard")
        else:
            messages.error(request,
                           "Invalid role. Please choose tutor or student.")

    return render(request, "gr8tutor/choose_role.html")

# Tutor deleting a student
@login_required
def delete_student(request, student_id):
    # Only tutors can have access
    if request.user.userprofile.role != "tutor":
        return HttpResponseForbidden("Only tutors can remove students.")
    
    try:
        tutor = request.user.userprofile.tutor
    except (AttributeError, Tutor.DoesNotExist):
        return HttpResponseForbidden("You must be registered as a tutor.")

    # Find the relationship
    relationship = StudentTutorRelationship.objects.filter(
        tutor=tutor, student__id=student_id
    ).first()

    if not relationship:
        raise Http404("This student is not associated with you.")
    
    # Delete the relationship
    relationship.delete()
    messages.success(request, "Student removed successfully.")
    return redirect("tutor_students")