from django import forms
from betterforms.multiform import MultiModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Profile

class UserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ["first_name", "last_name", "username", "email","password1", "password2"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['profile_picture']

class CombinedForm(MultiModelForm):
    form_classes = {
        'user':UserForm,
        'profile':ProfileForm
    }