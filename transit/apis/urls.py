# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 22:49
# @FileName: urls.py
# @Author  : CNPolaris
from django.conf.urls import url, include
from transit.apis import trips, stations, workdays, passenger
from transit.apis import echarts, exports, basic_statistics

echarts_api_urls = [
    # 单月客流
    url('charts/flow/month', echarts.all_month_flow),
    # 单日客流量
    url(r'^echarts/daily', echarts.get_daily_flow),
    # 用户年龄结构
    url('charts/passenger/age', echarts.get_age_struct),
    # 实时客流数据
    url(r'^charts/flow/now', echarts.get_station_now),
    # 站点的OD客流分析
    url('^echarts/od', echarts.get_OD_station, name="get_OD_station"),
    # 断面客流
    url('charts/route/section', echarts.get_route_section),
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
# 基础数据统计
basic_statistics_urls = [
    # 当前在站
    url('in/station', basic_statistics.get_in_station),
    # 历史出行客流总量
    url('historical/travel', basic_statistics.get_historical_travel),
    # 当日营运额
    url('today/income', basic_statistics.get_today_income)
]
trip_urls = [
    url(r'list', trips.dispatcher),
    url(r'create', trips.dispatcher),
    url(r'update', trips.dispatcher),
    url(r'delete', trips.dispatcher)
]
station_urls = [
    url(r'list', stations.dispatcher),
    url(r'create', stations.dispatcher),
    url(r'update', stations.dispatcher),
    url(r'delete', stations.dispatcher),
]
workday_urls = [
    url(r'list', workdays.dispatcher),
    url(r'create', workdays.dispatcher),
    url(r'update', workdays.dispatcher),
    url(r'delete', workdays.dispatcher),
]
passenger_url = [
    url(r'list', passenger.dispatcher),
    url(r'create', passenger.dispatcher),
    url(r'update', passenger.dispatcher),
    url(r'delete', passenger.dispatcher),
]
api_urls = [
    # excel导出
    url(r'manage/export', exports.dispatcher),
    # model基础数据管理
    url(r'manage/trip/', include(trip_urls)),
    url(r'manage/station/', include(station_urls)),
    url(r'manage/workday/', include(workday_urls)),
    url(r'manage/passenger/', include(passenger_url)),
    url(r'basic/', include(basic_statistics_urls))
]
