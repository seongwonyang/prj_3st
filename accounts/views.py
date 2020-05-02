#
#
# from django.shortcuts import render, get_object_or_404, redirect
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib import messages
#
# import string
# import random
# import hashlib
# import base64
# from django.contrib.auth.hashers import pbkdf2
#
# @csrf_exempt
#
# def hashing_password(user_pw):
#     count = random.randint(16, 21)
#     string_pool = string.ascii_letters + string.digits + string.punctuation
#     salt = "".join(random.choices(string_pool, k=count))
#
#     hash = pbkdf2(user_pw, salt, 10000, digest=hashlib.sha256)
#     hashed_pw = base64.b64encode(hash).decode('ascii').strip()
#
#     return salt, hashed_pw
#
#
# def log_password(user_pw,salt):
#     hash = pbkdf2(user_pw, salt, 10000, digest=hashlib.sha256)
#     hashed_pw = base64.b64encode(hash).decode('ascii').strip()
#
#     return hashed_pw
#
# def RegisterView(request):
#     if request.method == "GET":
#         return render(request, 'signup.html')
#
#     elif request.method == "POST":
#         email = request.POST.get("e_mail")
#         name = request.POST.get("name")
#         user_id = request.POST.get("user_id")
#         user_pw = request.POST.get("user_pw")
#         salt, hashed_pw = hashing_password(user_pw)
#
#         cursor = connection.cursor()
#
#         strSql = "SELECT instagram.user.user_id"
#         strSql += " FROM instagram.user"
#         strSql += " WHERE user_id = (%s)"
#
#         result = cursor.execute(strSql, (user_id,))
#         datas = cursor.fetchall()
#
#         connection.commit()
#         connection.close()
#
#         if len(datas) > 0:
#             connection.rollback()
#             print("이미 존재하는 아이디입니다.")
#
#             messages.error(request, '이미 존재하는 아이디입니다.')
#
#             return redirect('/register')
#
#         elif len(datas)==0:
#             cursor = connection.cursor()
#
#             insert_sql = "INSERT INTO instagram.user(e_mail, name, user_id, user_pw, salt)"
#             insert_sql += " VALUES ((%s), (%s), (%s), (%s), (%s))"
#
#             insert_result = cursor.execute(insert_sql, (email, name, user_id, hashed_pw, salt,))
#             insert_datas = cursor.fetchall()
#
#             connection.commit()
#             connection.close()
#
#             messages.success(request, '회원가입에 성공하셨습니다.')
#
#             return redirect('/login')
#
#
# def LoginView(request):
#     if request.method == "GET":
#         return render(request, 'login.html')
#
#     elif request.method == "POST":
#         user_id= request.POST.get('user_id')
#         user_pw= request.POST.get('user_pw')
#         salt, hashed_pw = hashing_password(user_pw)
#
#         cursor = connection.cursor()
#
#         strSql = "SELECT instagram.user.user_id"
#         strSql += " FROM instagram.user"
#         strSql += " WHERE user_id = (%s)"
#
#         result = cursor.execute(strSql, (user_id,))
#         datas = cursor.fetchall()
#
#         connection.commit()
#         connection.close()
#
#         if len(datas) == 0:
#             connection.rollback()
#             print("로그인 실패")
#
#             messages.error(request, '아이디 혹은 비밀번호를 확인해주세요.')
#
#             return redirect('/login')
#
#         elif len(datas) !=0:
#             cursor = connection.cursor()
#
#             pw_strSql = "SELECT instagram.user.user_pw, instagram.user.salt"
#             pw_strSql += " FROM instagram.user"
#             pw_strSql += " WHERE user_id = (%s)"
#
#             pw_result = cursor.execute(pw_strSql, (user_id,))
#             pw_datas = cursor.fetchall()
#
#             log_pw = log_password(user_pw, pw_datas[0][1])
#
#             log_pw_strSql = "SELECT instagram.user.user_pw"
#             log_pw_strSql += " FROM instagram.user"
#             log_pw_strSql += " WHERE user_pw = (%s)"
#
#             log_pw_result = cursor.execute(log_pw_strSql, (log_pw,))
#             log_pw_datas = cursor.fetchall()
#
#             connection.commit()
#             connection.close()
#
#             if len(log_pw_datas) == 0:
#                 connection.rollback()
#                 print("로그인 실패")
#
#                 messages.error(request, '아이디 혹은 비밀번호를 확인해주세요.')
#
#                 return redirect('/login')
#
#             elif len(log_pw_datas) !=0:
#                 request.session['user_id'] = user_id
#                 return redirect('/')
#
#
# def MainView(request):
#     inSession = request.session.get('user_id', False)
#
#     if inSession is not False:
#         render_page = "main.html"
#         return  render(request, render_page, {'user_id': inSession})
#     else:
#         return render(request, 'login.html')
