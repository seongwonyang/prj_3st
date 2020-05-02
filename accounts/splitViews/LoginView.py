# -*- coding: utf-8 -*-
from .common import *

def LoginView(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        user_id= request.POST.get('user_id')
        user_pw= request.POST.get('user_pw')
        salt, hashed_pw = hashing_password(user_pw)

        cursor = connection.cursor()

        strSql = "SELECT instagram.user.user_id"
        strSql += " FROM instagram.user"
        strSql += " WHERE user_id = (%s)"

        result = cursor.execute(strSql, (user_id,))
        datas = cursor.fetchall()

        connection.commit()
        connection.close()

        if len(datas) == 0:
            connection.rollback()
            print("로그인 실패")

            messages.error(request, '아이디 혹은 비밀번호를 확인해주세요.')

            return redirect('/login')

        elif len(datas) !=0:
            cursor = connection.cursor()

            pw_strSql = "SELECT instagram.user.user_pw, instagram.user.salt"
            pw_strSql += " FROM instagram.user"
            pw_strSql += " WHERE user_id = (%s)"

            pw_result = cursor.execute(pw_strSql, (user_id,))
            pw_datas = cursor.fetchall()

            log_pw = log_password(user_pw, pw_datas[0][1])

            log_pw_strSql = "SELECT instagram.user.user_pw"
            log_pw_strSql += " FROM instagram.user"
            log_pw_strSql += " WHERE user_pw = (%s)"

            log_pw_result = cursor.execute(log_pw_strSql, (log_pw,))
            log_pw_datas = cursor.fetchall()

            connection.commit()
            connection.close()

            if len(log_pw_datas) == 0:
                connection.rollback()
                print("로그인 실패")

                messages.error(request, '아이디 혹은 비밀번호를 확인해주세요.')

                return redirect('/login')

            elif len(log_pw_datas) !=0:
                request.session['user_id'] = user_id
                return redirect('/')
