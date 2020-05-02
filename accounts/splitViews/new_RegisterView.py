# -*- coding: utf-8 -*-
from .common import *

def new_RegisterView(request):
    cursor = connection.cursor()

    base_sql = "SELECT profile_img_src"
    base_sql += " FROM accounts_user"
    base_sql += " WHERE username = 'base'"

    base_sql_result = cursor.execute(base_sql)
    base_sql_data = cursor.fetchall()

    connection.commit()
    connection.close()

    if request.method == "GET":
        return render(request, 'signup.html')

    elif request.method == "POST":
        email = request.POST.get("e_mail")
        name = request.POST.get("name")
        user_id = request.POST.get("user_id")
        user_pw = request.POST.get("user_pw")
        profile_img_src = base_sql_data[0][0]


        try:
            user = User.objects.get(username=user_id)
            messages.error(request, '이미 존재하는 아이디입니다.')

            return redirect('accounts:register')

        except ObjectDoesNotExist:
            user2 = User.objects.create_user(email=email, username=user_id, first_name=name, password=user_pw, profile_img_src = profile_img_src)
            messages.success(request, '회원가입에 성공하였습니다.')

            return redirect('accounts:login')








