from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import NftUser

class UserForm(UserCreationForm):
    class Meta:
        model = NftUser
        fields = ("username", "email", "user_image", "birth_date", "password1", "password2", "nation" )