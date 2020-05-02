# -*- coding: utf-8 -*-
from .common import *

@login_required
def new_MainView(request):
    user = request.user

    cursor = connection.cursor()

    # 우측 상단 로그인된 유저 정보
    strSql= "SELECT user_id, post_img_src, content, time, profile_img_src, post_id"
    strSql += " FROM post"
    strSql += " LEFT OUTER JOIN accounts_user on post.user_id=accounts_user.username WHERE user_id IN (SELECT following_id FROM following WHERE user_id = (%s))"
    strSql += " OR user_id = (%s)"
    strSql += " ORDER BY time DESC"

    result = cursor.execute(strSql,(user, user,))
    datas = cursor.fetchall()

    # 우측 상단 로그인된 유저 정보
    myname_strsql = "SELECT username, profile_img_src"
    myname_strsql += " FROM accounts_user"
    myname_strsql += " WHERE username = (%s)"

    result2 = cursor.execute(myname_strsql,(user,))
    datas2 = cursor.fetchall()

    myname = {'user_id':datas2[0][0],
              'profile_img_src':datas2[0][1]}

    cate=[]
    for data in datas:

        #좋아요 개수 카운트
        like_count = "SELECT COUNT(user_id)"
        like_count += " FROM like_post"
        like_count += " WHERE post_id = (%s)"

        like_count_result = cursor.execute(like_count, (data[5],))
        like_count_datas = cursor.fetchall()

        #로그인된 유저가 좋아요를 눌렀는지 판단
        is_like = "SELECT user_id, post_id"
        is_like += " FROM like_post"
        is_like += " WHERE user_id = (%s) and post_id = (%s)"

        is_like_result = cursor.execute(is_like, (user.username, data[5]))
        is_like_datas = cursor.fetchall()

        #로그인된 유저가 포스팅을 북마크 했는지 판단
        is_collection = "SELECT user_id, post_id"
        is_collection += " FROM collection"
        is_collection += " WHERE user_id = (%s) AND post_id = (%s)"

        is_collection_result = cursor.execute(is_collection, (user.username, data[5],))
        is_collection_datas = cursor.fetchall()

        #해시태그 가져오기
        post_hashtag_sql = "SELECT keyword"
        post_hashtag_sql += " FROM hashtag"
        post_hashtag_sql += " LEFT OUTER JOIN post_hashtag on hashtag.hashtag_id = post_hashtag.hashtag_id"
        post_hashtag_sql += " WHERE post_id = (%s)"

        post_hashtag_sql_result = cursor.execute(post_hashtag_sql, (data[5],))
        post_hashtag_sql_datas = cursor.fetchall()

        hashtag = []
        for i in range(len(post_hashtag_sql_datas)):
            hashtag.append(post_hashtag_sql_datas[i][0])

        row = {'user_id':data[0],
               'post_img_src':data[1],
               'post_content':data[2],
               'post_time':data[3],
               'profile_img_src':data[4],
               'post_id':data[5],
               'like_count':like_count_datas[0][0],
               'is_like': len(is_like_datas),
               'is_collection': len(is_collection_datas),
               'hashtag': hashtag
               }
        cate.append(row)


    connection.commit()
    connection.close()

    if len(cate) == 0:
        messages.success(request, '새로운 포스트를 작성하거나 다른 사람들 팔로우 해보세요!')
        return  render(request, 'main.html')


    return render(request, 'main.html', {'cate':cate, 'myname': myname, 'hashtag': hashtag})