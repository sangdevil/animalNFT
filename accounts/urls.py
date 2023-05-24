from django.urls import path, include
from . import views


app_name = "accounts"
urlpatterns = [
    path('', views.login, name='login'),
    
    # 다른 URL 패턴들...
]