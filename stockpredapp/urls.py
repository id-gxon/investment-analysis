from django.urls import path

from . import views

app_name = 'stockpredapp'

urlpatterns = [
    path('', views.s_index, name='s_index'),
    path('<int:stock_id>/', views.result, name='result'),
    path('loading/<int:stock_id>/', views.loading, name='loading'),
    path('jisu/', views.jisu, name='jisu'),
    path('main_loading/', views.main_loading, name='main_loading'),
    path('main_loading2/', views.main_loading2, name='main_loading2')



]