from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..apps import get_client_ip
from ..models import Discussion, DiscussionCount


def index(request):
    """
    Discussion_list 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    so = request.GET.get('so', 'recent')

    if so == 'recommend':
        discussion_list = Discussion.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        discussion_list = Discussion.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    elif so == 'cntview':
        discussion_list = Discussion.objects.order_by('-view_count', '-create_date')
    else:  # recent
        discussion_list = Discussion.objects.order_by('-create_date')

    # 조회
    if kw:
        discussion_list = discussion_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw)  # 질문 글쓴이검색
            # Q(answer__author__username__icontains=kw)   # 답변 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(discussion_list, 10)
    page_obj = paginator.get_page(page)

    context = {'discussion_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'board/discussion_list.html', context)


def detail(request, discussion_id):
    """
    Discussion_context 출력
    """
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    context = {'discussion': discussion}

    ip = get_client_ip(request)
    cnt = DiscussionCount.objects.filter(ip=ip, discussion=discussion).count()
    if cnt == 0:
        qc = DiscussionCount(ip=ip, discussion=discussion)
        qc.save()
        if discussion.view_count:
            discussion.view_count += 1
        else:
            discussion.view_count = 1
        discussion.save()

    return render(request, 'board/discussion_detail.html', context)
