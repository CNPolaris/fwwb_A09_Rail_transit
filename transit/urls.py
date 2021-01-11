# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: urls.py
# @Author  : CNPolaris

# 引入path
from django.conf.urls import url, include, static
from django.urls import path
# 正在部署的应用的名称
from transit import views
from .echarts import echarts_monthflow, echarts_agestruct, echarts_dailyflow, echarts_singlesta, echarts_eachSta
from .imports import load_dataoftrip, load_dataofstation, load_dataofuser, load_dataofworkday
app_name = 'transit'

urlpatterns = [
    # 首页路由
    url(r'^$', views.IndexView.as_view(), name='index'),
    # 向echarts提供数据的api
    # 单月客流
    url(r'^echarts/data/monthflow', echarts_monthflow, name='monthflow'),
    # 用户年龄结构
    url('echarts/data/agestruct.json', echarts_agestruct, name='agestruct'),
    # 每日客流量
    url('^echarts/data/dailyflow.json/(?P<year>[0-9]{4})/$', echarts_dailyflow, name='dailyflow'),
    # 单站的点出/入站客流分析
    url('echarts/data/<str:station>/<str:date>/singlesta.json', echarts_singlesta, name='singlestaion'),
    # 每天所有站点的进出入站点的次数
    url('^echarts/data/eachSta/(?P<date>)', echarts_eachSta, name='eachSta'),
    # import数据模块
    url('load_dataoftrip', load_dataoftrip, name='load_data'),
    url('load_dataofworkday', load_dataofworkday, name='load_dataofworkday'),
    url('load_dataofuser', load_dataofuser, name='load_dataofuser'),
    url('load_dataofstation', load_dataofstation, name='load_dataofstation')
]
