from django.urls import path
from django.shortcuts import render
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.scrape_clubs, name='football'),
    path('success/', views.success, name='success')

]