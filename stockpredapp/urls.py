from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:stock_id>/', views.result, name='result'),
]