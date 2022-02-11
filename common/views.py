from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignupForm
from .models import Profile


@login_required
def profile(request):
    profile_list = Profile.objects.order_by()
    context = {'profile_list': profile_list}
    return render(request, 'common/profile.html', context)


def signup(request):
    print('test1')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print('test4')
        if form.is_valid():
            print('test2')
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        print('test3')
        form = SignupForm()
    return render(request, 'common/signup.html', {'form': form})
