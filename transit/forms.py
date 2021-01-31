# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: forms.py
# @Author  : CNPolaris
"""
创建表单
"""
from django import forms
# 引入行程model
from .models import Trips, Station, Users, TripStatistics, Workdays


# 行程的表单类
class TripsNewForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = Trips
        # 定义表单包含的字段
        fields = ('in_station', 'in_station_time', 'out_station', 'out_station_time', 'channel', "price")


class StationNewForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ('station_id', 'station_name', 'station_route', 'admin_area')


class UsersNewForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('user_id', 'dist', 'birth', 'gender')


class WorkdaysNewForm(forms.ModelForm):
    class Meta:
        model = Workdays
        fields = ('date', 'date_class')


class TripStatisticsNewForm(forms.ModelForm):
    class Meta:
        model = TripStatistics
        fields = ('date', 'count')
