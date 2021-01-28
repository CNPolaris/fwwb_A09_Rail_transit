# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 21:48
# @FileName: tableView.py
# @Author  : CNPolaris
from django.db import models
from django.forms import fields_for_model
from django.http import Http404
from django.utils.module_loading import import_string
from rest_framework.generics import GenericAPIView
from django.utils.decorators import method_decorator
from rest_framework.mixins import ListModelMixin
from django.apps import apps

from transit.models import Station, TripStatistics, Trips, Users, Workdays
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from transit.apis.serializers import StationSerializer, TripsSerializer, TripStatisticsSerializer, UsersSerializer, \
    WorkdaysSerializer
from transit.mixins import BaseRequiredMixin
from rest_framework.pagination import PageNumberPagination

_ORDER = 'order'


# 自定义分页器
class StandardResultSetPagination(PageNumberPagination):
    # 只需要做一些配置即可
    page_size = 100  # 每页的数据量（默认）
    page_query_param = "page"  # 请求参数中的 page参数名
    page_size_query_param = "size"  # 请求参数中的 page_size参数名
    max_page_size = 3  # 每页最大数量，请求参数中如果超过了这个配置，不会报错，会按照此配置工作

    def get_paginated_response(self, data):
        return {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        }


class AllSetByModel(ViewSetMixin, GenericAPIView):
    """
    可适用于所有model的list获取
    """

    def get_ordering(self):
        # 默认的排序规则
        ordering = list(self.opts.ordering or [])
        # 获取请求中的排序规则
        orders = self.request.GET.get(_ORDER, None)

    def get_queryset(self):
        """
        获取查询集合
        :return:
        """
        queryset = self.model.objects.all()
        return queryset

    def get_serializer_class(self):
        """
        获取序列化器
        :return:
        """
        name = self.model_name.capitalize()
        serializer_class_path = "transit.apis.serializers.{}Serializer".format(name)
        self.serializer_class = import_string(serializer_class_path)
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        根据参数获取指定model的数据列表
        :param request: get
        :param args:
        :param kwargs: /model e.g /station
        :return:
        """
        cmodel = ''
        context = {"data": None}
        model = self.kwargs.get('model', cmodel)
        if model:
            try:
                self.model = apps.get_model('transit', model.lower())
                self.opts = self.model._meta
                self.model_name = self.opts.model_name
                self.verbose_name = self.opts.verbose_name
                # 数据筛选
                queryset = self.get_queryset()
                # 实例化分页器
                page = StandardResultSetPagination()
                # 调用分页方法
                page_query = page.paginate_queryset(queryset, request, view=self)
                if page is not None:
                    # 序列化
                    serializer = self.get_serializer(instance=page_query, many=True)
                    page_info = page.get_paginated_response(serializer.data)
                    context["count"] = page_info["count"]
                    context["next"] = page_info["next"]
                    context["previous"] = page_info["previous"]
                serializer = self.get_serializer(instance=queryset, many=True)
                context["data"] = serializer.data
            except BaseException as e:
                print(e)
                raise Http404("您访问的模块不存在.")
        return Response(context)


class OneSetByPK(ViewSetMixin, GenericAPIView):
    """
    根据pk主键来查询指定的数据集
    """

    def get_serializer_class(self):
        """
        获取序列化器
        :return:
        """
        name = self.model_name.capitalize()
        serializer_class_path = "transit.apis.serializers.{}Serializer".format(name)
        self.serializer_class = import_string(serializer_class_path)
        return self.serializer_class

    def search(self, request, *args, **kwargs):
        """
        根据pk进行数据查询
        :param request: Get
        :param args:
        :param kwargs: /model/pk e.g /station/1004
        :return:
        """
        cmodel = ''
        context = {"data": None}
        model = self.kwargs.get('model', cmodel)
        pk = self.kwargs.get("pk")
        if model and pk:
            try:
                self.model = apps.get_model('transit', model.lower())
                self.opts = self.model._meta
                self.model_name = self.opts.model_name
                self.verbose_name = self.opts.verbose_name
                self.pk = pk
                queryObj = self.model.objects.filter(pk=self.pk)
                serializer = self.get_serializer(instance=queryObj, many=True)
                context["data"] = serializer.data
            except BaseException as e:
                print(e)
                raise Http404("您访问的模块不存在.")
        return Response(context)


