from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Discussion


def index(request):
    """
    Discussion_list 출력
    """
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    if so == 'recommend':
        discussion_list = Discussion.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        discussion_list = Discussion.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    elif so == 'view':
        discussion_list = Discussion.objects.annotate(num_view=Count('hitting')).order_by('-num_hitting', '-create_date')
    else:  # recent
        discussion_list = Discussion.objects.order_by('-create_date')

    if kw:
        discussion_list = discussion_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

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

    return render(request, 'board/discussion_detail.html', context)
