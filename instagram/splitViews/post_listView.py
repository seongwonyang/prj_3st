# -*- coding: utf-8 -*-
from .common import *

def post_listView(request, list):
    user_id = request.user

    cursor = connection.cursor()

    strSql = "SELECT post_img_src, user_id, post_id"  #클릭된 유저의 포스팅
    strSql += " FROM post"
    strSql += " WHERE user_id = (%s)"
    strSql += " ORDER BY time DESC"

    result = cursor.execute(strSql,(list,))
    datas = cursor.fetchall()

    post_count = "SELECT COUNT(post_id)"   #클릭된 유저의 포스팅 개수
    post_count += " FROM post"
    post_count += " WHERE user_id = (%s)"

    post_count_result = cursor.execute(post_count, (list,))
    post_count_datas = cursor.fetchall()

    following_count = "SELECT COUNT(following_id)"  # 클릭된 유저의 팔로워 수
    following_count += " FROM following"
    following_count += " WHERE user_id = (%s)"

    following_count_result = cursor.execute(following_count, (list,))
    following_count_datas = cursor.fetchall()

    name_strSql = "SELECT username, profile_img_src, profile_msg"
    name_strSql += " FROM accounts_user"   #클릭된 유저의 프로필 정보
    name_strSql += " WHERE username = (%s)"

    name_result = cursor.execute(name_strSql,(list,))
    name_datas = cursor.fetchall()

    follow_button = "SELECT COUNT(*)" #팔로우 유뮤에 따른 버튼 보여주기
    follow_button += " FROM following"
    follow_button += " WHERE user_id = (%s) AND following_id = (%s)"

    follow_button_result = cursor.execute(follow_button, (user_id.username, list))
    follow_button_datas = cursor.fetchall()

    follower_count_sql = "SELECT COUNT(user_id)" #클릭된 유저의 팔로잉 수
    follower_count_sql += " FROM following"
    follower_count_sql += " WHERE following_id = (%s)"

    follower_count_result = cursor.execute(follower_count_sql, (list,))
    follower_count_datas = cursor.fetchall()

    following_list = "SELECT profile_msg, profile_img_src, following_id, user_id" #클릭된 유저의 팔로잉 유저 목록
    following_list += " FROM accounts_user"
    following_list += " LEFT OUTER JOIN following on accounts_user.username = following.following_id"
    following_list += " WHERE following.user_id = (%s)"

    following_list_result = cursor.execute(following_list, (list,))
    following_list_datas = cursor.fetchall()

    follower_list = "SELECT profile_msg, profile_img_src, user_id, following_id"  # 클릭된 유저의 팔로워 유저 목록
    follower_list += " FROM accounts_user"
    follower_list += " LEFT OUTER JOIN following on accounts_user.username = following.user_id"
    follower_list += " WHERE following.following_id = (%s)"

    follower_list_result = cursor.execute(follower_list, (list,))
    follower_list_datas = cursor.fetchall()

    following_list_button = "SELECT user_id, following_id"
    following_list_button += " FROM following"

    following_list_button_result = cursor.execute(following_list_button)
    following_list_button_datas = cursor.fetchall()

    user_name = {'user_id':name_datas[0][0],
                 'profile_img_src':name_datas[0][1],
                 'profile_msg':name_datas[0][2]}

    post_count_tuple = {'post_count':post_count_datas[0][0]}

    following_count_tuple = {'following_count': following_count_datas[0][0]}

    follow_button_tuple = {'follow_button': follow_button_datas[0][0]}

    follower_count_tuple = {'follower_count': follower_count_datas[0][0]}

    following_list_tuple = []
    for following_list_data in following_list_datas:
        follow_button = "SELECT COUNT(*)"
        follow_button += " FROM following"
        follow_button += " WHERE user_id = (%s) AND following_id = (%s)"

        follow_button_result = cursor.execute(follow_button, (user_id.username, following_list_data[2],))
        follow_button_datas = cursor.fetchall()

        if follow_button_datas[0][0] == 0:
            is_follow = 0
        else:
            is_follow = 1

        row = {'profile_msg' : following_list_data[0],
               'profile_img_src' : following_list_data[1],
               'following_id' : following_list_data[2],
               'user_id' : following_list_data[3],
               'is_follow' : is_follow
               }
        following_list_tuple.append(row)

    follower_list_tuple = []
    for follower_list_data in follower_list_datas:
        follow_button = "SELECT COUNT(*)"
        follow_button += " FROM following"
        follow_button += " WHERE user_id = (%s) AND following_id = (%s)"

        follow_button_result = cursor.execute(follow_button, (user_id.username, follower_list_data[2],))
        follow_button_datas = cursor.fetchall()

        if follow_button_datas[0][0] == 0:
            is_follow = 0
        else:
            is_follow = 1

        row = {'profile_msg' : follower_list_data[0],
               'profile_img_src' : follower_list_data[1],
               'user_id' : follower_list_data[2],
               'following_id' : follower_list_data[3],
               'is_follow' : is_follow}
        follower_list_tuple.append(row)

    list= []
    for data in datas:
        row = {'post_img_src': data[0],
               'user_id': data[1],
               'post_id': data[2]}
        list.append(row)


    # 콜렉션 리스트
    collection_list_sql = "SELECT post.post_id, post_img_src"
    collection_list_sql += " FROM post"
    collection_list_sql += " LEFT OUTER JOIN collection on collection.post_id = post.post_id"
    collection_list_sql += " WHERE collection.user_id = (%s)"
    collection_list_sql += " ORDER BY post.time DESC"

    collection_list_result = cursor.execute(collection_list_sql, (user_id.username,))
    collection_list_datas = cursor.fetchall()

    collection_list = []
    for data in collection_list_datas:
        row = {'post_id': data[0],
               'post_img_src': data[1]}
        collection_list.append(row)

    connection.commit()
    connection.close()

    return render(request, 'post_list.html',{'list':list, 'user_name': user_name, 'post_count_tuple': post_count_tuple,
                                             'following_count_tuple': following_count_tuple,
                                             'follow_button_tuple': follow_button_tuple, 'follower_count_tuple': follower_count_tuple,
                                             'following_list': following_list_tuple, 'follower_list': follower_list_tuple,
                                             'collection_list': collection_list})