# # -*- coding: utf-8 -*-
# # @Time    : 2021/2/19 19:14
# # @FileName: exports.py
# # @Author  : CNPolaris
from __future__ import unicode_literals

import json

from django.apps import apps
from django.http import JsonResponse
from userprofile.models import Profile
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import jwt_decode_handler


def dispatcher(request):
    token = request.GET.get('token')
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    context = {'code': 1000}
    if user:
        if Profile.objects.filter(user_id=user_id).exists():
            profile = Profile.objects.get(user_id=user_id)
            if profile.roles == 'admin':
                if request.method == 'GET':
                    request.params = request.GET

                target_model = request.params.get('model', None)
                if target_model is not None:
                    target_model = apps.get_model('transit', target_model)
                    fields = target_model._meta.fields
                    field = []
                    verbose = []
                    for i in fields:
                        field.append(i.name)
                        verbose.append(i.verbose_name)
                    context['code'] = 2000
                    context['field'] = field
                    context['verbose_name'] = verbose
                    return JsonResponse(context)
                else:
                    return JsonResponse({'code': 1000, 'message': "model不存在"})
            else:
                return JsonResponse({'code': 1000, 'message': "无权执行该项操作"})
        else:
            return JsonResponse({'code': 1000, 'message': "无权执行该项操作"})
    else:
        return JsonResponse({'code': 1000, 'message': "无权执行该项操作"})
