from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("accounts/", include("allauth.urls")),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('tutors/', views.tutors, name='tutors'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
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

