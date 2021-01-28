# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 22:49
# @FileName: urls.py
# @Author  : CNPolaris
from django.conf.urls import url, include

from transit.apis import tableView

table_api_urls = [
    url(r'^model/(?P<model>\w+)/$', tableView.AllSetByModel.as_view({"get": "list"})),
    url(r'^get/(?P<model>\w+)/(?P<pk>\w+)', tableView.OneSetByPK.as_view({"get": "search"})),
]
