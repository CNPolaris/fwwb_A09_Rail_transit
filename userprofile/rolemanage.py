# -*- coding: utf-8 -*-
# @Time    : 2021/3/19 22:41
# @FileName: rolemanage.py
# @Author  : CNPolaris

from django.contrib.auth.models import User
from userprofile.models import Profile
from django.http import JsonResponse
from django.core.paginator import Paginator
from units.verify import admin_permissions


def get_params_role(request):
    """
    解析请求参数
    :param request:
    :return: dict
    """
    query_dict = {}
    uid = request.params.get('id', None)
    if uid:
        query_dict['id'] = uid
    username = request.params.get('username', None)
    if username:
        query_dict['username'] = username
    is_superuser = request.params.get('is_superuser', None)
    if is_superuser:
        query_dict['is_superuser'] = is_superuser
    profile__roles = request.params.get('profile__roles', None)
    if profile__roles:
        query_dict['profile__roles'] = profile__roles
    profile__online = request.params.get('profile__online', None)
    if profile__online:
        query_dict['profile__online'] = profile__online
    is_active = request.params.get('is_active', None)
    if is_active:
        query_dict['is_active'] = is_active
    mail = request.params.get('email', None)
    if mail:
        query_dict['email'] = mail

    return query_dict


def RoleManage(request):
    """
    用户权限管理 superuser才能实现的业务
    :param request: GET/api/role/manage
    :return: json
    """
    flag, user, profile, request = admin_permissions(request)
    context = {}
    if flag:
        User_querySet = User.objects.all()

        queryDict = get_params_role(request)

        pagenum = request.params.get('page', 1)
        pagelimit = request.params.get('limit', 40)
        sort = request.params.get('sort', 'id')

        if queryDict:
            queryset = User_querySet.filter(**queryDict).values('id', 'username', 'is_superuser', 'profile__roles',
                                                                'profile__online',
                                                                'email', 'last_login', 'is_active').order_by(sort)

        else:
            queryset = User_querySet.values('id', 'username', 'is_superuser', 'profile__roles',
                                            'profile__online',
                                            'email', 'last_login', 'is_active').order_by(sort)

        paginator = Paginator(queryset, pagelimit)
        page = paginator.page(pagenum)

        context['code'] = 2000
        context['data'] = list(page)
        context['total'] = paginator.count
    else:
        context['code'] = 1000
        context['message'] = "非管理员无法操作"
    return JsonResponse(context)


def create_new_user(request):
    """
    创建新的用户
    :param request: POST/api/role/create
    :return: json
    """
    flag, user, profile, request = admin_permissions(request)
    context = {}
    if flag:
        # 提取数据
        user_name = request.params.get('username')
        password = request.params.get('password')
        email = request.params.get('email')
        role = request.params.get('role')
        introduction = request.params.get('introduction')
        online = 0
        avatar = 'https://gitee.com/cnpolaris-tian/giteePagesImages/raw/master/null/IMG_7777(20200409-144633).JPG'
        user = User.objects.create_user(username=user_name, password=password, email=email)

        profile = Profile.objects.get(user=user)
        profile.roles = role
        profile.introduction = introduction
        profile.online = online
        profile.avatar = avatar
        profile.save()

        context['code'] = 2000
    else:
        context['code'] = 1000
        context['message'] = "非管理员无法操作"
    return JsonResponse(context)


def list_role(request):
    """
    获取所有用户的权限列表
    :param request: /api/role/list
    :return: json
    """
    flag, user, profile, request = admin_permissions(request)
    context = {}
    if flag:
        User_querySet = User.objects.all()

        query_dict = get_params_role(request)

        pagenum = request.params.get('page', 1)
        pagelimit = request.params.get('limit', 40)
        sort = request.params.get('sort', 'id')

        if query_dict:
            query_set = User_querySet.filter(**query_dict).values('id', 'username', 'profile__roles',
                                                                  'is_active').order_by(sort)
        else:
            query_set = User_querySet.values('id', 'username', 'profile__roles', 'is_active').order_by(sort)

        paginator = Paginator(query_set, pagelimit)
        page = paginator.page(pagenum)
        context['code'] = 2000
        context['data'] = list(page)
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
        role = request.params.get('role', None)
        if User.objects.get(id=uid):
            user = User.objects.get(id=uid)
            if role and role in [1, 2, 3]:
                user.profile.roles = role
            user.save()
            context['code'] = 2000
            context['message'] = '权限修改成功'
        else:
            context['code'] = 1000
            context['message'] = "不存在指定用户"
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
        active = request.params.get('active', None)
        if User.objects.get(id=uid):
            user = User.objects.get(id=uid)
            if active:
                user.is_active = active
            user.save()
            context['code'] = 2000
            context['message'] = '用户状态修改成功'
        else:
            context['code'] = 1000
            context['message'] = "不存在指定用户"
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
        user_name = request.params.get('username', None)
        email = request.params.get('email', None)
        introduction = request.params.get('introduction', None)

        if User.objects.get(id=uid):
            user = User.objects.get(id=uid)
            if user_name is not None:
                user.username = user_name
            if email is not None:
                user.email = email
            if introduction is not None:
                user.profile.introduction = introduction

            user.save()
            context['code'] = 2000
            context['message'] = '用户信息修改成功'
        else:
            context['code'] = 1000
            context['message'] = "不存在指定的用户"

    else:
        context['code'] = 1000
        context['message'] = "非管理员无法操作"

    return JsonResponse(context)


def delete_role(request):
    """
    删除用户
    :param request:DELETE /api/role/delete
    :return: json
    """
    flag, user, profile, request = admin_permissions(request)
    context = {}
    if flag:
        try:
            uid = request.params.get('id', None)
            if uid:
                delete_user = User.objects.get(id=uid)
                # User.objects.all()
                # Profile.objects.all()
                # profile = Profile.objects.get(user=user)
                # profile.delete()
                # delete_user.delete()
                # profile.entry_set.remove(user)
                delete_user.delete()
                context['code'] = 2000
                context['message'] = '用户删除成功'
        except BaseException as e:
            context['code'] = 1000
            context['message'] = '出现错误{}'.format(e)
    else:
        context['code'] = 1000
        context['message'] = "非管理员无法操作"

    return JsonResponse(context)
