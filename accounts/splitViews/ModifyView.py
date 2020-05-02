# -*- coding: utf-8 -*-
from .common import *

@login_required
def ModifyView(request):
    if request.method == 'GET':
        return render(request, 'user_info_modify.html')

    elif request.method == 'POST':
        user = request.user

        profile_img_file = request.FILES.get('profile_img_file')
        profile_msg = request.POST.get('profile_msg')
        email = request.POST.get('email')
        name = request.POST.get('name')

        if profile_img_file is None:
            profile_img_url = user.profile_img_src
        else:
            profile_img_url = fileUpload(user, profile_img_file)

        user.profile_img_src = profile_img_url
        user.profile_msg = profile_msg
        user.email = email
        user.first_name = name

        user.save()


        return redirect('instagram:list', user.username)


