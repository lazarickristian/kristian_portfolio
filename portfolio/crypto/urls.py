from django.urls import path
from django.shortcuts import render
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.crypto_dashboard_view, name='crypto'),
    path('download/', views.download_csv_view, name='crypto_csv'),
]