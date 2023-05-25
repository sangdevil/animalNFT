from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'accounts'
urlpatterns = [
    path('create_wallet', views.create_wallet, name='create_wallet'),
    path('mint_token', views.mint_token, name='mint_token'),
    
]