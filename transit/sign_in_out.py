# -*- coding: utf-8 -*-
# @Time    : 2021/2/18 13:14
# @FileName: sign_in_out.py
# @Author  : CNPolaris
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout


def signin(request):
    """
    登录处理
    :param request: POST
    :return: json
    """
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            if user.is_superuser:
                login(request, user)
                request.session['usertype'] = 'admin'
                return JsonResponse({'ret': 0})
            else:
                login(request, user)
                request.session['usertype'] = 'user'
                return JsonResponse({'ret': 0})
        else:
            return JsonResponse({'ret': 1, 'msg': '用户已经被禁用'})
    else:
        return JsonResponse({'ret': 1, 'msg': '用户名或者密码错误'})


def signout(request):
    logout(request)
    return JsonResponse({'ret': 0})
