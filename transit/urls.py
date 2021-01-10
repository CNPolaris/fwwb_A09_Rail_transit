# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: urls.py
# @Author  : CNPolaris

# 引入path
from django.urls import path, re_path

# 正在部署的应用的名称
from transit import views
from .echarts import echarts_monthflow, echarts_agestruct, echarts_dailyflow, echarts_singlesta
from .imports import load_dataoftrip, load_dataofstation, load_dataofuser, load_dataofworkday
app_name = 'transit'

urlpatterns = [
    # 首页路由
    path('index/', views.index, name='index'),
    # 向echarts提供数据的api
    # 单月客流
    path('echarts/data/<str:date>/monthflow.json', echarts_monthflow, name='monthflow'),
    # 用户年龄结构
    path('echarts/data/agestruct.json', echarts_agestruct, name='agestruct'),
    # 每日客流量
    path('echarts/data/<int:year>/dailyflow.json', echarts_dailyflow, name='dailyflow'),
    # 单站的点出/入站客流分析
    path('echarts/data/<str:station>/<str:date>/singlesta.json', echarts_singlesta, name='singlestaion'),

    # import数据模块
    path('load_dataoftrip', load_dataoftrip, name='load_data'),
    path('load_dataofworkday', load_dataofworkday, name='load_dataofworkday'),
    path('load_dataofuser', load_dataofuser, name='load_dataofuser'),
    path('load_dataofstation', load_dataofstation, name='load_dataofstation')
]
