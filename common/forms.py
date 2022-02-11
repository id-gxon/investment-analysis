from django import forms
from django.contrib.auth.forms import UserCreationForm

from common.models import Profile


class SignupForm(UserCreationForm):

    email = forms.EmailField(label="이메일")

    class Meta:
        model = Profile  # 사용할 모델
        fields = ['username', 'email', 'nickname', 'password1', 'password2', 'stock_firm']
#
#
# class SignupForm(UserCreationForm):
#    email = forms.EmailField(label="이메일")
#          def save(self):
#              user = super().save()
#              profile = Profile.objects.create(
#              user=user,phone_number=self.cleaned_data['phone_number'])
#              return user