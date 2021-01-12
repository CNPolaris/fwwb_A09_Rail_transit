# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 20:02
# @FileName: list.py
# @Author  : CNPolaris
from django.utils.functional import cached_property
from django.views.generic import TemplateView, ListView
from transit.mixins import BaseRequiredMixin, get_user_config
from django.core.cache import cache, utils
from django.utils.http import urlencode


class ListModelView(BaseRequiredMixin, ListView):

    def get_template_names(self):
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

    def get_queryset(self):
        # queryset = super(ListModelView, self).get_queryset()

        queryset = self.model.objects.all()
        print(queryset)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListModelView, self).get_context_data(**kwargs)
        return context
