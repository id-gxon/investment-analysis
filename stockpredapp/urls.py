from django.urls import path

from . import views

app_name = 'stockpredapp'

urlpatterns = [
    path('', views.s_index, name='s_index'),
    path('<int:stock_id>/', views.result, name='result'),
]