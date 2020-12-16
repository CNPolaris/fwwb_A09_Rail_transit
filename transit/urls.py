# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: urls.py
# @Author  : CNPolaris

# 引入path
from django.urls import path, re_path

# 正在部署的应用的名称
from transit import views

app_name = 'transit'

urlpatterns = [
    # path将url映射到视图
    path('index/', views.index, name='index'),
    # path('index-data/', views.index_data, name='index-data'),

]
