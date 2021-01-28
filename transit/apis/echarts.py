# -*- coding: utf-8 -*-
# @Time    : 2021/1/10 10:19
# @FileName: echarts.py
# @Author  : CNPolaris
import calendar

from transit.models import Trips, Users, Workdays, Station, TripStatistics
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.http import JsonResponse
import datetime
import pandas as pd

"""
向echarts绘制图形提供数据集的api
"""


@csrf_exempt
def get_month_flow(request, year, month):
    """
    单月整体客流情况分析
    :param date: 前端使用api时需要带上date数据 如2020-01-01
    :param request:
    :return: json
    key: 某年月的所有日期
    value: 对应日期的出行总量
    """
    if request.method == 'GET':
        TripStatistics_query_set = TripStatistics.objects.filter(date__contains='{}-{}'.format(year, month)).values(
            'date',
            'count')
        if TripStatistics_query_set:
            # 该月有多少天
            month_days = calendar.monthrange((int(year)), int(month))[1]
            # 生成日期序列
            date_range = pd.date_range(start='{}/{}/{}'.format(year, month, '01'), periods=month_days)
            date_list = []
            for date in date_range:
                date_list.append(date.strftime("%Y-%m-%d"))
            # 该月的每日出行人数
            month_flow_dict = dict(zip(date_list, [0] * month_days))
            for i in TripStatistics_query_set:
                month_flow_dict[i['date'].strftime("%Y-%m-%d")] = i['count']
            context = {
                "key": list(month_flow_dict.keys()),
                "value": list(month_flow_dict.values())
            }
            return JsonResponse(context)
        else:
            return JsonResponse({
                "key": [],
                "value": []
            })
    else:
        return JsonResponse({
            "key": [],
            "value": []
        })


@csrf_exempt
def get_oneday_flow(request, year, month, day):
    """
    查询某一天的出行量
    :param request: GET
    :param year: str
    :param month: str
    :param day: str
    :return: json
    e.g 2020/01/01
    """
    if request.method == "GET":
        TripStatistics_query_set = TripStatistics.objects.filter(
            date='{}-{}-{}'.format(year, month, day)).values('date', 'count')
        if TripStatistics_query_set:
            context = {
                "key": [i['date'] for i in TripStatistics_query_set],
                "value": [i['count'] for i in TripStatistics_query_set]
            }
            return JsonResponse(context)
        else:
            return JsonResponse({
                "key": [],
                "value": []
            })
    else:
        return JsonResponse({
            "key": [],
            "value": []
        })


@csrf_exempt
def get_passengerAge_struct(request):
    """
    用户年龄结构分析
    :param request:Get
    :return: Json
    age: 用户年龄的分组
    count: 不同年龄段的用户数量
    """
    User_list = Users.objects.values_list('birth').annotate(Count("user_id"))
    # 记录不同年龄段的个数
    count = [0, 0, 0, 0, 0]
    stage = ["0-6", "7-17", "18-40", "41-65", "66+"]
    # 获取互联网时间的年份
    This_year = datetime.date.today().year
    if User_list:
        for line in User_list:
            # 当前的日期减去用户的出生年
            age = This_year - line[0]
            if 0 <= age < 7:
                count[0] = count[0] + line[1]
            elif 7 <= age < 18:
                count[1] = count[1] + line[1]
            elif 18 <= age < 41:
                count[2] = count[2] + line[1]
            elif 41 <= age < 66:
                count[3] = count[3] + line[1]
            elif 66 <= age:
                count[4] = count[4] + line[1]
    data = []
    for s, c in zip(stage, count):
        data.append({'name': s, 'value': c})
    # 向前端返回的数据
    context = {
        "data": data,
        "name": stage
    }
    return JsonResponse(context)


@csrf_exempt
def get_daily_year(request, year):
    """
    一年中每一天的出行量统计
    :param year: web发送请求时所附带的当前年份参数
    :param request: Get
    :return: json
    """
    if request.method == "GET":
        # 从Tripstatistics中获取每一天的实时出行人数
        EachDay_list = TripStatistics.objects.filter(date__contains=year).order_by('date')
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
            return JsonResponse({"date": [], "date_flow": []})
    else:
        return JsonResponse({"date": [], "date_flow": []})


@csrf_exempt
def get_station_date(request, station, year, month, day):
    """
    该api提供查询具体到某站某天24时刻的出入客流
    :param day:
    :param month:
    :param year:
    :param station:
    :param request:
    :return:
    """
    if request.method == 'GET':
        context = {
            'hour_list': [],
            'in_list': [],
            'out_list': []
        }
        # 使用Q语句通过或条件筛选出进站或出站是所查询station的集合
        Sta_in_list = Trips.objects.filter(in_station=station,
                                           in_station_time__contains='{}-{}-{}'.format(year, month, day)).values(
            'in_station_time')
        Sta_out_list = Trips.objects.filter(out_station=station,
                                            out_station_time__contains='{}-{}-{}'.format(year, month, day)).values(
            'out_station_time')
        if Sta_in_list and Sta_out_list:
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
        else:
            return JsonResponse(context)


