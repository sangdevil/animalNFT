from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView

from . import views
# Custom function to check if the user is logged in
def check_user_login(user):
    return user.is_authenticated
app_name = 'my_page'
urlpatterns = [
    path('', views.PostList.as_view(), name = "post_list"),
]