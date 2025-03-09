from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from .models import Profile

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

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
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
        user_id = self.instance.id  # Get the ID of the user being edited

        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError("A user with this email already exists.")
        
        return email
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New Password',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm New Password',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    class Meta:
        model = User
        fields = ['email']

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New Password',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm New Password',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2',]