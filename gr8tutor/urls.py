from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Static pages
    path('about/', views.about, name='about'),
    path('tutors/', views.tutors, name='tutors'),
    path('contact/', views.contact, name='contact'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Tutor/Student
    path('tutor/students/', views.tutor_students, name='tutor_students'),
    path('confirm-student/<int:student_id>/', views.confirm_student, name='confirm_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('request-tutor/<int:tutor_id>/', views.request_tutor, name='request_tutor'),
    path('choose-role/', views.choose_role, name='choose_role'),

    # Admin
    path('delete-profile/<int:user_id>/', views.delete_profile, name='delete_profile'),
    path('admin-user-list/', views.admin_user_list, name='admin_user_list'),

    # Chat
    path('chat/<int:other_party_id>/', views.chat_view, name='chat'),

    # Endpoints
]

