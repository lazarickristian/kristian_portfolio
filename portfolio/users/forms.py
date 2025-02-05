from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
#from .models import Profile

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )