# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 18:26
# @FileName: app_extras.py
# @Author  : CNPolaris
from __future__ import unicode_literals
from django import template
from django.utils.http import urlencode

register = template.Library()


@register.filter(name='addcss', is_safe=True)
def addcss(field, css):
    return field.as_widget(attrs={"class": css})


@register.simple_tag(takes_context=True)
def get_query_string(context, **kwargs):
    params = context['request'].GET.copy()
    for k, v in kwargs.items():
        params[k] = v
    if params:
        return '?%s' % urlencode(sorted(params.items()))
    else:
        return ''
