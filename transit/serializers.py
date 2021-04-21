# -*- coding: utf-8 -*-
# @Time    : 2021/4/21 9:33
# @FileName: serializers.py
# @Author  : CNPolaris

from rest_framework import serializers
from transit.models import Users

class PassengerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'dist', 'birth', 'gender']


