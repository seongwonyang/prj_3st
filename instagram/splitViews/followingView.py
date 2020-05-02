# -*- coding: utf-8 -*-
from .common import *

@login_required
def followingView(request, follow):
    user = request.user
    cursor = connection.cursor()

    follow_button = "SELECT COUNT(*)"  # 방문된 유저가 로그인된 유저에게 팔로우가 되있는지 구분
    follow_button += " FROM following"
    follow_button += " WHERE user_id = (%s) AND following_id = (%s)"

    follow_button_result = cursor.execute(follow_button, (user.username, follow,))
    follow_button_datas = cursor.fetchall()

    if follow_button_datas[0][0] == 0:
        following_sql = "INSERT INTO following(user_id, following_id) "
        following_sql += " VALUES ((%s), (%s))"

        following_result = cursor.execute(following_sql, (user.username, follow,))
        is_follow = 0

    elif follow_button_datas[0][0] == 1:
        unfollowing_sql = "DELETE"
        unfollowing_sql += " FROM following"
        unfollowing_sql += " WHERE user_id = (%s) AND following_id = (%s)"

        unfollowing_result = cursor.execute(unfollowing_sql, (user.username, follow,))
        is_follow = 1

    follower_count_sql = "SELECT COUNT(user_id)"  # 타인의 팔로워 수 카운트
    follower_count_sql += " FROM following"
    follower_count_sql += " WHERE following_id = (%s)"

    follower_count_result = cursor.execute(follower_count_sql, (follow,))
    follower_count_datas = cursor.fetchall()
    followerCount = follower_count_datas[0][0]

    my_follower_count_sql = "SELECT COUNT(user_id)"  # 나의 팔로워 수 카운트
    my_follower_count_sql += " FROM following"
    my_follower_count_sql += " WHERE following_id = (%s)"

    my_follower_count_result = cursor.execute(my_follower_count_sql, (user.username,))
    my_follower_count_datas = cursor.fetchall()
    my_followerCount = my_follower_count_datas[0][0]



    following_count_sql = "SELECT COUNT(following_id)"  # 팔로잉 수 카운트
    following_count_sql += " FROM following"
    following_count_sql += " WHERE user_id = (%s)"

    following_count_result = cursor.execute(following_count_sql, (user.username,))
    following_count_datas = cursor.fetchall()
    followingCount = following_count_datas[0][0]

    connection.commit()
    connection.close()

    current_url = request.POST.get('current_url')
    current_url = current_url.split('/')


    return HttpResponse(json.dumps({"is_follow":is_follow , "followerCount": followerCount,
                                    "followingCount": followingCount, "list_page_user": current_url[4],
                                    "my_followerCount": my_followerCount, "user": user.username}), content_type="application/json")