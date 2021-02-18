# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: urls.py
# @Author  : CNPolaris

# 引入path
from django.conf.urls import url, include
# 正在部署的应用的名称
from transit import views, sign_in_out
from .apis.urls import echarts_api_urls, manager_urls
from .imports import load_dataoftrip, load_dataofstation, load_dataofuser, load_dataofworkday
app_name = 'transit'

urlpatterns = [
    # 首页路由
    # 登录登出
    url(r'^api/signin', sign_in_out.signin),
    url(r'^api/signout', sign_in_out.signout),

    # API模块
    url(r'^api/', include(echarts_api_urls)),
    url(r'^api/', include(manager_urls)),

    # import数据模块
    url('load_dataoftrip', load_dataoftrip, name='load_data'),
    url('load_dataofworkday', load_dataofworkday, name='load_dataofworkday'),
    url('load_dataofuser', load_dataofuser, name='load_dataofuser'),
    url('load_dataofstation', load_dataofstation, name='load_dataofstation')
]
