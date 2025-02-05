from django.urls import path
from django.shortcuts import render
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register_user.as_view(), name='register'),
]