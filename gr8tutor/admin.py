from django.contrib import admin

# Register your models here.
from .models import UserProfile, Tutor, Student, StudentTutorRelationship, Message

admin.site.register(UserProfile)
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(StudentTutorRelationship)
admin.site.register(Message)
