from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'email']
