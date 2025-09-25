from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("accounts/", include("allauth.urls")), # allauth handles login/register/logout
    path('index/', views.index, name='index'),
    path('dashboard/', views.index, name='dashboard'),
    path('about/', views.about, name='about'),
    path('tutors/', views.tutors, name='tutors'),
    path('contact/', views.contact, name='contact'),

    # Tutor/Student
    path('tutor/students/', views.tutor_students, name='tutor_students'),
    path('confirm-student/<int:student_id>/', views.confirm_student, name='confirm_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('request-tutor/<int:tutor_id>/', views.request_tutor, name='request_tutor'),

    # Admin
    path('delete-profile/<int:user_id>/', views.delete_profile, name='delete_profile'),
    path('admin-user-list/', views.admin_user_list, name='admin_user_list'),

    # Chat
    path('chat/<int:other_party_id>/', views.chat_view, name='chat'),

    # Endpoints

]

