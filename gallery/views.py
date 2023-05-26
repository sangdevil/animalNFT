from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Nft_object, Category
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login as auth_login # login함수와 이름이 겹쳐서
from django.contrib.auth.forms import AuthenticationForm
class PostList1(ListView):
    model = Nft_object
    ordering = '-pk'    
    template_name = "gallery/nft_object_list.html"

class PostList2(ListView):
    model = Nft_object
    ordering = '-pk'    
    template_name = "gallery/my_page.html"

    def get_context_data(self, **kwargs):
        context = super(PostList2, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# def single_post_page(request, pk):
#     posts = Post.objects.get(pk=pk)
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'posts': posts,
#         }
#     )

class PostDetail(DetailView):
    model = Nft_object
    template_name = 'blog/post_detail.html'
    
def home(request):
    return render(
        request,
        '/',
    )
    
def gallery(request):
    return render(
        request,
        'gallery/blog.html'
    )    
        

def my_page(request):
    print("fuck you")
    return render(request, 'single_pages/my_page.html')