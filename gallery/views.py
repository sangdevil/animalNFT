from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Nft_object, Category
from django.contrib.auth.mixins import LoginRequiredMixin

class PostList(ListView):
    model = Nft_object
    ordering = '-pk'
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
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
        