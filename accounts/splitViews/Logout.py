# -*- coding: utf-8 -*-
from .common import *

def Logout(request):
    logout(request)
    return redirect('accounts:login')