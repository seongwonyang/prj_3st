# -*- coding: utf-8 -*-
from .common import *

def MainView(request):
    inSession = request.session.get('username', False)

    if inSession is not False:
        render_page = "main.html"
        return render(request, render_page, {'user_id': inSession})
    else:
        return render(request, 'login.html')