# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: forms.py
# @Author  : CNPolaris
"""
创建表单
"""
from django import forms
# 引入行程model
from .models import Trips


# 行程的表单类
class TripsForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = Trips
        # 定义表单包含的字段
        fields = ('In_name', 'In_time', 'Out_name', 'Out_time', 'Channel_id', "Price")
