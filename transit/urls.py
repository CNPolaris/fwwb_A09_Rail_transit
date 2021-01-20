# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:48
# @FileName: urls.py
# @Author  : CNPolaris

# 引入path
from django.conf.urls import url, include
# 正在部署的应用的名称
from transit import views
from .echarts import (get_month_flow, get_passengerAge_struct, get_daily_year, get_station_date, get_station_now, get_oneday_flow, get_peak_station)
from .imports import load_dataoftrip, load_dataofstation, load_dataofuser, load_dataofworkday
from .list import ListModelView
from transit.edit import NewModelView

app_name = 'transit'
accounts_urls = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done,
        name='password_change_done'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done,
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset, name='password_reset_confirm'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_complete'),
]

echarts_api_urls = [
    # 单月客流
    url(r'^echarts/data/monthflow/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', get_month_flow, name='monthflow'),
    url(r'^echarts/data/onedayflow/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', get_oneday_flow, name='onedayflow'),
    # 用户年龄结构
    url('echarts/data/agestruct', get_passengerAge_struct, name='agestruct'),
    # 每日客流量
    url('^echarts/data/dailyflow.json/(?P<year>[0-9]{4})/$', get_daily_year, name='dailyflow'),
    # 单站的点出/入站客流分析
    url('^echarts/data/singlesta/(?P<station>)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', get_station_date, name='singlestaion'),
    # 每天所有站点的进出入站点的次数
    url('^echarts/data/eachSta/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', get_station_now, name='eachSta'),
    # 高峰期站点客流压力
    url('^echarts/data/peak/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<hour>[0-9]{2})/$', get_peak_station, name="get_peak_station"),
]
urlpatterns = [
    # 首页路由
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^accounts/', include(accounts_urls)),
    # 向echarts提供数据的api
    url(r'^api/', include(echarts_api_urls)),
    url(r'^(?:list/(?P<model>\w+))/$', ListModelView.as_view(), name='list'),
    url(r'^(?:new/(?P<model>\w+))/$', NewModelView.as_view(), name='new'),

    # import数据模块
    url('load_dataoftrip', load_dataoftrip, name='load_data'),
    url('load_dataofworkday', load_dataofworkday, name='load_dataofworkday'),
    url('load_dataofuser', load_dataofuser, name='load_dataofuser'),
    url('load_dataofstation', load_dataofstation, name='load_dataofstation')
]
