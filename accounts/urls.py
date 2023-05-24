from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.login, name='login'),
    path('create_account', views.create_account, name = 'create_account')
    
    # 다른 URL 패턴들...
]