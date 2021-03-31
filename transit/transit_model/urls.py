# -*- coding: utf-8 -*-
# @Time    : 2021/3/24 17:35
# @FileName: urls.py
# @Author  : CNPolaris
from django.conf.urls import url, include
from transit.transit_model import predict

predict_urls = [
    url('predict', predict.main),
]
