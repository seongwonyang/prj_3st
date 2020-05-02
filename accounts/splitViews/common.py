# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
import os
import uuid

import string
import random
import hashlib
import base64
from django.contrib.auth.hashers import pbkdf2

def hashing_password(user_pw):
    count = random.randint(16, 21)
    string_pool = string.ascii_letters + string.digits + string.punctuation
    salt = "".join(random.choices(string_pool, k=count))

    hash = pbkdf2(user_pw, salt, 10000, digest=hashlib.sha256)
    hashed_pw = base64.b64encode(hash).decode('ascii').strip()

    return salt, hashed_pw


def log_password(user_pw,salt):
    hash = pbkdf2(user_pw, salt, 10000, digest=hashlib.sha256)
    hashed_pw = base64.b64encode(hash).decode('ascii').strip()

    return hashed_pw

def fileUpload(user, postImg):
    # 파일 이름과 확장자를 분리
    fileName, extension = os.path.splitext(postImg.name)

    newFileName = str(uuid.uuid4()) + extension
    # ex) image/1111/51dc6889-448c-4dff-a685-3372acd78c9d.jpg
    filePath = os.path.join('image', user.username, newFileName)

    # 사진 파일을 지정된 경로에 저장
    default_storage.save(filePath, postImg)
    # 저장된 파일의 경로 가져오기
    post_img_url = default_storage.url(filePath)

    return post_img_url