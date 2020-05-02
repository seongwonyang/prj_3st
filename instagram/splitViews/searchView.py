# -*- coding: utf-8 -*-
from .common import *

@login_required
def searchView(request):
    cursor = connection.cursor()

    keyword = request.GET.get("keyword")

    if '#' not in keyword:
        keyword = '#' + keyword[0:]



    search_sql = "SELECT post_id, post_hashtag.hashtag_id"
    search_sql += " FROM post_hashtag"
    search_sql += " LEFT OUTER JOIN hashtag on hashtag.hashtag_id = post_hashtag.hashtag_id"
    search_sql += " WHERE keyword = (%s)"

    search_sql_result = cursor.execute(search_sql, (keyword,))
    search_sql_datas = cursor.fetchall()

    # 검색된 해시태그 게시물 count
    count_sql = "SELECT COUNT(post_id)"
    count_sql += " FROM post_hashtag"
    count_sql += " WHERE hashtag_id = (%s)"

    count_sql_result = cursor.execute(count_sql, (search_sql_datas[0][1],))
    count_sql_datas = cursor.fetchall()

    if len(search_sql_datas) != 0:
        search = []
        for search_sql_data in search_sql_datas:
            # 검색결과 포스팅 이미지
            search_result_sql = "SELECT post_img_src"
            search_result_sql += " FROM post"
            search_result_sql += " WHERE post_id = (%s)"

            search_result_sql_result = cursor.execute(search_result_sql, (search_sql_data[0],))
            search_result_datas = cursor.fetchall()

            row = {'post_img_src': search_result_datas[0][0]
                   }

            search.append(row)
    else:
        return render(request, 'search.html')

    return render(request, 'search.html', {"search": search, "keyword": keyword, 'count':count_sql_datas[0][0]})