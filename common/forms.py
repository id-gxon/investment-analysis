from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    nickname = forms.CharField(max_length=20)
    email = forms.EmailField(label="이메일")
    STOCK_FIRM_CHOICE = (
        ('키움증권', 'KIWOOM'),
        ('삼성증권', 'SAMSUNG'),
        ('한국투자증권', 'KOREA'),
        ('KB증권', 'KOOKMIN'),
        ('NH투자증권', 'NONGHYUP'),
        ('미래에셋증권', 'MIREA'),
        ('신한금융투자', 'SHINHAN'),
        ('그 외', 'ETC')
    )
    stock_firm = forms.ChoiceField(choices=STOCK_FIRM_CHOICE)

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'password1', 'password2', 'stock_firm')


class UpdateForm(UserChangeForm):
    password = None
    nickname = forms.CharField(max_length=20)
    email = forms.EmailField(label="이메일")
    STOCK_FIRM_CHOICE = (
        ('키움증권', 'KIWOOM'),
        ('삼성증권', 'SAMSUNG'),
        ('한국투자증권', 'KOREA'),
        ('KB증권', 'KOOKMIN'),
        ('NH투자증권', 'NONGHYUP'),
        ('미래에셋증권', 'MIREA'),
        ('신한금융투자', 'SHINHAN'),
        ('그 외', 'ETC')
    )
    stock_firm = forms.ChoiceField(choices=STOCK_FIRM_CHOICE)

    class Meta:
        model = User
        fields = ('nickname', 'stock_firm')
