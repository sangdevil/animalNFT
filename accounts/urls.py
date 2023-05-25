from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test

from . import views
# Custom function to check if the user is logged in
def check_user_login(user):
    return user.is_authenticated
app_name = 'accounts'
urlpatterns = [
    path('', user_passes_test(check_user_login, login_url='login')(views.my_page), name='my_page'),
    path('create_account', views.create_account, name = 'create_account'),
    path('login', views.login, name='login')
    # 다른 URL 패턴들...
]