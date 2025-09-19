from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tutors/', views.tutors, name='tutors'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('my-students/', views.tutor_students, name='tutor_students'),
    path('confirm-student/<int:student_id>/', views.confirm_student,
         name='confirm_student'),
    path('delete-student/<int:student_id>/', views.delete_student,
         name='delete_student'),
    path('request-tutor/<int:tutor_id>/', views.request_tutor,
         name='request_tutor'),

    # Endpoints

]

