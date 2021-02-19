# -*- coding: utf-8 -*-
# @Time    : 2021/2/19 19:14
# @FileName: exports.py
# @Author  : CNPolaris
from __future__ import unicode_literals

from collections import OrderedDict
from decimal import Decimal
from itertools import chain

import xlwt
from io import BytesIO

from django.apps import apps
from django.db import models
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.utils import formats, timezone
from django.utils.http import urlquote
from django.utils.text import slugify
from django.utils.encoding import force_text
from django.contrib.admin.utils import label_for_field


def fields_for_model(model, fields=None, exclude=None):
    """
    返回一个model类`字段名`和`字段`组成的元组列表。
    """
    field_list = []
    opts = model._meta
    for f in sorted(chain(opts.concrete_fields, opts.many_to_many)):
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        else:
            field_list.append((f.name, f))
    field_dict = OrderedDict(field_list)
    return field_dict


def display_for_value(value):
    """
    返回一个比较人性化的值。
    """
    if value is None:
        return ''
    elif isinstance(value, bool):
        return force_text(value)
    elif isinstance(value, (int, Decimal, float)):
        return formats.number_format(value)
    elif isinstance(value, models.query.QuerySet):
        return ', '.join(force_text(v) for v in [force_text(i) for i in value])
    elif isinstance(value, (list, tuple)):
        return ', '.join(force_text(v) for v in value)
    else:
        return force_text(value)


def display_for_field(value, field, empty_value_display):
    """返回某个模型字段的一个字段值"""
    if getattr(field, 'flatchoices', None):
        return dict(field.flatchoices).get(value, empty_value_display)
    elif isinstance(field, (models.BooleanField, models.NullBooleanField)):
        boolchoice = {False: "否", True: "是"}
        return boolchoice.get(value)
    elif value is None:
        return empty_value_display
    elif isinstance(field, models.DateTimeField):
        return formats.localize(timezone.template_localtime(value))
    elif isinstance(field, (models.DateField, models.TimeField)):
        return formats.localize(value)
    elif isinstance(field, models.DecimalField):
        return formats.number_format(value, field.decimal_places)
    elif isinstance(field, (models.IntegerField, models.FloatField)):
        return formats.number_format(value)
    elif isinstance(field, models.ForeignKey) and value:
        rel_obj = field.related_model.objects.get(pk=value)
        return force_text(rel_obj)
    else:
        return display_for_value(value)


def make_to_excel(object_list=None):
    """
    传入某个模型的查询集（queryset）
    将查询集写入excel表格并响应以附件返回
    :param object_list: querySet
    :return:
    """
    body_style = xlwt.XFStyle()

    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    font = xlwt.Font()
    font.bold = True

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 22
    title_style = xlwt.XFStyle()
    title_style.borders = borders
    title_style.font = font
    title_style.pattern = pattern
    body_style = xlwt.XFStyle()
    body_style.borders = borders
    if object_list is not None:
        model_name = object_list.model._meta.model_name
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('{0}List'.format(model_name.capitalize()))
        model = object_list.model
        fields = fields_for_model(model)
        field_names = []
        field_verboses = []
        for attname, field in fields.items():
            field_names.append(attname)
            fv = label_for_field(attname, model)
            field_verboses.append(fv)
        for col in range(len(field_verboses)):
            ws.write(0, col, field_verboses[col], title_style)
        row = 1
        for obj in object_list:
            for index, field_name in enumerate(field_names):
                field = model._meta.get_field(field_name)
                value = field.value_from_object(obj)
                cell_value = display_for_field(value, field, empty_value_display='N/A')
                ws.write(row, index, cell_value, body_style)
            row += 1
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        response = StreamingHttpResponse(output)
        response['content_type'] = 'application/octet-stream'
        response['charset'] = 'utf-8'
        response['Content-Disposition'] = 'attachment; filename="{0}{1}.xls"'.format(
            model_name.capitalize(), timezone.datetime.now().strftime('%Y%m%d%H%M'))
        return response


def download(request):
    """
    在高级管理员权限下提供数据的excel格式导出
    :param request: GET /api/exports?model=station
    :return: json
    """
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': '/sign.html'},
            status=302
        )

    if request.session['usertype'] != 'admin':
        return JsonResponse({
            'ret': 302,
            'msg': '需要高级管理员权限才可导出数据',
            'redirect': '/sign.html'},
            status=302
        )

    if request.method == 'GET':
        request.params = request.GET

    target_model = request.params.get('model', None)
    if target_model is not None:
        target_model = apps.get_model('transit', target_model.lower())
        objects = target_model.objects.all()
        return make_to_excel(objects)
