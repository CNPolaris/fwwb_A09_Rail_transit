# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from threading import Thread

from django.db import models
from django.http import JsonResponse
from django.contrib import messages
from django.forms.models import model_to_dict, construct_instance
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.module_loading import import_string
from django.utils.encoding import force_text
from django.views.generic.edit import CreateView, UpdateView
# Create your views here.
from transit.lib.tasks import log_action
from transit.lib.utils import get_content_type_for_model
from transit.mixins import BaseRequiredMixin, PostRedirect
from django.contrib.auth.models import User


class NewModelView(BaseRequiredMixin, PermissionRequiredMixin,
                   PostRedirect, SuccessMessageMixin, CreateView):

    def get_template_names(self):
        prefix = self.model_name
        if self.request.is_ajax():
            return ["{}/ajax_new.html".format(prefix), "base/ajax_new.html"]
        else:
            return ["{}/new.html".format(prefix), "base/new.html"]

    def get_permission_required(self):
        """
        获取权限路径
        :return:
        """
        self.permission_required = 'transit.add_%s' % (self.model_name)
        return super(NewModelView, self).get_permission_required()

    def handle_no_permission(self):
        """
        判断是否有新建权限
        :return:
        """
        messages.error(self.request, '您没有新建{0}的权限.'.format(self.model._meta.verbose_name))
        return super(NewModelView, self).handle_no_permission()

    def get_success_message(self, cleaned_data):
        """
        新建成功信息
        :param cleaned_data:
        :return:
        """
        self.success_message = "成功创建了{}{}".format(self.verbose_name, self.object)
        return self.success_message

    def get_form_class(self):
        """
        获取表单
        :return:
        """
        name = self.model_name.capitalize()
        try:
            # 获取对应的表单
            form_class_path = "transit.forms.{}NewForm".format(name)
            self.form_class = import_string(form_class_path)
        except BaseException:
            form_class_path = 'transit.forms.{}Form'.format(name)
            self.form_class = import_string(form_class_path)
        return self.form_class

    def get_form_kwargs(self):
        kwargs = super(NewModelView, self).get_form_kwargs()
        params = self.request.GET.dict()
        # 字段
        mfields = [f.attname for f in self.opts.fields]
        for k in params.keys():
            if k in mfields:
                kwargs.update({k: params[k]})
        related_models = []
        for f in self.opts.get_fields():
            if isinstance(f, (models.ForeignKey, models.ManyToManyField)):
                if f.related_model:
                    related_models.append(f.related_model)
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super(NewModelView, self).form_valid(form)
        log_action(
            user_id=self.request.user.pk,
            content_type_id=get_content_type_for_model(self.object, True).pk,
            object_id=self.object.pk,
            action_flag="新增"
        )
        if self.request.is_ajax():
            data = {
                'message': "成功提交表单数据",
                'data': form.cleaned_data
            }
            return JsonResponse(data)
        else:
            return response

    def get_context_data(self, **kwargs):
        context = super(NewModelView, self).get_context_data(**kwargs)
        return context
