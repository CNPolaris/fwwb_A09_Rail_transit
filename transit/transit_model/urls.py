# -*- coding: utf-8 -*-
# @Time    : 2021/3/24 17:35
# @FileName: urls.py
# @Author  : CNPolaris
from django.conf.urls import url, include
from transit.transit_model import predict, predict_by_station

predict_urls = [
    url('normal', predict.normal_predict),
    url('station', predict_by_station.predict_station)
]
