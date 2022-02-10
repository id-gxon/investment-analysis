from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from board.views import base_views
from stockpredapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', include('board.urls')),
    path('common/', include('common.urls')),
    path('board', base_views.index, name='index'),
    path('stockpredapp/', include('stockpredapp.urls')),
    path('', views.jisu)

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)