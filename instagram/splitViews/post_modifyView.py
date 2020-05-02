# -*- coding: utf-8 -*-
from .common import *

@login_required
def post_modifyView(request, postmodify):

    if request.method == "GET":
        user = request.user

        cursor = connection.cursor()

        strSql = "SELECT post_img_src, content, post_id"
        strSql += " FROM post"
        strSql += " WHERE post_id = (%s)"

        result = cursor.execute(strSql, (postmodify,))
        datas = cursor.fetchall()

        # 해시태그 가져오기
        post_hashtag_sql = "SELECT keyword"
        post_hashtag_sql += " FROM hashtag"
        post_hashtag_sql += " LEFT OUTER JOIN post_hashtag on hashtag.hashtag_id = post_hashtag.hashtag_id"
        post_hashtag_sql += " WHERE post_id = (%s)"

        post_hashtag_sql_result = cursor.execute(post_hashtag_sql, (postmodify,))
        post_hashtag_sql_datas = cursor.fetchall()

        hashtag = []
        for i in range(len(post_hashtag_sql_datas)):
            hashtag.append(post_hashtag_sql_datas[i][0])

        hashtag_result = ' '.join(hashtag)

        connection.commit()
        connection.close()

        post = {'post_img_src': datas[0][0],
                'content': datas[0][1],
                'post_id': datas[0][2],
                'hashtag': hashtag_result}

        return render(request, 'post_modify.html', {'post': post})

    elif request.method == "POST":
        new_content = request.POST.get("content")
        new_hashtag = request.POST.get("hashtag")

        split_new_hashtag = new_hashtag.split(' ')

        cursor = connection.cursor()

        # 포스트 content 수정 삽입
        strSql = "UPDATE post"
        strSql += " SET content = (%s)"
        strSql += " WHERE post_id = (%s)"

        results = cursor.execute(strSql, (new_content, postmodify,))
        datas = cursor.fetchall()


        # 기존의 post_hashtag 삭제
        delete_post_hashtag = "DELETE"
        delete_post_hashtag += " FROM post_hashtag"
        delete_post_hashtag += " WHERE post_id = (%s)"

        delete_post_hashtag_result = cursor.execute(delete_post_hashtag, (postmodify,))

        for i in range(len(split_new_hashtag)):
            # 수정될 해시태그가 이미 테이블에 존재하는가
            inserted_hashtag = "SELECT COUNT(*)"
            inserted_hashtag += " FROM hashtag"
            inserted_hashtag += " WHERE keyword = (%s)"

            inserted_hashtag_result = cursor.execute(inserted_hashtag, (split_new_hashtag[i],))
            inserted_hashtag_datas = cursor.fetchall()

            if inserted_hashtag_datas[0][0] == 0:
                if '#' in split_new_hashtag[i]:

                    hashtag_sql = "INSERT INTO hashtag(keyword)"
                    hashtag_sql += " VALUES (%s)"

                    hashtag_result = cursor.execute(hashtag_sql, (split_new_hashtag[i],))
                    hashtag_id = cursor.lastrowid

                    # POST 해시태그 테이블 INSERT
                    post_hashtag_sql = "INSERT INTO post_hashtag(post_id, hashtag_id)"
                    post_hashtag_sql += " VALUES ((%s), (%s))"

                    post_hashtag_result = cursor.execute(post_hashtag_sql, (postmodify, hashtag_id,))

            else:
                if '#' in split_new_hashtag[i]:
                    # 이미 존재하는 해시태그 아이디 가져오기
                    present_hashtag_sql = "SELECT hashtag_id"
                    present_hashtag_sql += " FROM hashtag"
                    present_hashtag_sql += " WHERE keyword = (%s)"

                    present_hashtag_result = cursor.execute(present_hashtag_sql, (split_new_hashtag[i],))
                    present_hashtag_datas = cursor.fetchall()

                    # POST 해시태그 테이블 INSERT
                    post_hashtag_sql = "INSERT INTO post_hashtag(post_id, hashtag_id)"
                    post_hashtag_sql += " VALUES ((%s), (%s))"

                    post_hashtag_result = cursor.execute(post_hashtag_sql, (postmodify, present_hashtag_datas[0][0],))

        connection.commit()
        connection.close()

        return redirect('instagram:detail', postmodify)
