# -*- coding: utf-8 -*-
# @Time    : 2021/1/10 10:19
# @FileName: echarts.py
# @Author  : CNPolaris
from .models import Trips, Users, Workdays, Station, TripStatistics
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.http import JsonResponse
import datetime
import pandas as pd

"""
向echarts绘制图形提供数据集的api
"""


@csrf_exempt
def echarts_monthflow(request, date):
    """
    后端向前端返回json数据
    :param date: 前端使用api时需要带上date数据 如2020-01-01
    :param request:
    :return: json
    key: 某年月日内的所有入站时间
    value: 根据入站时间In_time进行分类统计后的每组对应的数量
    """
    Trips_list_2020 = Trips.objects.filter(in_station_time__contains=date).values_list(
        'in_station_time').annotate(
        Count("id"))
    # date_list = Trips_list_2020.dates('In_time', kind='day')
    context = {
        "key": [i[0] for i in Trips_list_2020],
        "value": [i[1] for i in Trips_list_2020]
    }
    return JsonResponse(context)


@csrf_exempt
def echarts_agestruct(request):
    """
    用户年龄结构分析
    :param request:Get
    :return: Json
    age: 用户年龄的分组
    count: 不同年龄段的用户数量
    """
    User_list = Users.objects.values_list('birth').annotate(Count("user_id"))
    # 年龄阶段分组
    age_stage = [list(range(0, 7)), list(range(7, 18)), list(range(18, 41)), list(range(41, 66))]
    # 记录不同年龄段的个数
    count = [0, 0, 0, 0, 0]
    # 获取互联网时间的年份
    This_year = datetime.date.today().year
    if User_list:
        for line in User_list:
            # 当前的日期减去用户的出生年
            age = This_year - line[0]
            if age in age_stage[0]:
                count[0] = count[0] + line[1]
            elif age in age_stage[1]:
                count[1] = count[1] + line[1]
            elif age in age_stage[2]:
                count[2] = count[2] + line[1]
            elif age in age_stage[3]:
                count[3] = count[3] + line[1]
            else:
                count[4] = count[4] + line[1]
    # 向前端返回的数据
    context = {
        "age": ["0-6", "7-17", "18-40", "41-65", "66+"],
        "count": count
    }
    return JsonResponse(context)


@csrf_exempt
def echarts_dailyflow(request, year):
    """
    每天实时客流量统计
    :param year: web发送请求时所附带的当前年份参数
    :param request: Get
    :return: json
    """
    # 从Tripstatistics中获取每一天的实时出行人数
    EachDay_list = TripStatistics.objects.filter(date__contains=year)
    if EachDay_list:
        each_day = []
        each_day_flow = []
        for line in EachDay_list:
            each_day.append(line.date)
            each_day_flow.append(line.count)
        # api响应的数据
        context = {
            "date": each_day,
            "date_flow": each_day_flow
        }
        return JsonResponse(context)
    else:
        return JsonResponse({})


@csrf_exempt
def echarts_singlesta(request, station, date):
    """
    该api提供查询具体到某站某天24时刻的出入客流
    :param station:
    :param date:
    :param request:
    :return:
    """
    # 使用Q语句通过或条件筛选出进站或出站是所查询station的集合
    Sta_in_list = Trips.objects.filter(in_station=station,
                                       in_station_time__contains=date).values(
        'in_station_time')
    Sta_out_list = Trips.objects.filter(out_station=station, out_station_time__contains=date).values(
        'out_station_time')
    hour_dict_in = dict(zip(list(range(0, 24)), [0] * 24))
    hour_dict_out = dict(zip(list(range(0, 24)), [0] * 24))

    in_list = pd.value_counts([int(i['in_station_time'].strftime('%H')) for i in Sta_in_list]).to_dict()
    out_list = pd.value_counts([int(i['out_station_time'].strftime('%H')) for i in Sta_out_list]).to_dict()
    for i, o in zip(in_list.keys(), out_list.keys()):
        hour_dict_in[i] = in_list[i]
        hour_dict_out[o] = out_list[o]
    context = {
        'hour_list': list(range(0, 23)),
        'in_list': [i for i in hour_dict_in.values()],
        'out_list': [i for i in hour_dict_out.values()]
    }
    return JsonResponse(context)
