from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import DiscussionForm
from ..models import Discussion


@login_required(login_url='common:login')
def discussion_create(request):
    """
    discussion 등록
    """
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.create_date = timezone.now()
            discussion.save()
            return redirect('board:index')
    else:
        form = DiscussionForm()

    context = {'form': form}
    return render(request, 'board/discussion_form.html', context)


@login_required(login_url='common:login')
def discussion_modify(request, discussion_id):
    """
    discussion 수정
    """
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    if request.user != discussion.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('board:detail', discussion_id=discussion.id)

    if request.method == "POST":
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.modify_date = timezone.now()
            discussion.save()
            return redirect('board:detail', discussion_id=discussion.id)
    else:
        form = DiscussionForm(instance=discussion)
    context = {'form': form}
    return render(request, 'board/discussion_form.html', context)


@login_required(login_url='common:login')
def discussion_delete(request, discussion_id):
    """
    discussion 삭제
    """
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    if request.user != discussion.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('board:detail', discussion_id=discussion.id)
    discussion.delete()
    return redirect('board:index')