@csrf_exempt
def get_station_now(request, **kwargs):
    """
    实时返回当前日期的所有站点的出入站客流压力
    :param date: 路由中的日期
    :param request: get
    :return: json
    """
    if request.method == "GET":
        context = {
            'label': [],
            'inNum': [],
            'outNum': []
        }

        # 在Station中查询所有的station_name
        Station_query_set = Station.objects.values('station_name')
        # 在Trips中查询所有的in_station_time和out_station_time
        In_out_station = Trips.objects.filter(
            in_station_time__contains='{}-{}-{}'.format(kwargs['year'], kwargs['month'], kwargs['day'])).values(
            'in_station', 'out_station')
        if Station_query_set and In_out_station:
            # 存储当前系统中的所有站点
            station_list = []
            if Station_query_set:
                station_list = [sta['station_name'] for sta in Station_query_set]
            # 存储进出站的时间
            in_station_list = []
            out_station_list = []
            # 填充
            if In_out_station:
                for d in In_out_station:
                    in_station_list.append(d['in_station'])
                    out_station_list.append(d['out_station'])
            # 保证station_name全面
            station_list = list(set(in_station_list + out_station_list + station_list))
            # 对所有的进出站点进行分类统计了
            in_station_list = pd.value_counts(in_station_list).to_dict()
            out_station_list = pd.value_counts(out_station_list).to_dict()
            # 构成两个进出站字典
            in_station_dict = dict(zip(station_list, [0] * len(station_list)))
            out_station_dict = dict(zip(station_list, [0] * len(station_list)))
            # 根据字典进行数据填充
            for inSta in in_station_list.keys():
                in_station_dict[inSta] = in_station_dict[inSta] + in_station_list[inSta]
            for outSta in out_station_list.keys():
                out_station_dict[outSta] = out_station_dict[outSta] + out_station_list[outSta]
            inNum = [i for i in in_station_dict.values()]
            outNum = [i for i in out_station_dict.values()]
            context = {
                'label': station_list,
                'inNum': inNum,
                'outNum': outNum
            }
            return JsonResponse(context)
        else:
            return JsonResponse(context)


@csrf_exempt
def get_peak_station(request, **kwargs):
    """
    早晚客流高峰期各站点的客流压力分析
    :param request: GET
    :return: json
    目标图表样式：https://echarts.apache.org/examples/zh/editor.html?c=multiple-y-axis
    """
    # TODO: 对station进行排序 使站点列表有序
    if request.method == "GET":
        # 默认返回空数据
        context = {
            "station": [],
            "in_pressure": [],
            "out_pressure": []
        }
        if 7 <= int(kwargs['hour']) <= 9:
            # 时间区间
            Time_interval = ['{}-{}-{} {}'.format(kwargs['year'], kwargs['month'], kwargs['day'], '07:00'), '{}-{}-{} '
                                                                                                            '{}'.format(
                kwargs['year'], kwargs['month'], kwargs['day'], '09:00')]
        elif 17 <= int(kwargs['hour']) <= 19:
            Time_interval = ['{}-{}-{} {}'.format(kwargs['year'], kwargs['month'], kwargs['day'], '15:00'), '{}-{}-{} '
                                                                                                            '{}'.format(
                kwargs['year'], kwargs['month'], kwargs['day'], "17:00")]
        else:
            Time_interval = ['{}-{}-{} 00:00'.format(kwargs['year'], kwargs['month'], kwargs['day']),
                             '{}-{}-{} 23:59'.format(kwargs['year'], kwargs['month'], kwargs['day'])]
        # 站点表
        Station_query_set = Station.objects.values('station_name')
        # 高峰期进站的客流
        Trips_in_set = Trips.objects.filter(in_station_time__range=(Time_interval[0], Time_interval[1])).values(
            "in_station")
        # 高峰期出站的客流
        Trips_out_set = Trips.objects.filter(out_station_time__range=(Time_interval[0], Time_interval[1])).values(
            "out_station")
        if Station_query_set:
            # 站点和站点压力dict
            station_pressure_dict = dict(
                zip([i['station_name'] for i in Station_query_set], [0] * len(Station_query_set)))
            # 进出站点的压力列表
            in_pressure_list = []
            out_pressure_list = []
            if Trips_in_set:
                in_peak_dict = pd.value_counts([i['in_station'] for i in Trips_in_set]).to_dict()
                for station in in_peak_dict:
                    station_pressure_dict[station] = in_peak_dict[station]
                in_pressure_list = list(station_pressure_dict.values())
            if Trips_out_set:
                station_pressure_dict = dict(
                    zip([i['station_name'] for i in Station_query_set], [0] * len(Station_query_set)))
                out_peak_dict = pd.value_counts([i['out_station'] for i in Trips_out_set]).to_dict()
                for station in out_peak_dict:
                    station_pressure_dict[station] = out_peak_dict[station]
                out_pressure_list = list(station_pressure_dict.values())
            context = {
                "station": [i['station_name'] for i in Station_query_set],
                "in_pressure": in_pressure_list,
                "out_pressure": out_pressure_list
            }
        return JsonResponse(context)


@csrf_exempt
def get_OD_station(request, **kwargs):
    """
    获取站点的OD客流
    :param request:
    :param kwargs:
    :return:
    """
    if request.method == "GET":
        context = {
            "station_name": [],
            "station_route": [],
        }
        Station_query_set = Station.objects.all().values("station_name", "station_route")
        if Station_query_set:
            station_name_list = [i["station_name"] for i in Station_query_set]
            station_route_list = [i["station_route"] for i in Station_query_set]
            context["station_name"] = station_name_list
            context["station_route"] = station_route_list
            name_route_dict = dict(zip(station_name_list, station_route_list))
            context["name_route_dict"] = name_route_dict
            Trips_query_set = Trips.objects.filter(in_station_time__contains='2020-01-01').values("in_station",
                                                                                                  "out_station")
            if Trips_query_set:
                od = []
                for i in Trips_query_set:
                    od.append([i["in_station"], i["out_station"]])
                od_dict = pd.value_counts(od)
                context["od"] = [{"begin": i[0][0], "end": i[0][1],
                                  "route": [name_route_dict[i[0][0]], name_route_dict[i[0][1]]],
                                  "value": i[1]
                                  } for i in od_dict.items() if
                                 i[0][0] in name_route_dict.keys() and i[0][1] in name_route_dict.keys()]
        return JsonResponse(context)
