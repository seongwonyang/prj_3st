# -*- coding: utf-8 -*-
from .common import *

def new_LoginView(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        user_id= request.POST.get('user_id')
        user_pw= request.POST.get('user_pw')

        user = authenticate(request, username=user_id, password=user_pw)

        if user is not None:
            login(request,user=user)
            return redirect('instagram:main')

        else:
            messages.error(request,'ID 혹은 비밀번호 오류입니다.')
            return redirect('accounts:login')
