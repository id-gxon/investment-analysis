from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email


class SignupForm(UserCreationForm):
    def clean_username(self):
        value = self.cleaned_data.get('username')
        if value:
            validate_email(value)
        return value
    nickname = forms.CharField(max_length=20)
