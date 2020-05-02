# -*- coding: utf-8 -*-
from .common import *


@login_required
def collectionView(request, post_id):
    user = request.user

    cursor = connection.cursor()

    is_collection = "SELECT COUNT(*)"
    is_collection += " FROM collection"
    is_collection += " WHERE user_id = (%s) AND post_id = (%s)"

    is_collection_result = cursor.execute(is_collection, (user.username, post_id))
    is_collection_datas = cursor.fetchall()

    if is_collection_datas[0][0] == 0:
        collection_sql = "INSERT INTO collection(post_id, user_id)"
        collection_sql += "VALUES ((%s), (%s))"

        collection_sql_result = cursor.execute(collection_sql, (post_id, user.username,))
        collection_check = 1

    elif is_collection_datas[0][0] == 1:
        uncollection_sql = "DELETE"
        uncollection_sql += " FROM collection"
        uncollection_sql += " WHERE user_id = (%s) AND post_id = (%s)"

        uncollection_sql_result = cursor.execute(uncollection_sql, (user.username, post_id,))
        collection_check = 0

    return HttpResponse(json.dumps({"collection_check": collection_check}), content_type="application/json")