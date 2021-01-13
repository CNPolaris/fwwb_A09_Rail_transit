# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 16:31
# @FileName: mixins.py
# @Author  : CNPolaris
from __future__ import unicode_literals

import json
from django.apps import apps
from django.core.cache import cache, utils
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.utils.encoding import force_text
from django.urls import reverse_lazy

from transit.models import Menu

system_menus_key = utils.make_template_fragment_key('system.menus')


def construct_menus():
    Menu_list = Menu.objects.all()
    menus = [
        {
            'model_name': menu.model_name,
            'verbose_name': menu.model_verbose,
            'icon': menu.icon,
            'icon_color': menu.icon_color
        } for menu in Menu_list
    ]
    return menus


def get_user_config(user, mark, model):
    # content_type = get_content_type_for_model(model)
    # configs = Configure.objects.filter(
    #     creator=user,
    #     mark=mark,
    #     content_type=content_type).order_by('-pk')
    # if configs.exists():
    #     config = configs.first().content
    #     try:
    #         return json.loads(config)
    #     except BaseException:
    #         return None
    # else:
        return None


class BaseRequiredMixin(LoginRequiredMixin):
    cmodel = ''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "系统需要登录才能访问")
            return redirect_to_login(
                request.get_full_path(),
                self.get_login_url(), self.get_redirect_field_name()
            )
        model = self.kwargs.get('model', self.cmodel)
        if model:
            try:
                self.model = apps.get_model('transit', model.lower())
                self.opts = self.model._meta
                self.model_name = self.opts.model_name
                self.verbose_name = self.opts.verbose_name
                if self.kwargs.get('pk', None):
                    self.pk_url_kwarg = self.kwargs.get('pk')
            except BaseException:
                raise Http404("您访问的模块不存在.")
        return super(BaseRequiredMixin, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseRequiredMixin, self).get_context_data(**kwargs)
        self.meta = {}
        try:
            self.meta['model_name'] = self.model_name
            self.meta['verbose_name'] = self.verbose_name
        except BaseException:
            print("error")
            # self.meta['title'] = self.verbose_name
        context['meta'] = self.meta
        context['menus'] = construct_menus()

        return context
