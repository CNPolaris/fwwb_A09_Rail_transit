# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 21:29
# @FileName: utils.py
# @Author  : CNPolaris
from itertools import chain
from collections import OrderedDict

from django.contrib.admin.utils import lookup_field
from django.contrib.auth import get_permission_codename
from django.utils import formats, timezone
from django.utils.encoding import force_text

from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.db import models, router
import decimal
import datetime


def get_query_string(params, new_params=None, remove=None):
    new_params = new_params if new_params else {}
    remove = remove if remove else []
    p = params.copy()
    for r in remove:
        for k in list(p):
            if k.startswith(r):
                del p[k]
    for k, v in new_params.items():
        if v is None:
            if k in p:
                del p[k]
        else:
            p[k] = v
    if p:
        return '?%s' % urlencode(sorted(p.items()))
    else:
        return ''


def get_content_type_for_model(obj, fcm=False):
    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level.
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(obj, for_concrete_model=fcm)


def fields_for_model(model, fields=None, exclude=None):
    """
    获取model的字段 并返回
    :param model: 目标模型
    :param fields: 已有字段
    :param exclude: 要排除的字段
    :return: list
    """
    field_list = []
    opts = model._meta
    for f in chain(opts.concrete_fields, opts.many_to_many):
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        else:
            field_list.append((f.name, f))
    field_dict = OrderedDict(field_list)
    return field_dict


def display_for_value(value):
    if isinstance(value, bool):
        return force_text(value)
    elif isinstance(value, (int, decimal.Decimal, float)):
        return formats.number_format(value)
    elif isinstance(value, (list, tuple)):
        return ', '.join(force_text(v) for v in value)
    # elif isinstance(value, six.integer_types + (decimal.Decimal, float)):
    #     return formats.number_format(value)
    elif isinstance(value, datetime.datetime):
        return formats.localize(timezone.template_localtime(value))
    elif isinstance(value, (datetime.date, datetime.time)):
        return formats.localize(value)
    elif isinstance(value, models.query.QuerySet):
        # if value.model is Option and COLOR_TAGS:
        #     html = ''
        #     for v in value:
        #         item = '<span class="badge bg-{}">{}</span>&nbsp'.format(
        #             v.color, v.text
        #         )
        #         html += item
        #     return mark_safe(html)
        # else:
        value = [force_text(i) for i in value]
        return display_for_value(value)
    else:
        return force_text(value)


def make_boolean_icon(field_val):
    choice = {
        True: 'fa fa-check-circle text-green',
        False: 'fa fa-ban on fa-check-circle text-red',
        None: 'unknown'}[field_val]
    return format_html('<i class="{}"></i>'.format(choice))


def make_color_icon(field_val):
    return format_html('<i class="fa fa-square text-{}"'.format(field_val))


def display_for_field(value, field, html=True, only_date=True):
    # if getattr(field, 'flatchoices', None):
    #     # if html and field.name == 'color' and value:
    #     #     return make_color_icon(value)
    #     return dict(field.flatchoices).get(value, '')
    # # elif html and (isinstance(field, (
    # #         models.BooleanField, models.NullBooleanField))):
    # #     return make_boolean_icon(value)
    # # elif isinstance(field, (models.BooleanField, models.NullBooleanField)):
    # #     boolchoice = {False: "否", True: "是"}
    # #     return boolchoice.get(value)
    # elif value is None:
    #     return ""
    # elif isinstance(field, models.DecimalField):
    #     return formats.number_format(value, field.decimal_places)
    # elif isinstance(field, (models.IntegerField, models.FloatField)):
    #     return formats.number_format(value)
    # elif isinstance(field, models.ForeignKey) and value:
    #     rel_obj = field.related_model.objects.get(pk=value)
    #     # if html and COLOR_FK_FIELD and isinstance(rel_obj, Option):
    #     #     text_color = rel_obj.color
    #     #     if not text_color:
    #     #         text_color = 'text-info'
    #     #     safe_value = format_html(
    #     #         '<span class="text-{}">{}</span>', text_color, rel_obj.text)
    #     #     return safe_value
    #     return force_text(rel_obj)
    # elif isinstance(field, models.TextField) and value:
    #     return force_text(value)
    # elif isinstance(field, models.DateTimeField):
    #     if only_date:
    #         return formats.date_format(value)
    #     return formats.localize(timezone.template_localtime(value))
    # elif isinstance(field, (models.DateField, models.TimeField)):
    #     return formats.localize(value)
    # elif isinstance(field, models.FileField) and value:
    #     return format_html('<a href="{}">{}</a>', value.url, value)
    # else:
    return display_for_value(value)


