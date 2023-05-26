from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from gallery.models import Nft_object, Category
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login as auth_login # login함수와 이름이 겹쳐서
from django.contrib.auth.forms import AuthenticationForm

class PostList(ListView):
    model = Nft_object
    ordering = '-pk'
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context

