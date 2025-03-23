from django.urls import path
from django.shortcuts import render
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.cv_generator, name='cv_generator'),
]