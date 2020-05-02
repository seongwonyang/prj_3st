from django.urls import re_path
from .splitViews import *
from django.conf import settings
from django.conf.urls.static import static
# Create your views here.

app_name = 'instagram'

urlpatterns = [
    re_path(r'^$', new_MainView, name='main'),
    re_path(r'^list/(?P<list>[ㄱ-힣a-zA-Z0-9-_.]*)/$', post_listView, name='list'),
    re_path(r'^detail/(?P<detail>\d+)/$', post_detailView, name='detail'),
    re_path(r'^create/$', post_createView, name='create'),
    re_path(r'^postmodify/(?P<postmodify>\d+)/$', post_modifyView, name='postmodify'),
    re_path(r'^postdelete/(?P<postdelete>\d+)/$', post_deleteView, name='postdelete'),
    re_path(r'^follow/(?P<follow>[ㄱ-힣a-zA-Z0-9-_.]*)/$', followingView, name='follow'),
    re_path(r'^like/(?P<post_id>\d+)/$', likeView, name='like'),
    re_path(r'^collection/(?P<post_id>\d+)/$', collectionView, name='collection'),
    re_path(r'^search/$', searchView, name='search'),

]

# DEBUG = TRUE일 때만 작동
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)