# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: urls.py
# @Author  : CNPolaris

# 引入path
from django.conf.urls import url, include
# 正在部署的应用的名称
from .apis.urls import echarts_api_urls, api_urls
from transit.apis.imports import load_dataoftrip, load_dataofstation, load_dataofuser, load_dataofworkday
from userprofile.urls import userprofile, rolemanage_urls
from transit.transit_model.urls import predict_urls
app_name = 'transit'

urlpatterns = [
    # 首页路由

    # API模块
    url(r'^api/', include(echarts_api_urls)),
    url(r'^api/', include(api_urls)),
    # 用户相关
    url(r'^api/userprofile/', include(userprofile)),
    url(r'^api/role/', include(rolemanage_urls)),
    # 模型预测
    url(r'^api/', include(predict_urls)),
    # import数据模块
    url('load_dataoftrip', load_dataoftrip, name='load_data'),
    url('load_dataofworkday', load_dataofworkday, name='load_dataofworkday'),
    url('load_dataofuser', load_dataofuser, name='load_dataofuser'),
    url('load_dataofstation', load_dataofstation, name='load_dataofstation')
]
