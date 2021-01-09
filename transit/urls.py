# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: urls.py
# @Author  : CNPolaris

# 引入path
from django.urls import path, re_path

# 正在部署的应用的名称
from transit import views
from .views import echarts_monthflow, echarts_agestruct, echarts_dailyflow

app_name = 'transit'

urlpatterns = [
    # path将url映射到视图
    path('index/', views.index, name='index'),
    # TODO：目前是所写的api没有加上id等来进行特别识别，需要前端配合form来实现
    # 单月客流
    path('echarts/data/<str:date>/monthflow.json', echarts_monthflow, name='monthflow'),
    # 用户年龄结构
    path('echarts/data/agestruct.json', echarts_agestruct, name='agestruct'),
    # 每日客流量
    path('echarts/data/<int:year>/dailyflow.json', echarts_dailyflow, name='dailyflow'),
    # 单站的点出/入站客流分析
    path('echarts/data/<str:station>/<str:date>/singlesta.json', views.echarts_singlesta, name='singlestaion'),
    path('load_dataoftrip', views.load_dataoftrip, name='load_data'),
    path('load_dataofworkday', views.load_dataofworkday, name='load_dataofworkday'),
    path('load_dataofuser', views.load_dataofuser, name='load_dataofuser'),
    path('load_dataofstation', views.load_dataofstation, name='load_dataofstation')
]
