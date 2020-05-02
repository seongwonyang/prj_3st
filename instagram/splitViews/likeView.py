# -*- coding: utf-8 -*-
from .common import *

@login_required
def likeView(request, post_id):
    user = request.user

    cursor = connection.cursor()

    is_like = "SELECT COUNT(*)"
    is_like += " FROM like_post"
    is_like += " WHERE user_id = (%s) and post_id = (%s)"

    is_like_result = cursor.execute(is_like, (user.username, post_id))
    is_like_datas = cursor.fetchall()

    if is_like_datas[0][0] == 0:
        like_sql = "INSERT INTO like_post(post_id, user_id)"
        like_sql += " VALUES (%s, %s)"

        like_sql_result = cursor.execute(like_sql, (post_id, user.username))
        like_check = 1

    elif is_like_datas[0][0] == 1:
        unlike_sql = "DELETE"
        unlike_sql += " FROM like_post"
        unlike_sql += " WHERE user_id = (%s) AND post_id = (%s)"

        unlike_sql_result = cursor.execute(unlike_sql, (user.username, post_id,))
        like_check = 0

    like_count = "SELECT COUNT(user_id)"
    like_count += " FROM like_post"
    like_count += " WHERE post_id = (%s)"

    like_count_result = cursor.execute(like_count, (post_id,))
    like_count_datas = cursor.fetchall()
    likeCount = like_count_datas[0][0]

    connection.commit()
    connection.close()



    return HttpResponse(json.dumps({"like_check": like_check, "likeCount": likeCount}), content_type="application/json")