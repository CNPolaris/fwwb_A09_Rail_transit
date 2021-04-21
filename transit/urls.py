# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: urls.py
# @Author  : CNPolaris

from django.conf.urls import url, include
from .apis.urls import echarts_api_urls, api_urls
from userprofile.urls import userprofile, role_urls
from transit.transit_model.urls import predict_urls
from transit.views import PassengerViewSet, WorkdayViewSet, TripViewSet, StationViewSet

app_name = 'transit'

urlpatterns = [
    # 首页路由
    # API模块
    url(r'^api/', include(echarts_api_urls)),
    url(r'^api/', include(api_urls)),
    # 数据管理
    url(r'^api/manage/test/passenger/',
        PassengerViewSet.as_view({'get': 'list', 'put': 'update', 'delete': 'destroy', 'post': 'create'})),
    url(r'^api/manage/test/workday',
        WorkdayViewSet.as_view({'get': 'list', 'put': 'update', 'delete': 'destroy', 'post': 'create'})),
    url(r'^api/manage/test/trip',
        TripViewSet.as_view({'get': 'list', 'put': 'update', 'delete': 'destroy', 'post': 'create'})),
    url(r'^api/manage/test/station',
        StationViewSet.as_view({'get': 'list', 'put': 'update', 'delete': 'destroy', 'post': 'create'})),
    # 用户管理
    url(r'^api/userprofile/', include(userprofile)),
    url(r'^api/role/', include(role_urls)),
    # 模型预测
    url(r'^api/predict/', include(predict_urls)),
]
