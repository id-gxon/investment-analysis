from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserForm(UserCreationForm):
    username = forms.EmailField(label="username")
    nickname = forms.CharField(max_length=16)
    # stockfirm = forms.

    class Meta:
        model = User
        fields = ["username", "nickname", "password1", "password2"]


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ["nickname", "password"]
