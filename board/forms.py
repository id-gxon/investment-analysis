from django import forms
from board.models import Discussion, Answer


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion  # 사용할 모델
        fields = ['subject', 'content', 'image', 'voter']
        labels = {
            'subject': '제목',
            'content': '내용',
            'image': '사진',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'image', 'voter']
        labels = {
            'content': '답글내용',
            'image': '사진',
        }
