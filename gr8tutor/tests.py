from django.test import TestCase
from django.contrib.auth.models import User
from gr8tutor.models import UserProfile, Tutor, Student
from django.urls import reverse

# Create your tests here.
class UserProfileAndRoleTests(TestCase):
    
    def setUp(self):
        self.student_user = User.objects.create_user(
            username="student", password="testpass"
            )
        self.tutor_user = User.objects.create_user(
            username="tutor", password="testpass"
            )
        
        self.student_profile = UserProfile.objects.get(user=self.student_user)
        self.tutor_profile = UserProfile.objects.get(user=self.tutor_user)
        
        self.student_profile.role = "student"
        self.student_profile.save()

        self.tutor_profile.role = "tutor"
        self.tutor_profile.save()
        
        Student.objects.create(user_profile=self.student_profile)
        Tutor.objects.create(user_profile=self.tutor_profile)
        
    def test_user_profiles_created_automatically(self):
        self.assertIsNotNone(self.student_profile)
        self.assertIsNotNone(self.tutor_profile)

    def test_student_role_assigned(self):
        self.assertEqual(self.student_profile.role, "student")

    def test_tutor_role_assigned(self):
        self.assertEqual(self.tutor_profile.role, "tutor")
        