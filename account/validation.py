from django.contrib.auth.models import User
from django import forms
from .models import *

# Validation Start for Registration Form

class RegisterFormValidation(forms.ModelForm):
    email = forms.CharField(
        max_length=50,
        error_messages = {
            'required': 'Email field is required.',
                
        }
        )
    password=forms.CharField(
        widget=forms.PasswordInput(),
        error_messages = {
            'required': 'Password field is required.',
        })
    confirm_password=forms.CharField(
        widget=forms.PasswordInput(),
        error_messages = {
            'required': 'Confirm Password field is required.',
                
        })
    

    class Meta:
        model = User
        fields = ['email', 'password']
       

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data.items())
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError({'confirm_password': 'Confirm Password do not match'})

        return cleaned_data
    

# Validation End for Registration Form


# Validation Start for Login Form

class LoginFormValidation(forms.ModelForm):
    email = forms.CharField(
        max_length=50,
        error_messages = {
            'required': 'Email field is required.',       
        })
    password=forms.CharField(
        widget=forms.PasswordInput(),
        error_messages = {
            'required': 'Password field is required.',
        })
    
    class Meta:
        model = User
        fields = ['email', 'password']
       
# Validation End for Login Form


# Validation Start for Profile Form

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'profile_image']