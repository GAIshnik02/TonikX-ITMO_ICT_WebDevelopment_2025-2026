from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('submit/<int:homework_id>/', views.submit_homework, name='submit_homework'),
    path('grades/', views.grades, name='grades'),
]
