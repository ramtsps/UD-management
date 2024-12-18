from django import forms
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields ='__all__'

class UserProfileForm(forms.ModelForm):
    new_password = forms.CharField(required=False, widget=forms.PasswordInput, label="New Password")

    class Meta:
        model = UserData
        fields = ['username', 'email', 'profile_picture']  # Exclude password from regular fields

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)  # Hash and set the new password
        if commit:
            user.save()
        return user
    


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    profile_picture = forms.ImageField(required=False)  # Allow profile picture upload (optional)

   

class RegisterForm_changes(forms.ModelForm):
    # Define custom form fields if needed
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = UserData  # Link the form to your model
        fields = ['username', 'email', 'password']  # Fields to include in the form

    # Custom validation for the confirm_password field
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username or password.")
        return cleaned_data