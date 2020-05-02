from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    # 기존의 accounts url 연결
    re_path(r'^accounts/', include('accounts.urls')),
    # 추가한 accounts url 연결
    re_path(r'^accounts/', include('allauth.urls')),

    re_path(r'^', include('instagram.urls')),
]