# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 20:02
# @FileName: list.py
# @Author  : CNPolaris
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, ListView
from django.contrib.admin.utils import label_for_field
from django.utils.html import format_html

from transit.lib.utils import fields_for_model
from transit.mixins import BaseRequiredMixin, get_user_config
from django.core.cache import cache, utils
from django.utils.http import urlencode

_QUERY = 'search'
# _RANGE = 'range'
_ORDER = 'order'
_PAGINATE = 'paginate_by'


# _ALL_VAL = 'all'

class ListModelView(BaseRequiredMixin, ListView):

    def get_template_names(self):
        """
        获取对应的模板名称 e.g trips/list.html 默认为base/list.html
        :return:
        """
        return ["{0}/list.html".format(self.model_name), "base/list.html"]

    @cached_property
    def _config(self):
        key = utils.make_template_fragment_key(
            "{}.{}.{}".format(self.request.user.id, self.model_name, 'list')
        )
        data = cache.get_or_set(
            key, get_user_config(self.request.user, 'list', self.model), 180
        )
        return data

    @property
    def default_list_fields(self):
        """
        获取model默认字段
        :return: list e.g ['user_id', 'in_station']
        """
        exclude = ['id', 'password', 'system_pass', 'user_permissions']
        base_fields = list(fields_for_model(self.model, exclude=exclude))
        extra_fields = getattr(self.opts, 'extra_fields', None)
        if extra_fields and isinstance(extra_fields, list):
            base_fields.extend(extra_fields)
        return base_fields

    @property
    def get_list_fields(self):
        """
        多种方式获取字段
        :return: list e.g ['user_id', 'in_station']
        """
        # TODO：补充多重字段筛选
        fields = self.default_list_fields
        return fields

    @cached_property
    def get_params(self):
        """
        从请求中获取排序参数
        :return: e.g {'order': 'in_station.-user_id'}
        """
        self.params = dict(self.request.GET.items())
        return self.params

    def get_query_string(self, new_params=None, remove=None):
        """
        获取查询项的字符串
        :param new_params: 新的查询字段
        :param remove: 要别移除的字段
        :return: e.g {'order': 'in_station.-user_id'}
        """
        new_params = {} if not new_params else new_params
        remove = [] if not remove else remove
        p = self.get_params.copy()
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

    def get_ordering(self):
        """
        获取通过指定排序的结果
        :return: list e.g ['user_id', '-pk']
        """
        # 默认的排序规则
        ordering = list(self.opts.ordering or [])
        # 获取请求中的排序规则
        orders = self.request.GET.get(_ORDER, None)
        # 如果不为空
        if orders:
            # ordering 置空
            ordering = []
            for p in orders.split('.'):
                _, pfx, fname = p.rpartition('-')
                if fname.startswith('-') and pfx == "-":
                    ordering.append(fname[1:])
                else:
                    ordering.append(pfx + fname)
        pk_name = self.opts.pk.name
        if not (set(ordering) & {'pk', '-pk', pk_name, '-' + pk_name}):
            ordering.append('-pk')
        return ordering

    def get_queryset(self):
        """
        根据路由模型查询数据库
        :return: QuerySet
        """
        # queryset = super(ListModelView, self).get_queryset()
        queryset = self.model.objects.all()
        return queryset

    def make_thead(self):
        """
        创建列表头部
        :return:
        """
        # 字段
        fields = self.get_list_fields
        # 排序选项
        ordering = [o for o in self.get_ordering() if o.rpartition('-')
        [2] in fields]
        # 可供选择的排序方式
        switch = {'asc': '', 'desc': '-'}
        checked_fields = fields
        can_sorted_fields = [f.name for f in self.opts.concrete_fields]
        for _, field_name in enumerate(fields):
            checked = field_name in checked_fields
            sortable = field_name in can_sorted_fields
            if field_name == 'field-first':
                yield {
                    "text": mark_safe(
                        '''<input id="action-toggle"'''
                        '''name="mode" value="page" type="checkbox">'''
                    ),
                    "field": field_name,
                    "class_attrib": mark_safe(' class="no-print field-first"'),
                    "sortable": sortable,
                }
                continue
            if field_name == 'field-second':
                yield {
                    "text": "#",
                    "field": field_name,
                    "class_attrib": mark_safe(' class="field-second"'),
                    "sortable": sortable,
                }
            if field_name == 'field-last':
                yield {
                    "text": "操作",
                    "field": field_name,
                    "class_attrib": mark_safe(' class="no-print field-last"'),
                    "sortable": sortable,
                }
                continue
            try:
                text = label_for_field(name=field_name, model=self.model)
            except Exception:
                continue
            if field_name not in can_sorted_fields:
                # Not sortable
                yield {
                    "text": text,
                    "checked": checked,
                    "field": field_name,
                    "class_attrib": format_html(' class="col-{}"', field_name),
                    "sortable": sortable,
                }
                continue
            # OK, it is sortable if we got this far
            is_sorted = field_name in ordering or '-' + field_name in ordering
            sorted_key = 'asc' if is_sorted and field_name in ordering else 'desc'
            sorted_value = switch.get(sorted_key)
            new_ordering = [
                o for o in ordering if o != str(
                    sorted_value + field_name)]
            remove_link = '.'.join(i for i in new_ordering)
            new_sorted_key = 'desc' if is_sorted and field_name in ordering else 'asc'
            new_sorted_value = switch.get(new_sorted_key)
            new_ordering.insert(0, str(new_sorted_value + field_name))
            toggle_link = '.'.join(i for i in new_ordering)
            toggle_url = self.get_query_string({'order': toggle_link})
            remove_url = self.get_query_string({'order': remove_link})
            th_classes = ['sortable', 'col-{}'.format(field_name)]
            yield {
                "text": text,
                "checked": checked,
                "field": field_name,
                "sortable": sortable,
                "is_sorted": is_sorted,
                "sorted_key": sorted_key,
                "remove_link": "{}".format(remove_url),
                "toggle_link": "{}".format(toggle_url),
                "class_attrib": format_html(
                    'style="{}" class="{}"',
                    'min-width: 64px;' if is_sorted else '',
                    ' '.join(th_classes)) if th_classes else '',

            }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListModelView, self).get_context_data(**kwargs)
        _extra = {
            'thead': self.make_thead(),
        }
        context.update(**_extra)
        return context
