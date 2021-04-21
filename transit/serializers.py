# -*- coding: utf-8 -*-
# @Time    : 2021/4/21 9:33
# @FileName: serializers.py
# @Author  : CNPolaris

from rest_framework import serializers
from transit.models import Users, Station, Workdays, Trips


class PassengerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'dist', 'birth', 'gender']


class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class WorkdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Workdays
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = '__all__'
