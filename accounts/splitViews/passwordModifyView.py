# -*- coding: utf-8 -*-
from .common import *

@login_required
def passwordModifyView(request):
    if request.method == 'GET':
        return render(request, 'password_modify.html')

    elif request.method == 'POST':
        user = request.user

        user_pw = request.POST.get('user_pw')
        new_user_pw = request.POST.get('new_user_pw')
        user_ch_pw = request.POST.get('user_ch_pw')

        if user.check_password(user_pw):
            if user.check_password(new_user_pw):
                messages.error(request, '새 비밀번호는 기존의 비밀번호와 다르게 설정해주세요.')
                return redirect('accounts:passwordmodify')

            else:
                if new_user_pw == user_ch_pw:
                    user.set_password(new_user_pw)
                    user.save()

                    messages.success(request, '비밀번호 변경이 완료되었습니다.')
                    return redirect('accounts:login')

                else:
                    messages.error(request, '새로운 비밀번호가 서로 일치하지 않습니다.')
                    return redirect('accounts:passwordmodify')

        else:
            messages.error(request, '기존의 비밀번호가 일치하지 않습니다.')
            return redirect('accounts:passwordmodify')