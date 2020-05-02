# -*- coding: utf-8 -*-
from .common import *

@login_required
def post_createView(request):
    if request.method == "GET":
        return render(request, 'post_create.html')

    if request.method =="POST":
        user = request.user
        cursor = connection.cursor()

        # POST 내용 INSERT
        content = request.POST.get('content')
        post_img = request.FILES.get('post_img')
        hashtag = request.POST.get('hashtag')
        post_img_url = fileUpload(user, post_img)

        split_hashtag = hashtag.split(' ')

        insert_sql = "INSERT INTO post(user_id, content, post_img_src)"
        insert_sql += " VALUES ((%s) ,(%s), (%s))"

        result = cursor.execute(insert_sql, (user.username, content, post_img_url,))
        post_id = cursor.lastrowid


        # 해시태그 INSERT
        for i in range(len(split_hashtag)):
            # 이미 등록된 해시태그인지 확인
            inserted_hashtag = "SELECT COUNT(*)"
            inserted_hashtag += " FROM hashtag"
            inserted_hashtag += " WHERE keyword = (%s)"

            inserted_hashtag_result = cursor.execute(inserted_hashtag, (split_hashtag[i],))
            inserted_hashtag_datas = cursor.fetchall()

            if inserted_hashtag_datas[0][0] == 0:
                if '#' in split_hashtag[i]:

                    hashtag_sql = "INSERT INTO hashtag(keyword)"
                    hashtag_sql += " VALUES (%s)"

                    hashtag_result = cursor.execute(hashtag_sql, (split_hashtag[i],))
                    hashtag_id = cursor.lastrowid


                    # POST 해시태그 테이블 INSERT
                    post_hashtag_sql = "INSERT INTO post_hashtag(post_id, hashtag_id)"
                    post_hashtag_sql += " VALUES ((%s), (%s))"

                    post_hashtag_result = cursor.execute(post_hashtag_sql, (post_id, hashtag_id,))

            else:
                if '#' in split_hashtag[i]:
                    # 이미 존재하는 해시태그 아이디 가져오기
                    present_hashtag_sql = "SELECT hashtag_id"
                    present_hashtag_sql += " FROM hashtag"
                    present_hashtag_sql += " WHERE keyword = (%s)"

                    present_hashtag_result = cursor.execute(present_hashtag_sql, (split_hashtag[i],))
                    present_hashtag_datas = cursor.fetchall()

                    # POST 해시태그 테이블 INSERT
                    post_hashtag_sql = "INSERT INTO post_hashtag(post_id, hashtag_id)"
                    post_hashtag_sql += " VALUES ((%s), (%s))"

                    post_hashtag_result = cursor.execute(post_hashtag_sql, (post_id, present_hashtag_datas[0][0],))

        connection.commit()
        connection.close()


        return redirect('instagram:list', user.username)