from django import forms
from django_countries import countries

class CVForm(forms.Form):
    first_name = forms.CharField(
        label="First Name", 
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        }))
    
    last_name = forms.CharField(
        label="Last Name", 
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        }))
    
    profession = forms.CharField(
        label="Profession", 
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Profession',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        }))

    city = forms.CharField(
        label="City", 
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        }))

    country = forms.ChoiceField(
        label="Country", 
        choices=[("", "Country")] + list(countries),
        widget=forms.Select(attrs={
            'class': 'w-full country-dropdown',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        }))

    email = forms.EmailField(
        label="Email Address",
        widget=forms.TextInput(attrs={
            'placeholder': 'Email Address',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        }))
                             
    phone = forms.CharField(
        label="Phone Number", 
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone Number',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        }))
                            
    summary = forms.CharField(
        label="Summary", 
        widget=forms.Textarea(attrs={
            'placeholder': 'Summary',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        }))
    
    photo = forms.ImageField(label="Upload Photo", required=False)
    skills = forms.CharField(widget=forms.HiddenInput(), required=False)  
    languages = forms.CharField(widget=forms.HiddenInput(), required=False)
    work_experience = forms.CharField(widget=forms.HiddenInput(), required=False)  
    education = forms.CharField(widget=forms.HiddenInput(), required=False)
    social_links = forms.CharField(widget=forms.HiddenInput(), required=False)