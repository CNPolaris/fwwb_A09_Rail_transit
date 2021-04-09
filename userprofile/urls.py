# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 10:42
# @FileName: urls.py
# @Author  : CNPolaris
from django.conf.urls import url
from django.urls import path
from . import user_login_logout
from . import rolemanage
app_name = 'userprofile'

userprofile = [
    # 用户登录
    url(r'^login', user_login_logout.user_login),
    # 用户退出
    url(r'^logout', user_login_logout.user_logout),
    # 用户信息
    url(r'^info', user_login_logout.get_user_info),
    # 获取当前权限等级
    url(r'^role', user_login_logout.get_role),
]

role_urls = [
    # 权限管理
    url('manage', rolemanage.RoleManage),
    # 创建新用户
    url('create', rolemanage.create_new_user),
    # 获取所有用户的权限列表
    url('list', rolemanage.list_role),
    # 修改用户权限
    url('update', rolemanage.modify_user_role),
    # 强制用户下线
    url('off', rolemanage.offline),
    # 修改用户的信息
    url('info', rolemanage.modify_user_info),
    # 删除用户
    url('delete', rolemanage.delete_role),
    # 获取权限表
    url('permission', rolemanage.get_permission_list),
    # 编辑权限表
    url('permission/edit', rolemanage.edit_permission),
    # 查询指定权限的用户有哪些
    url('permission/look', rolemanage.get_role_permission)
]