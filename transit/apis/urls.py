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
    url('^charts/od', echarts.get_OD_station),
    # 断面客流
    url('charts/route/section', echarts.get_route_section),
    # 不同购票渠道的统计
    url('charts/channel', echarts.get_channel_statistics),
    # 站点的点出入客流
    url('charts/flow/point', echarts.get_station_of_point),
    # 工作日客流分析
    url('charts/week', echarts.get_work_week),
    # 高峰期客流分析
    url('charts/peak', echarts.get_peak_period),
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
    # 基础数据统计url
    url(r'basic/', include(basic_statistics_urls))
]
