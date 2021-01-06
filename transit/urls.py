# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: urls.py
# @Author  : CNPolaris

# 引入path
from django.urls import path, re_path

# 正在部署的应用的名称
from transit import views
from .views import echarts_data_month, echarts_data_user

app_name = 'transit'

urlpatterns = [
    # path将url映射到视图
    path('index/', views.index, name='index'),
    # path('index-data/', views.index_data, name='index-data'),
    path('echarts/data_month.json', echarts_data_month, name='data_month'),
    path('echarts/data_user_age.json', echarts_data_user, name='user_age')
]
