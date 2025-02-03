from django.urls import path
from django.shortcuts import render
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', RedirectView.as_view(url='index')),
    path('about/', views.about, name='about'),
    path('website/', views.website, name='website'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('login/', views.login, name='login'),
]