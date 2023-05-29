from django.urls import path, include
from . import views
# 각 요청은 views.py에서 함수로 처리
urlpatterns = [
    path('', views.HotFeed.as_view(), name='home'),
    path('gallery/', include('gallery.urls')),
    path('login/', include('gallery.urls'))
    ]