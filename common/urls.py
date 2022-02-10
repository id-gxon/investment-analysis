from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('common:profile'), template_name='common/password_change.html'), name='password_change'),
]