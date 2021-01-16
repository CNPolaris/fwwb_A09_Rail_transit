# -*- coding: utf-8 -*-
# @Time    : 2021/1/16 19:47
# @FileName: tasks.py
# @Author  : CNPolaris
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType

import urllib
import re

from py._log.log import Syslog


# def get_related_client_name(obj):
#     related_clients = []
#     for f in obj._meta.fields:
#         if f.related_model is Client or (
#                 f.name == 'client' and isinstance(f, models.CharField)):
#             value = display_for_field(f.value_from_object(obj), f, html=False)
#             related_clients.append(value)
#     return '{}'.format(", ".join(c for c in list(set(related_clients))))

def log_action(user_id, content_type_id, object_id,
               action_flag, message='', content='',
               actived=True, related_client=None, created=None
               ):
    model = ContentType.objects.get_for_id(content_type_id).model_class()
    object = model.objects.get(pk=object_id)
    user = User.objects.get(pk=user_id)
    onidc_id = user.onidc_id
    data = dict(
        creator_id=user_id,
        onidc_id=onidc_id,
        object_repr=object,
        action_flag=action_flag,
        message=message,
        object_desc=force_text(object)[:128],
        related_client=related_client[:128],
        content=content, actived=actived
    )
    if created:
        data.update(**dict(created=created))
    log = Syslog.objects.create(**data)
    return force_text(log)
