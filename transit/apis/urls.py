# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 22:49
# @FileName: urls.py
# @Author  : CNPolaris
from django.conf.urls import url, include
from transit.apis import trips, stations, workdays, passenger, user_in_out
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
    # # 登录登出
    # url(r'^login', user_in_out.user_login),
    # url(r'^logout', user_in_out.user_logout),
    # url(r'^user/info', user_in_out.get_user_info),
    # excel导出
    url(r'manage/export', exports.dispatcher),
    # model基础数据管理
    url(r'manage/trip/', include(trip_urls)),
    url(r'manage/station/', include(station_urls)),
    url(r'manage/workday/', include(workday_urls)),
    url(r'manage/passenger/', include(passenger_url))
]
