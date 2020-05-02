# -*- coding: utf-8 -*-
from .common import *

@login_required
def post_deleteView(request, postdelete):
    user = request.user

    cursor = connection.cursor()

    strSql = "DELETE"
    strSql += " FROM post"
    strSql += " WHERE post_id = (%s)"

    result = cursor.execute(strSql, (postdelete,))

    #삭제될 게시물과 연결된 해시태그가 있는가
    post_hashtag = "SELECT post_id"
    post_hashtag += " FROM post_hashtag"
    post_hashtag += " WHERE post_id = (%s)"

    post_hashtag_result = cursor.execute(post_hashtag, (postdelete,))
    post_hashtag_datas = cursor.fetchall()

    if len(post_hashtag_datas) !=0 :
        delete_post_hashtag = "DELETE"
        delete_post_hashtag += " FROM post_hashtag"
        delete_post_hashtag += " WHERE post_id = (%s)"

        delete_post_hashtag_result = cursor.execute(delete_post_hashtag, (postdelete,))

    connection.commit()
    connection.close()

    return redirect('instagram:list', user.username)