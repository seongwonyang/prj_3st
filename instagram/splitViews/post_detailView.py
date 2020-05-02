# -*- coding: utf-8 -*-
from .common import *

@login_required
def post_detailView(request, detail):
    user_id = request.user

    cursor = connection.cursor()

    detail_strSql = "SELECT user_id, post_img_src, content, time, post_id, profile_img_src"
    detail_strSql += " FROM post"
    detail_strSql += " LEFT OUTER JOIN accounts_user on accounts_user.username=post.user_id WHERE post_id = (%s)"

    restult = cursor.execute(detail_strSql, (detail,))
    datas = cursor.fetchall()

    profile_strSql = "SELECT instagram_2nd.accounts_user.profile_img_src"
    profile_strSql += " FROM instagram_2nd.accounts_user"
    profile_strSql += " WHERE instagram_2nd.accounts_user.username = (%s)"

    profile_result = cursor.execute(profile_strSql, (user_id,))
    profile_datas = cursor.fetchall()

    # 해당 포스트가 좋아요 되있는지
    is_like_sql = "SELECT COUNT(*)"
    is_like_sql += " FROM like_post"
    is_like_sql += " WHERE user_id = (%s) AND post_id = (%s)"

    is_like_result = cursor.execute(is_like_sql, (user_id.username, detail,))
    is_like_datas = cursor.fetchall()
    is_like = is_like_datas[0][0]

    # 해당 포스트가 콜렉션 되있는지
    is_collection_sql = "SELECT COUNT(*)"
    is_collection_sql += " FROM collection"
    is_collection_sql += " WHERE user_id = (%s) AND post_id = (%s)"

    is_collection_result = cursor.execute(is_collection_sql, (user_id.username, detail,))
    is_collection_datas = cursor.fetchall()
    is_collection = is_collection_datas[0][0]

    like_count = "SELECT COUNT(user_id)"
    like_count += " FROM like_post"
    like_count += " WHERE post_id = (%s)"

    like_count_result = cursor.execute(like_count, (detail,))
    like_count_datas = cursor.fetchall()

    # 해시태그 가져오기
    post_hashtag_sql = "SELECT keyword"
    post_hashtag_sql += " FROM hashtag"
    post_hashtag_sql += " LEFT OUTER JOIN post_hashtag on hashtag.hashtag_id = post_hashtag.hashtag_id"
    post_hashtag_sql += " WHERE post_id = (%s)"

    post_hashtag_sql_result = cursor.execute(post_hashtag_sql, (detail,))
    post_hashtag_sql_datas = cursor.fetchall()

    hashtag = []
    for i in range(len(post_hashtag_sql_datas)):
        hashtag.append(post_hashtag_sql_datas[i][0])

    connection.commit()
    connection.close()

    detail = {'user_id': datas[0][0],
              'post_img_src': datas[0][1],
              'content': datas[0][2],
              'time': datas[0][3],
              'post_id': datas[0][4],
              'profile_img_src': datas[0][5],
              'like_count': like_count_datas[0][0],
              'hashtag': hashtag}

    profile = {'profile_img_src': profile_datas[0][0]}


    return render(request, 'post_detail.html', {'detail':detail, 'profile':profile,
                                                'is_like': is_like, 'is_collection': is_collection, 'hashtag': hashtag})