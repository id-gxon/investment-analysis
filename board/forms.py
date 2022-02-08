from django import forms
from board.models import Discussion, Answer


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion  # 사용할 모델
        fields = ['subject', 'content', 'image']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            # 'image': forms.ImageField(attrs={'class': 'form-control'})
        }
        labels = {
            'subject': '제목',
            'content': '내용',
            'image': '사진',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'image']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
        }
        labels = {
            'content': '답글내용',
            'image': '사진',
        }
