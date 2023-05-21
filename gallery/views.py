from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts': posts,
#         }
#     )

class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'gallery/blog.html'


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
    model = Post
    template_name = 'blog/post_detail.html'