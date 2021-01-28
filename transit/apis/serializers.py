# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 22:03
# @FileName: serializers.py
# @Author  : CNPolaris
from transit import models
from rest_framework import serializers

"""
序列化器
"""


class TripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trips
        fields = "__all__"


class TripStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TripStatistics
        fields = "__all__"


class WorkdaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workdays
        fields = "__all__"


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = "__all__"
