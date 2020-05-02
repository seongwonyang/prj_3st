# -*- coding: utf-8 -*-
from .common import *

def RegisterView(request):
    if request.method == "GET":
        return render(request, 'signup.html')

    elif request.method == "POST":
        email = request.POST.get("e_mail")
        name = request.POST.get("name")
        user_id = request.POST.get("user_id")
        user_pw = request.POST.get("user_pw")
        salt, hashed_pw = hashing_password(user_pw)

        cursor = connection.cursor()

        strSql = "SELECT instagram.user.user_id"
        strSql += " FROM instagram.user"
        strSql += " WHERE user_id = (%s)"

        result = cursor.execute(strSql, (user_id,))
        datas = cursor.fetchall()

        connection.commit()
        connection.close()

        if len(datas) > 0:
            connection.rollback()
            print("이미 존재하는 아이디입니다.")

            messages.error(request, '이미 존재하는 아이디입니다.')

            return redirect('/register')

        elif len(datas)==0:
            cursor = connection.cursor()

            insert_sql = "INSERT INTO instagram.user(e_mail, name, user_id, user_pw, salt)"
            insert_sql += " VALUES ((%s), (%s), (%s), (%s), (%s))"

            insert_result = cursor.execute(insert_sql, (email, name, user_id, hashed_pw, salt,))
            insert_datas = cursor.fetchall()

            connection.commit()
            connection.close()

            messages.success(request, '회원가입에 성공하셨습니다.')

            return redirect('/login')
