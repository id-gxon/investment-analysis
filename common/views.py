from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash


def signup(request):
    """
    회원 가입
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request,"회원 가입을 환영합니다.")
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


@login_required(login_url='common:login')
def update(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('common:people')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'common/user_update.html', {'form': form})


@login_required(login_url='common:login')
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('board:discussion_list')
    return render(request, 'common/delete.html')
