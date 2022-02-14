from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignUpForm
from .models import Profile


@login_required
def profile(request):
    """
    profile
    """
    profile_list = Profile.objects.order_by()
    context = {'profile_list': profile_list}
    return render(request, 'common/profile.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.nickname = form.cleaned_data.get('nickname')
            user.profile.stock_firm = form.cleaned_data.get('stock_firm')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(settings.LOGIN_URL)
    else:
        form = SignUpForm()
    return render(request, 'common/signup.html', {'form': form})


@login_required(login_url='common:login')
def profile_update(request):
    """
    profile 수정
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = request.user
            user.profile.nickname = form.cleaned_data('nickname')
            user.profile.stock_firm = form.cleaned_data('stock_firm')
            user.save()
            return redirect('common:profile')
        else:
            form = SignUpForm()
        return render(request, 'common/profile.html', {'form': form})


@login_required(login_url='common:login')
def profile_delete(request):
    """
    profile 삭제
    """
    profile.delete()
    return redirect('board:index')
