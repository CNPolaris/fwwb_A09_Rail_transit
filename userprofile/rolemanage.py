# -*- coding: utf-8 -*-
# @Time    : 2021/3/19 22:41
# @FileName: rolemanage.py
# @Author  : CNPolaris

from django.contrib.auth.models import User
from userprofile.models import Profile
from django.http import JsonResponse

from units.verify import admin_permissions


def RoleManage(request):
    """
    用户权限管理 superuser才能实现的业务
    :param request: /api/role/manage
    :return: json
    """
    flag, user, profile, request = admin_permissions(request)
    context = {}
    if flag:
        User_querySet = User.objects.values('id', 'username', 'is_superuser', 'profile__roles', 'profile__online',
                                            'email', 'last_login', 'is_active')
        user_list = list(User_querySet)
        context['code'] = 2000
        context['data'] = user_list
    else:
        context['code'] = 1000
        context['message'] = "非管理员无法操作"
    return JsonResponse(context)


def create_new_user(request):
    """
    创建新的用户
    :param request: /api/role/create
    :return: json
    """
    return None


def list_role(request):
    """
    获取所有用户的权限列表
    :param request: /api/role/list
    :return: json
    """
    flag, user, profile, request = admin_permissions(request)
    context = {}
    if flag:
        User_querySet = User.objects.values('id', 'username', 'profile__roles', 'is_active')
        user_list = list(User_querySet)
        context['code'] = 2000
        context['data'] = user_list
    else:
        context['code'] = 1000
        context['message'] = "非管理员无法操作"

    return JsonResponse(context)


def modify_user_role(request):
    """
    修改用户权限
    :param request: POST/api/role/update
    :return:
    """
    flag, user, profile, request = admin_permissions(request)
    context = {}
    if flag:
        uid = request.params.get('id')
        role = request.params.get('role')
        user = User.objects.get(id=uid)
        user.profile.roles = role
        user.save()
        context['code'] = 2000
        context['message'] = '权限修改成功'
    else:
        context['code'] = 1000
        context['message'] = "非管理员无法操作"

    return JsonResponse(context)


def offline(request):
    """
    强制用户下线
    :param request: /api/role/off
    :return: json
    """
    flag, user, profile, request = admin_permissions(request)
    context = {}
    if flag:
        uid = request.params.get('id')
        active = request.params.get('active')
        user = User.objects.get(id=uid)
        user.is_active = active
        user.save()
        context['code'] = 2000
        context['message'] = '权限修改成功'
    else:
        context['code'] = 1000
        context['message'] = "非管理员无法操作"

    return JsonResponse(context)


def modify_user_info(request):
    """
    修改用户的信息
    :param request: /api/role/info
    :return: json
    """
    flag, user, profile, request = admin_permissions(request)
    context = {}
    if flag:
        uid = request.params.get('id')
        user_name = request.params.get('username')
        email = request.params.get('email')
        introduction = request.params.get('introduction')

        user = User.objects.get(id=uid)

        user.username = user_name
        user.email = email
        user.profile.introduction = introduction

        user.save()
        context['code'] = 2000
        context['message'] = '权限修改成功'
    else:
        context['code'] = 1000
        context['message'] = "非管理员无法操作"

    return JsonResponse(context)
