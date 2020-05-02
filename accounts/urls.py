from django.urls import re_path
from .splitViews import *
# Create your views here.

app_name = 'accounts'

urlpatterns = [
    re_path(r'^register/$', new_RegisterView, name='register'),
    re_path(r'^login/$', new_LoginView, name='login'),
    re_path(r'^logout/$', Logout, name='logout'),
    re_path(r'^modify/$', ModifyView, name='modify'),
    re_path(r'^passwordmodify/$', passwordModifyView, name='passwordmodify')
]