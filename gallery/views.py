from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Nft_object, Category
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login as auth_login # login함수와 이름이 겹쳐서
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy
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
    
class PostCreate(CreateView):
    model = Nft_object
    fields = ['title', 'nft_image', 'description', 'category', "owner"]
    success_url = reverse_lazy('NFT:mint_token')
    # def get_success_url(self):
    #     # return reverse('NFT:mint_token')
    #     print(self)
    #     return render(self.object,'NFT:mint_token')
    # mint_token(title, Nft_object, des)
    def form_valid(self, form):
        title = form.cleaned_data['title']
        nft_image = form.cleaned_data['nft_image']
        description = form.cleaned_data['description']
        # category = form.cleaned_data['category']
        # owner = form.cleaned_data['owner']
        
        obj = form.save(commit=False)
        obj.image = nft_image
        obj.save()
        
        
        self.request.session['title'] = title
        # self.request.session['nft_image'] = nft_image
        self.request.session['description'] = description
        # self.request.session['category'] = category
        # self.request.session['owner'] = owner
        return super().form_valid(form)

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