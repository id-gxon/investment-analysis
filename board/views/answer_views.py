from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Discussion, Answer


@login_required(login_url='common:login')
def answer_create(request, discussion_id):
    """
    Discussion_answer 등록
    """
    discussion = get_object_or_404(Discussion, pk=discussion_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.discussion = discussion
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('board:detail', discussion_id=discussion.id), answer.id))
    else:
        form = AnswerForm()

    context = {'discussion': discussion, 'form': form}
    return render(request, 'board/discussion_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    discussion_answer 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('board:detail', discussion_id=answer.discussion.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('board:detail', discussion_id=answer.discussion.id), answer.id))
    else:
        form = AnswerForm(instance=answer)

    context = {'answer': answer, 'form': form}
    return render(request, 'board/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    discussion_answer 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('board:detail', discussion_id=answer.discussion.id)
