from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserRegisterForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['title', 'first_name', 'last_name', 'category']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    category = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ['title', 'username', 'first_name', 'last_name', 'email', 'category', 'gender']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'status', 'image']
