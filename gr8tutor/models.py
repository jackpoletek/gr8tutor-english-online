from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('tutor', 'Tutor'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

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

class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    goals = models.TextField(blank=True)

    def __str__(self):
        return self.user_profile.user.username

class StudentTutorRelationship(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'tutor')

    def __str__(self):
        return f"{self.student} - {self.tutor}"

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