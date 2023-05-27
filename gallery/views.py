from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Nft_object, Category
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login as auth_login # login함수와 이름이 겹쳐서
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy
import requests
import json
import random

from .models import Nft_object
from .forms import NFT_form
import os
from animalNFT.settings import MEDIA_ROOT
from datetime import datetime
import sys

class PostList1(ListView):
    model = Nft_object
    ordering = '-pk'    
    template_name = "gallery/nft_object_l.html"

class PostList2(ListView):
    model = Nft_object
    ordering = '-pk'    
    template_name = "gallery/my_page.html"

    def get_context_data(self, **kwargs):
        context = super(PostList2, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def post(self, request):
        
        form = NFT_form(request.POST, request.FILES)
        
        if form.is_valid():
            NFT_object_ = form.save(commit=False)
            NFT_object_.owner = request.user
            # print(NFT_object)
            
            
            # saved_obj = NFT_object.objects.get(pk = obj.pk)
            
            
            NFT_username = str(request.user)
            
            current_date = str(datetime.today().strftime('%Y/%m/%d'))
            img_name =request.FILES['nft_image'].name.replace(" ", "_")
            NFT_image = open(MEDIA_ROOT +"/images/nft_images/"+current_date+"/"+ request.FILES['nft_image'].name.replace(" ", "_"),'rb')
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
            data = f'{{"to": "0xea57c26203cb95f90fa86039100101dcb6a1cbe6", "id": "{randomID}", "uri": "{token_uri}"}}'
            # print(data)
            response = requests.post('https://kip17-api.klaytnapi.com/v2/contract/animal-ntf-kaist5/token', headers=headers, data=data, auth=(access_key_id, secret_access_key))
            print(response.json())
            NFT_object_.tx_hash = response.json()["transactionHash"]
            NFT_object_.token_URI = token_uri
            NFT_object_.save()
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