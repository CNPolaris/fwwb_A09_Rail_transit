# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 10:42
# @FileName: urls.py
# @Author  : CNPolaris
from django.conf.urls import url
from django.urls import path
from . import user_login_logout

app_name = 'userprofile'

userprofile = [
    # 用户登录
    url(r'^login', user_login_logout.user_login),
    # # 用户注册
    # path('register/',views.user_register,name='register'),
    # 用户退出
    url(r'^logout', user_login_logout.user_logout),
    # 用户信息
    url(r'^info',user_login_logout.get_user_info),

    # # 用户删除
    # path('delete/<int:id>/',views.user_delete,name='delete'),
]