# -*- coding: utf-8 -*-
# @Time    : 2021/3/17 15:52
# @FileName: verify.py
# @Author  : CNPolaris

import json
from rest_framework_jwt.serializers import jwt_decode_handler
from django.contrib.auth.models import User
from userprofile.models import Profile


def verify_permissions(request):
    """
    登录验证
    :param request: token
    :return: bool
    """
    token = request.GET.get('token',None)
    if token:
        toke_user = jwt_decode_handler(token)
        user_id = toke_user["user_id"]
        user = User.objects.get(id=user_id)

        if user:
            if Profile.objects.filter(user_id=user_id).exists():
                profile = Profile.objects.get(user_id=user_id)
                if request.method == 'GET':
                    request.params = request.GET

                # POST/PUT/DELETE 请求 参数从request对象的body属性中获取
                elif request.method in ['POST', 'PUT', 'DELETE']:
                    # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
                    request.params = json.loads(request.body)

                return True, request
        else:
            return False, request
    else:
        return False, request


def admin_permissions(request):
    """
    管理员管理
    :param request: token
    :return: bool
    """
    token = request.GET.get('token')
    toke_user = jwt_decode_handler(token)
    user_id = toke_user["user_id"]
    user = User.objects.get(id=user_id)

    if user.is_superuser:
        if Profile.objects.filter(user_id=user_id).exists():
            profile = Profile.objects.get(user_id=user_id)
            if profile.roles == 'admin' and profile.online == 1:
                if request.method == 'GET':
                    request.params = request.GET

                # POST/PUT/DELETE 请求 参数从request对象的body属性中获取
                elif request.method in ['POST', 'PUT', 'DELETE']:
                    # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
                    request.params = json.loads(request.body)

                return True, user, profile, request
    else:
        return True, request
