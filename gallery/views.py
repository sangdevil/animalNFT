from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Nft_object, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login # login함수와 이름이 겹쳐서
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy
import requests
import json
import random

from .models import Nft_object
from .forms import NFT_form
from accounts.models import NftUser
import os
from animalNFT.settings import MEDIA_ROOT
from datetime import datetime
import sys

class PostList1(ListView):
    model = Nft_object
    ordering = '-pk'    
    template_name = "gallery/nft_object_l.html"
    def get_context_data(self, **kwargs):
        context = super(PostList1, self).get_context_data(**kwargs)
        # nation_img = self.request.user.nation
        print(self.request.GET.get('category', ''))

        context['selected_category'] = self.request.GET.get('category', '')
        context['categories'] = Category.objects.all()
        return context
class PostList2(ListView):
    model = Nft_object
    ordering = '-pk'    
    template_name = "gallery/my_page.html"

    def get_context_data(self, **kwargs):
        context = super(PostList2, self).get_context_data(**kwargs)
        current_username = self.request.user
        filtered_nft_objects = Nft_object.objects.filter(owner=current_username)
        # nation_img = self.request.user.nation
        print(self.request.GET.get('category', ''))
        print("fuck you")
        print("fuck you")
        print("fuck you")
        
        print("fuck you")
        print("fuck you")
        print("fuck you")
        context['selected_category'] = self.request.GET.get('category', '')
        context['user_nfts'] = filtered_nft_objects
        context['categories'] = Category.objects.all()
        return context
    
    def post(self, request):
        
        form = NFT_form(request.POST, request.FILES)
        
        if form.is_valid():
            temp_object = form.save(commit=False)
            # form.owner = request.user
            # NFT_object_ = Nft_object.objects.get(owner_id=request.user)
            # print(NFT_object_)
            # NFT_object_.owner = request.user
            # NFT_object_.save()
            
            temp_object.owner = request.user
            temp_object.save()
            # print(NFT_object)
            
            
            # saved_obj = NFT_object.objects.get(pk = obj.pk)
            
            
            NFT_username = str(request.user)
            
            current_date = str(datetime.today().strftime('%Y\\%m\\%d'))
            img_name =request.FILES['nft_image'].name.replace(" ", "_")
            NFT_image = open(MEDIA_ROOT +"\\images\\nft_images\\"+current_date+"\\"+ request.FILES['nft_image'].name.replace(" ", "_"),'rb')
            # test = open("../media/images/nft_images/2023/05/26/우아한_청년들_릴레이_채용_데이터_분석_1EXhOuQ.png", 'rb')
            # print(test)
            meta_data = {"image":None,"name":"AnimalNFT","description":"Test","properties":{"owner":NFT_username}}
            headers = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDZjZTZkODZBYTkwOTA4Q2UxMkU1QWMzRGU5MzRkNDVmNTRBOTgyOTgiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY4NDY1MzgzNTkxNiwibmFtZSI6IkFuaW1hbE5GVCJ9.v3BSPEDt3fH3ZD2F2qTXqQa6IUcp5qnpA3MHXtn5QrA"}
            files = {
                'image': (img_name, NFT_image),
                'meta': (None, json.dumps(meta_data))
                }
            # print(files)
            # files = {
            #     'meta': {"name":"AnimalNFT","image":NFT_image_data, "properties":{"videoClip": null}}}
            # print(json.parse(files))

            response = requests.post('https://api.nft.storage/store', files=files, headers=headers)
            # if not response.status_code ==200:
            #     return render(request, 'gallery:post_list')
            IPFS_data = response.json()
            # print(IPFS_data)
            token_uri = IPFS_data["value"]['url']


            #klaytn token minting
            # global chain_id, access_key_id, secret_access_key
            chain_id = "1001"
            access_key_id = "KASKHT32FUV2LSVC00OZ2DHM"
            secret_access_key = "XM-hoBODxZCZdpgvJqeWl7LdG2JpGX4Ny5YB16Qa"
            
            headers = {
                'x-chain-id': chain_id,
                'Content-Type': 'application/json',
                
            }
            randomID = str(hex(random.randint(0, sys.maxsize)))
            # data = {"to": "0x20b718A535251B4DceA83a0B79EF12723835A898", "id": randomID, "uri": token_uri}
            # print(randomID)
            # print(token_uri)
            NFT_user_model_data = NftUser.objects.get(username = request.user)
            NFT_wallet_addr =NFT_user_model_data.NFT_wallet_addr
            data = f'{{"to": "{NFT_wallet_addr}", "id": "{randomID}", "uri": "{token_uri}"}}'
            # print(data)
            response = requests.post('https://kip17-api.klaytnapi.com/v2/contract/animal-ntf-kaist5/token', headers=headers, data=data, auth=(access_key_id, secret_access_key))
            # print(response.json())
            NFT_object_saved = Nft_object.objects.get(owner_id=request.user)
            NFT_object_saved.tx_hash = response.json()["transactionHash"]
            NFT_object_saved.token_URI = token_uri
            NFT_object_saved.save()
            return render(request, "gallery/nft_object_l.html")
        

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
    

def update_like(request, nft_object_id):
    # print(request.POST)
    # print(nft_object_id)
    if request.method == 'POST' and request.user.is_authenticated:
        nft_object = Nft_object.objects.get(id=nft_object_id)
        user = request.user
        
        if nft_object.like_users.filter(id=user.id).exists():
            # User has already liked, remove the like
            nft_object.like_users.remove(user)
            is_liked = False
        else:
            # User has not liked, add the like
            nft_object.like_users.add(user)
            is_liked = True
        nft_object.save()
        print(nft_object)
        return JsonResponse({'is_liked': is_liked})
    
    return JsonResponse({'error': 'Invalid request'})




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