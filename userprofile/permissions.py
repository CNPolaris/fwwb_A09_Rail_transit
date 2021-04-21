# -*- coding: utf-8 -*-
# @Time    : 2021/4/21 19:52
# @FileName: permissions.py
# @Author  : CNPolaris
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework_jwt.serializers import jwt_decode_handler
from django.contrib.auth.models import User
from userprofile.models import Profile


class IsSelfOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            token = request.GET.get('token')
            toke_user = jwt_decode_handler(token)
            user_id = toke_user["user_id"]
            if User.objects.get(id=user_id):
                if Profile.objects.filter(user_id=user_id).exists():
                    profile = Profile.objects.get(user_id=user_id)
                    if profile.roles in ['admin', 1]:
                        return True
            else:
                return False
        return False