def has_permission(opts, user, perm):
    codename = get_permission_codename(perm, opts)
    return user.has_perm("%s.%s" % (opts.app_label, codename))


def get_forms_names():
    forms = import_string('transit.forms')
    return dir(forms)


def _has_form(model_name):
    return "{}Form".format(model_name) in get_forms_names()


def _has_add_form(model_name):
    name = model_name.capitalize()
    return _has_form(name) or "{}NewForm".format(name) in get_forms_names()


def _has_edit_form(model_name):
    name = model_name.capitalize()
    return _has_form(name) or "{}EditForm".format(name) in get_forms_names()


def can_create(opts, user):
    # from idcops import forms
    name = opts.model_name.capitalize()
    return has_permission(opts, user, 'add') and _has_add_form(name)


def can_change(opts, user):
    # from idcops import forms
    name = opts.model_name.capitalize()
    return has_permission(opts, user, 'change') and _has_edit_form(name)


def nature_field_name(model):
    """ Return model CharField , SlugField Field name use nature field."""
    opts = model._meta
    fields = [
        f.name for f in opts.fields if (
                isinstance(f, (models.CharField, models.GenericIPAddressField))
                and not getattr(f, 'blank', False)
        )
    ]
    if fields:
        if 'name' in fields:
            return 'name'
        elif 'text' in fields:
            return 'text'
        elif 'title' in fields:
            return 'title'
        elif 'username' in fields:
            return 'username'
        elif 'linenum' in fields:
            return 'linenum'
        elif 'kcnum' in fields:
            return 'kcnum'
        elif 'address' in fields:
            return 'address'
        else:
            if 'created' in [f.name for f in opts.fields]:
                return 'created'
            else:
                return fields[0]
    else:
        if 'created' in [f.name for f in opts.get_fields()]:
            return 'created'
        else:
            return '{}'.format(opts.pk.attname)


def make_tbody_tr(
        lmv, obj, row_num, fields, extra_fields, _only_date,
        _verbose_name, _model_name, to_field_name
):
    """Return tbody tr items."""
    pk_val = obj.pk
    opts = lmv.opts
    detail_link = obj.get_absolute_url
    update_link = obj.get_edit_url
    rowdata = ''
    for field_name in fields:
        td_class = "field-{}".format(field_name)
        if field_name == 'field-first':
            td_text = pk_val
            td_format = '''<td class="no-print {}">
                <input type="checkbox" name="index" value="{}"></td>'''
        if field_name == 'field-second':
            td_text = row_num
            td_format = '<td class="{}">{}.</td>'
        if field_name == 'field-last':
            _edit = ''
            if can_change(opts, lmv.request.user):
                _edit = '''
                    <a title="编辑" href="{}">
                    <span class="label label-default margin-r-5">编辑</span>
                    </a>'''.format(update_link)
            _show = '''
                <a title="弹窗模式进行查看" href="{}"
                data-toggle="modal" data-target="#modal-lg">
                <span class="label label-default">查看</span>
                </a>'''.format(detail_link)
            td_text = mark_safe(_edit + _show)
            td_format = '<td class="no-print {}">{}</td>'
        if field_name not in extra_fields:
            td_format = '<td class="{}">{}</td>'
            classes = 'text-info'
            try:
                field = opts.get_field(field_name)
                value = field.value_from_object(obj)
                td_text = display_for_field(value, field, only_date=_only_date)
                # if field.name == to_field_name:
                #     title = "点击查看 {} 为 {} 的详情信息".format(
                #         opts.verbose_name, force_text(obj))
                #     td_text = mark_safe(
                #         '<a title="{}" href="{}">{}</a>'.format(
                #             title, detail_link, td_text
                #         )
                #     )
                if getattr(field, 'flatchoices', None) \
                        or isinstance(field, models.ForeignKey) \
                        or isinstance(field, models.NullBooleanField):
                    link = lmv.get_query_string(
                        {'{}'.format(field.name): '{}'.format(value)}, ['page']
                    )
                    td_title = display_for_field(
                        value, field, html=False, only_date=_only_date
                    )
                    title = "点击过滤 {} 为 {} 的所有 {}".format(
                        field.verbose_name, td_title, _verbose_name
                    )
                    td_text = mark_safe(
                        '<a class="{}" title="{}" href="{}">{}</a>'.format(
                            classes, title, link, td_text
                        )
                    )
            except BaseException:
                _, _, td_text = lookup_field(
                    field_name, obj, obj._meta.model)
                td_text = mark_safe(td_text)
        rowdata += format_html(td_format, td_class, td_text)
    return mark_safe(rowdata)
