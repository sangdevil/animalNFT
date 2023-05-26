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
def login(request):


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = NftUser.objects.get(username=username)
            if check_password(password, user.password):
                auth_login(request, user)
                return redirect('gallery/')  # Redirect to the main page upon successful login
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

    if request.method == 'POST':
        # Handle the form submission
        # ...
        form = AuthenticationForm(request, data = request.POST) # 먼저 request 인자를 받아야함
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



    
