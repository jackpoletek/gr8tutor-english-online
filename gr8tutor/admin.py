from django.contrib import admin

# Register your models here.
from .models import UserProfile, Tutor, Student, StudentTutorRelationship, Message
from django_summernote.admin import SummernoteModelAdmin

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ("user_profile", "subject", "hourly_rate")
    search_fields = ("user_profile__user__username", "subject")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user_profile", "goals")
    search_fields = ("user_profile__user__username",)


@admin.register(StudentTutorRelationship)
class StudentTutorRelationshipAdmin(admin.ModelAdmin):
    list_display = ("student", "tutor", "is_active")
    list_filter = ("is_active",)
    search_fields = ("student__user_profile__user__username",
                     "tutor__user_profile__user__username")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "time", "text")
    search_fields = ("sender__username", "recipient__username", "text")
    list_filter = ("time",)
