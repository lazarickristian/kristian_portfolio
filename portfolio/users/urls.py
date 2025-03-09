from django.urls import path
from django.shortcuts import render
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register_user.as_view(), name='register'),
    path('edit/', views.Edit_User.as_view(), name='edit_user'),
    path('delete-user/', views.DeleteUserView.as_view(), name='delete_user'),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', views.CustomPasswordResetView.as_view(html_email_template_name='users/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',views.CustomPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]


