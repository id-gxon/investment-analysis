from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Discussion, Answer


@login_required(login_url='common:login')
def vote_discussion(request, discussion_id):
    """
    discussion_vote 등록
    """
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    if request.user == discussion.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        discussion.voter.add(request.user)
    return redirect('board:detail', discussion_id=discussion.id)


@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    """
    discussion_answer_vote 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        answer.voter.add(request.user)
    return redirect('board:detail', discussion_id=answer.discussion.id)
