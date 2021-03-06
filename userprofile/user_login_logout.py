# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 10:49
# @FileName: user_login_logout.py
# @Author  : CNPolaris
import json

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_decode_handler
from rest_framework_jwt.settings import api_settings


# Create your views here.
from userprofile.models import Profile


def user_login(request):
    """
    登录处理
    :param request: POST
    :return: json
    """
    if request.method == 'POST':
        request.params = json.loads(request.body)
        username = request.params.get('username')
        password = request.params.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.is_superuser:
                    login(request, user)
                    request.session['usertype'] = 'admin'

                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)

                    return JsonResponse({'code': 2000, "data": {'token': token}})
                else:
                    login(request, user)
                    request.session['usertype'] = 'user'

                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)

                    return JsonResponse({'code': 2000, "data": {'token': token}})
            else:
                return JsonResponse({'code': 1000, 'message': '用户已经被禁用'})
        else:
            return JsonResponse({'code': 1000, 'message': '用户名或者密码错误'})


def user_logout(request):
    logout(request)
    return JsonResponse({'ret': 2000})


def get_user_info(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        if token:
            toke_user = []
            toke_user = jwt_decode_handler(token)
            user_id = toke_user["user_id"]
            user = User.objects.get(id=user_id)
            if user:
                if Profile.objects.filter(user_id=user_id).exists():
                    profile = Profile.objects.get(user_id=user_id)
                else:
                    profile = Profile.objects.create(user=user)
                context = {
                    'code': 2000,
                    'data': {
                        'username': user.username,
                        'roles': profile.roles,
                        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                        'introduction': profile.introduction,
                    }
                }
                return JsonResponse(context)
            else:
                return JsonResponse({'code': 1000, 'message': '无访问权限'})

        else:
            return JsonResponse({'code': 1000, 'message': '无访问权限'})
