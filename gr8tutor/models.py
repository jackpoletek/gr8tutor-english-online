from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('tutor', 'Tutor'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def unique_role(self, role):
        if User.objects.filter(email=self.user.email).exists() \
           and self.role != role:
            raise ValidationError(
                f"This email is already registered ({self.role}).")

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Tutor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.user_profile.user.username
    
    def current_students(self):
        students = []
        for rship in StudentTutorRelationship.objects.filter(tutor=self,
                                                             is_active=True):
            students.append(rship.student)
        return students
    
    def save(self, *args, **kwargs):
        self.user_profile.unique_role("tutor")
        super().save(*args, **kwargs)

class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    goals = models.TextField(blank=True)

    def __str__(self):
        return self.user_profile.user.username
    
    def save(self, *args, **kwargs):
        self.user_profile.unique_role("student")
        super().save(*args, **kwargs)

class StudentTutorRelationship(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'tutor')
        ordering = ['-is_active', 'tutor__user_profile__user__username']

    def __str__(self):
        status = "Active" if self.is_active else "Pending"
        return f"{self.student} - {self.tutor} ({status})"

# Messaging between Tutor and Student
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="received_messages")
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.recipient} at {self.time}"