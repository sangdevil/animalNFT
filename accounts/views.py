from django.shortcuts import render


    
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login # login함수와 이름이 겹쳐서
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def login(request) : 
    if request.method=='POST' :
        
        # data는 forms.form 두번쨰 인자이므로 data = 은 생략 가능
        # print(request)
        print(request.POST)
        form = AuthenticationForm(request, data = request.POST) # 먼저 request 인자를 받아야함
        print(form)
        if form.is_valid() :
            # print("hey")
            # 세션 CREATE/ form.get_user는 User 객체 반환
            auth_login(request, form.get_user())
            return redirect('gallery') # 로그인 성공시 메인페이지 이동
    else :
        form = AuthenticationForm()

    context = {
        'form' : form,
    }
    return render(request, 'single_pages/login.html', context)

def create_account(request):
    return render(request, 'single_pages/login copy.html')