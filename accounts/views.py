from django.shortcuts import render

import pycountry
from .models import Nation, NftUser
from gallery.models import Nft_object, Category
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login # login함수와 이름이 겹쳐서
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from .forms import UserForm
from animalNFT.settings import BASE_DIR
import os
import requests
from django.http import JsonResponse

# # Create your views here.
# def login(request) : 
#     if request.method=='POST' :
        
#         # data는 forms.form 두번쨰 인자이므로 data = 은 생략 가능
#         # print(request)
#         print(request.POST)
#         form = AuthenticationForm(request, data = request.POST) # 먼저 request 인자를 받아야함
#         print(form)
#         print(form.get_user())
#         if form.is_valid() :
#             print("valid form")
#             # 세션 CREATE/ form.get_user는 User 객체 반환
#             auth_login(request, form.get_user())
#             return redirect('gallery') # 로그인 성공시 메인페이지 이동
#     else :
#         form = AuthenticationForm()

#     context = {
#         'form' : form,
#     }
#     return render(request, 'single_pages/login.html', context)


# Create your views here.
# def create_wallet(request) : 
#   global chain_id, access_key_id, secret_access_key
#   if request.method=='POST' :
#     headers = {
#       'x-chain-id': {chain_id},
#       'x-krn':{account_pool_krn}
#     }
#     response = requests.post('https://wallet-api.klaytnapi.com/v2/account', headers=headers, auth=(access_key_id, secret_access_key))
#     # print(response.json())
#     return JsonResponse(response.json())
#   else :
#     pass
#   context = {
#   }
#   return render(request, 'single_pages/login.html', context)

def login(request):


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = NftUser.objects.get(username=username)
            if check_password(password, user.password):
                auth_login(request, user)
                return redirect('gallery:post_list')  # Redirect to the main page upon successful login
        except NftUser.DoesNotExist:
            pass

        error_message = "Invalid username or password. Please try again."
    else:
        error_message = None

    context = {
        'error_message': error_message,
    }
    return render(request, 'single_pages/login.html', context)

def create_account(request):
    nation_choices = [(country.alpha_2, country.name) for country in pycountry.countries]
    print(request.POST)
    if request.method == 'POST':
        form = UserForm(request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            
            chain_id = str(1001)
            access_key_id = "KASKHT32FUV2LSVC00OZ2DHM";
            secret_access_key = "XM-hoBODxZCZdpgvJqeWl7LdG2JpGX4Ny5YB16Qa";
            account_pool_krn = "krn:1001:wallet:56ba73e4-b905-4cf2-aa8f-c4ec16d68430:account-pool:default"
            
            headers = {
            'x-chain-id': chain_id,
            'x-krn':account_pool_krn            }
            response = requests.post('https://wallet-api.klaytnapi.com/v2/account', headers=headers, auth=(access_key_id, secret_access_key))
            response_json = response.json()
            
            user = NftUser.objects.get(username=username)
            user.NFT_wallet_addr = response_json['address']
            user.NFT_private_key = response_json['keyId']
            user.NFT_public_key = response_json['publicKey']
            user.save()
            user2 = NftUser.objects.get(username=username)
            print(user2.NFT_wallet_addr)
            return redirect('gallery:post_list')
    else:
        # Render the registration form with the country choices
        context = {
            'nation_choices': nation_choices
        }
    return render(request, 'single_pages/login copy.html', context)
    

def decide(request):
    # if request.user.is_authenticated:
    #     # User is logged in, redirect to my_page
    #     return redirect('accounts:my_page')
    # else:
    #     # User is not logged in, redirect to login
    #     return redirect('accounts:login')
    print("fuck you my passsge")
    return redirect('/account/login')



    
