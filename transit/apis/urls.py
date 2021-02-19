# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 22:49
# @FileName: urls.py
# @Author  : CNPolaris
from django.conf.urls import url, include
from transit.apis import trips, stations, workdays, users, sign_in_out
from transit.apis import echarts, exports
echarts_api_urls = [
    # 单月客流
    url(r'^echarts/month', echarts.get_month_flow),
    # 单日客流量
    url(r'^echarts/daily', echarts.get_daily_flow),
    # 用户年龄结构
    url('echarts/agestruct', echarts.get_age_struct),
    # 实时客流数据
    url(r'^echarts/realtime', echarts.real_time_dispatcher),
    # 站点的OD客流分析
    url('^echarts/od', echarts.get_OD_station, name="get_OD_station"),
    # url('^echarts/data/dailyflow.json/(?P<year>[0-9]{4})/$', get_daily_year, name='dailyflow'),
    # # 单站的点出/入站客流分析
    # url('^echarts/data/singlesta/(?P<station>)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
    #     get_station_date, name='singlestaion'),
    # # 每天所有站点的进出入站点的次数
    # url('^echarts/data/eachSta/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', get_station_now,
    #     name='eachSta'),
    # # 高峰期站点客流压力
    # url('^echarts/data/peak/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<hour>[0-9]{2})/$',
    #     get_peak_station, name="get_peak_station"),

]

api_urls = [
    # 登录登出
    url(r'^signin', sign_in_out.signin),
    url(r'^signout', sign_in_out.signout),
    # excel导出
    url(r'exports', exports.download),
    # model基础数据管理
    url(r'manager/trips', trips.dispatcher),
    url(r'manager/station', stations.dispatcher),
    url(r'manager/workday', workdays.dispatcher),
    url(r'manager/passenger', users.dispatcher)
]
