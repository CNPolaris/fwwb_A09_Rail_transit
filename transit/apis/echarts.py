# -*- coding: utf-8 -*-
# @Time    : 2021/1/10 10:19
# @FileName: echarts.py
# @Author  : CNPolaris
import calendar
import json


from transit.models import Trips, Users, Workdays, Station, TripStatistics
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
import datetime
import pandas as pd
from rest_framework_jwt.serializers import jwt_decode_handler
from django.contrib.auth.models import User
from userprofile.models import Profile
from ..units.verify import verify_permissions
"""
向echarts绘制图形提供数据集的api
"""
TIME_LIST = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
             16, 17, 18, 19, 20, 21, 22, 23]


def monthly_flow(request):
    """
    根据具体的date来获取当月的整体客流波动情况
    :param request: GET /api/echarts/month?action=list_month&date=2020-01 HTTP/1.1
    :return: json
    """
    context = {'ret': 0}
    date = request.params['date']
    querySet = TripStatistics.objects.filter(date__contains=date).order_by('date').values(
        'date',
        'count')
    if querySet:
        context['data'] = list(querySet)
    else:
        context['ret'] = 1
        context['msg'] = "{}客流量为空".format(date)
    return JsonResponse(context)


def all_month_flow(request):
    """
    返回当前年的所有月份的客流量
    :param request: GET /api/charts/flow/month HTTP/1.1
    :return:
    """
    flag, request = verify_permissions(request)
    context = {}
    if flag:
        year = request.params.get('year', None)
        month = request.params.get('month', None)
        if year is None:
            year = datetime.date.today().year - 1
        year = int(year) - 1
        querySet = TripStatistics.objects.filter(date__contains=year)
        if month:
            querySet = querySet.filter(date_month__contains=month)
        if querySet:
            month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            data = []
            for m in month:
                tempSet = querySet.filter(date__contains="{}-{}".format(year, m)).values('count')
                total = 0
                for t in tempSet:
                    total = total + t['count']
                data.append(total)
            context['code'] = 2000
            context['month'] = month
            context['data'] = data
        else:
            context['code'] = 1000
            context['message'] = "年月度客流量数据不存在"
    else:
        context['code'] = 1000
        context['message'] = "年月度客流量数据不存在"

    return JsonResponse(context)


@csrf_exempt
def get_month_flow(request):
    """
    单月整体客流情况分析业务转发器
    :param request:GET /api/echarts/month?action=list_month&date=2020-01 HTTP/1.1
    :return: json
    """
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': 'sign.html'
        }, status=302)
    if request.method == 'GET':
        request.params = request.GET
        action = request.params.get('action', None)
        date = request.params.get('date', None)
        year = request.params.get('date', None)
        if action == 'list_month' and date:
            return monthly_flow(request)
        elif year or (action and date is None):
            return all_month_flow(request)
        else:
            return JsonResponse({'ret': 1, 'msg': "不支持该类型的http请求"})
    else:
        return JsonResponse({'ret': 1, 'msg': "不支持该类型的http请求"})


def daily_flow(request):
    """
    返回具体date的客流量
    :param request:GET /api/echarts/daily?action=list_daily&date=2020-01-01
    :return: json
    """
    date = request.params['date']
    context = {'ret': 0}
    querySet = TripStatistics.objects.filter(date=date).values('date', 'count')
    if querySet:
        context['data'] = list(querySet)
    else:
        context['ret'] = 1
        context['msg'] = "{}的客流量为空".format(date)
    return JsonResponse(context)


def list_daily(request):
    """
    列出所有日期的当日客流量
    :param request: GET /api/echarts/daily?action=list_daily
    :return: json
    """
    context = {'ret': 0}
    querySet = TripStatistics.objects.values()
    if querySet:
        context['data'] = list(querySet)
    else:
        context['ret'] = 1
        context['msg'] = "获取数据失败"
    return JsonResponse(context)


@csrf_exempt
def get_daily_flow(request):
    """
    查询某一天的出行量业务分发器
    :param request: GET /api/echarts/daily?action=list_daily
    :return: json
    """
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': 'sign.html'
        }, status=302)

    if request.method == "GET":
        request.params = request.GET
        action = request.params.get('action', None)
        date = request.params.get('date', None)
        if action == 'list_daily' and date:
            return daily_flow(request)
        elif action and date is None:
            return list_daily(request)
        else:
            return JsonResponse({'ret': 1, 'msg': "不支持该类型的http访问"})


@csrf_exempt
def get_age_struct(request):
    """
    用户年龄结构分析
    :param request:GET /api/charts/passenger/age?action=age_struct
    :return: Json
    age: 用户年龄的分组
    count: 不同年龄段的用户数量
    """
    # if 'usertype' not in request.session:
    #     return JsonResponse({
    #         'ret': 302,
    #         'msg': '未登录',
    #         'redirect': 'sign.html'
    #     }, status=302)
    token = request.GET.get('token')
    toke_user = jwt_decode_handler(token)
    user_id = toke_user["user_id"]
    user = User.objects.get(id=user_id)

    if user and Profile.objects.filter(user_id=user_id).exists():
        context = {'code': 2000}
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
        else:
            context['code'] = 1000
            context['message'] = "年龄组成结构查询结果为空"
            return JsonResponse(context)
        data = []
        for s, c in zip(stage, count):
            data.append({'name': s, 'value': c})
        # 向前端返回的数据
        context['code'] = 2000
        context['data'] = data
        context['name'] = stage
        return JsonResponse(context)

    else:
        return JsonResponse({'code': 1000, 'message': '未登录用户无访问权限'})


# if request.method == 'GET':
#         request.params = request.GET
#         action = request.params.get('action', None)
#         if action is not None and action == 'age_struct':
#             context = {'ret': 0}
#             User_list = Users.objects.values_list('birth').annotate(Count("user_id"))
#             # 记录不同年龄段的个数
#             count = [0, 0, 0, 0, 0]
#             stage = ["0-6", "7-17", "18-40", "41-65", "66+"]
#             # 获取互联网时间的年份
#             This_year = datetime.date.today().year
#             if User_list:
#                 for line in User_list:
#                     # 当前的日期减去用户的出生年
#                     age = This_year - line[0]
#                     if 0 <= age < 7:
#                         count[0] = count[0] + line[1]
#                     elif 7 <= age < 18:
#                         count[1] = count[1] + line[1]
#                     elif 18 <= age < 41:
#                         count[2] = count[2] + line[1]
#                     elif 41 <= age < 66:
#                         count[3] = count[3] + line[1]
#                     elif 66 <= age:
#                         count[4] = count[4] + line[1]
#             else:
#                 context['ret'] = 1
#                 context['msg'] = "年龄组成结构查询结果为空"
#                 return JsonResponse(context)
#             data = []
#             for s, c in zip(stage, count):
#                 data.append({'name': s, 'value': c})
#             # 向前端返回的数据
#             context['data'] = data
#             context['name'] = stage
#             return JsonResponse(context)
#         return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})
#     else:
#         return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


@csrf_exempt
def get_station_date(request):
    """
    该api提供查询具体到某站某天24时刻的出入客流
    :param request:GET
    :return:json
    """
    if request.method == 'GET':
        context = {
            'hour_list': [],
            'in_list': [],
            'out_list': []
        }
        # # 使用Q语句通过或条件筛选出进站或出站是所查询station的集合
        # Sta_in_list = Trips.objects.filter(in_station=station,
        #                                    in_station_time__contains='{}-{}-{}'.format(year, month, day)).values(
        #     'in_station_time')
        # Sta_out_list = Trips.objects.filter(out_station=station,
        #                                     out_station_time__contains='{}-{}-{}'.format(year, month, day)).values(
        #     'out_station_time')
        # if Sta_in_list and Sta_out_list:
        #     hour_dict_in = dict(zip(list(range(0, 24)), [0] * 24))
        #     hour_dict_out = dict(zip(list(range(0, 24)), [0] * 24))
        #
        #     in_list = pd.value_counts([int(i['in_station_time'].strftime('%H')) for i in Sta_in_list]).to_dict()
        #     out_list = pd.value_counts([int(i['out_station_time'].strftime('%H')) for i in Sta_out_list]).to_dict()
        #     for i, o in zip(in_list.keys(), out_list.keys()):
        #         hour_dict_in[i] = in_list[i]
        #         hour_dict_out[o] = out_list[o]
        #     context = {
        #         'hour_list': list(range(0, 23)),
        #         'in_list': [i for i in hour_dict_in.values()],
        #         'out_list': [i for i in hour_dict_out.values()]
        #     }
        #     return JsonResponse(context)
        # else:
        #     return JsonResponse(context)


@csrf_exempt
def get_station_now(request):
    """
    实时返回当前日期的所有站点的出入站客流压力
    :param request: /api/charts/flow/now
    :return: json
    """
    flag, request = verify_permissions(request)
    context = {}
    if flag:
        year = request.params.get('year', None)
        month = request.params.get('month', None)
        day = request.params.get('day', None)
        year = "2020"
        month = "01"
        day = "01"
        # 在Station中查询所有的station_name
        Station_query_set = Station.objects.values('station_name')
        # 在Trips中查询所有的in_station_time和out_station_time
        In_out_station = Trips.objects.filter(
            in_station_time__contains='{}-{}-{}'.format(year, month, day)).values(
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
            context['code'] = 2000
            context['label'] = station_list
            context['in_list'] = inNum
            context['out_list'] = outNum
            return JsonResponse(context)
        else:
            context['code'] = 1000
            context['message'] = '无法获取数据'
            return JsonResponse(context)
    else:
        context['code'] = 1000
        context['message'] = '无法获取数据'
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


def station_of_point(request):
    """
    站点的点出入客流分析
    :param request: GET /api/echarts/realtime?action=station_of_point
    :return:json
    """
    context = {'ret': 0}
    station = request.params.get('station', None)
    date = request.params.get('date', None)
    if station and date:
        Sta_in_querySet = Trips.objects.filter(in_station=station,
                                               in_station_time__contains=date).values('in_station_time')
        Sta_out_querySet = Trips.objects.filter(out_station=station,
                                                out_station_time__contains=date).values('out_station_time')
        in_dict = pd.value_counts([int(i['in_station_time'].strftime('%H')) for i in Sta_in_querySet]).to_dict()
        out_dict = pd.value_counts([int(i['out_station_time'].strftime('%H')) for i in Sta_out_querySet]).to_dict()
        context['in_list'] = [{'hour': i, 'count': in_dict[i]} for i in TIME_LIST if i in in_dict]
        context['out_list'] = [{'hour': i, 'count': out_dict[i]} for i in TIME_LIST if i in out_dict]

    else:
        context['ret'] = 1
        context['msg'] = "请求消息不全"
    return JsonResponse(context)


def real_time_dispatcher(request):
    """
    实时客流情况分析事务调度器
    :param request: GET /api/echarts/realtime?action=station_of_point
    :return: json
    """
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': 'sign.html'
        }, status=302)

    if request.method == 'GET':
        action = request.GET.get('action', None)
        request.params = json.loads(request.body)
        if action == 'station_of_point':
            return station_of_point(request)
    else:
        return JsonResponse({'ret': 1, 'msg': " 不支持该类型的http请求"})


def list_od(request):
    """
    根据date列出所有站点的OD客流
    :param request:
    :return:json
    """
    context = {'ret': 0}
    date = request.params['date']
    station = request.params.get('station', None)
    if station is not None:
        Trips_querySet = Trips.objects.filter(Q(in_station=station) | Q(out_station=station),
                                              Q(in_station_time__contains=date) | Q(
                                                  out_station_time__contains=date)).values("in_station", "out_station")
    else:
        Trips_querySet = Trips.objects.filter(
            Q(in_station_time__contains=date) | Q(out_station_time__contains=date)).values("in_station", "out_station")
    if Trips_querySet:
        od = list(Trips_querySet)
        od_dict = pd.value_counts(od)
        context['data'] = [{"in_station": i[0]["in_station"], "out_station": i[0]["out_station"], "count": i[1]} for i
                           in od_dict.items()]
    else:
        context['ret'] = 1
        context['msg'] = "站点信息为空"
    return JsonResponse(context)


@csrf_exempt
def get_OD_station(request, **kwargs):
    """
    获取站点的OD客流
    :param request:GET /api/echarts/od?action=list_od
    :param kwargs:
    :return:
    """
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': 'sign.html'
        }, status=302)

    if request.method == "GET":
        request.params = json.loads(request.body)
        action = request.params.get('action', None)
        date = request.params.get('date', None)
        if action == 'list_od' and date:
            return list_od(request)
        else:
            return JsonResponse({'ret': 1, 'msg': "不支持该类型的http访问"})
    else:
        return JsonResponse({'ret': 1, 'msg': "不支持该类型的http访问"})


def get_route_section(request):
    """
    获取时间端内的指定线路的各站点的断面客流
    :param request: GET /api/charts/route/section
    :return: json
    目标数据图 https://echarts.apache.org/examples/zh/editor.html?c=bar-brush
    """
    # 验证权限
    flag, request = verify_permissions(request)
    # 存储返回数据
    context = {}
    tripSet = Trips.objects.all()
    if flag:
        # 获取指定的线路
        route = request.params.get('route', None)
        date = request.params.get('date', None)
        # TODO:测试时使用的指定数据
        date = '2020-01-01'
        if route and not date:
            route = '{}号线'.format(route)
            station_list = Station.objects.filter(station_route=route).values('station_name')
            station_list = [i['station_name'] for i in station_list]
            context['station'] = station_list

            station_dict = dict(zip(station_list, [0] * len(station_list)))
            tripSet = tripSet.filter(Q(in_station__in=station_list) | Q(out_station__in=station_list)).values(
                'in_station', 'out_station')

            context['code'] = 2000

            in_list = station_dict
            in_dict = pd.value_counts([i['in_station'] for i in tripSet]).to_dict()

            out_list = station_dict
            out_dict = pd.value_counts([i['out_station'] for i in tripSet]).to_dict()

            for s in station_dict.keys():
                if s in in_dict.keys():
                    in_list[s] = in_dict[s]

                if s in out_dict.keys():
                    out_list[s] = out_dict[s]

            in_list = list(in_list.values())
            out_list = list(out_list.values())

            context['in_list'] = in_list
            context['out_list'] = out_list

        elif route and date:
            route = '{}号线'.format(route)

            station_list = Station.objects.filter(station_route=route).values('station_name')
            station_list = [i['station_name'] for i in station_list]
            context['station'] = station_list
            station_dict = dict(zip(station_list, [0] * len(station_list)))

            trip_querySet = tripSet.filter(Q(in_station__in=station_list) | Q(out_station__in=station_list),
                                           Q(in_station_time__contains=date) | Q(
                                               out_station_time__contains=date)).values('in_station', 'out_station')

            context['code'] = 2000

            in_list = station_dict
            in_dict = pd.value_counts([i['in_station'] for i in trip_querySet]).to_dict()

            out_list = station_dict
            out_dict = pd.value_counts([i['out_station'] for i in trip_querySet]).to_dict()

            for s in station_dict.keys():
                if s in in_dict.keys():
                    in_list[s] = in_dict[s]

                if s in out_dict.keys():
                    out_list[s] = out_dict[s]

            in_list = list(in_list.values())
            out_list = list(out_list.values())

            context['in_list'] = in_list
            context['out_list'] = out_list

        else:
            context['code'] = 1000
            context['message'] = '请携带线路访问'
    else:
        context['code'] = 1000
        context['message'] = '无法获取站点的断面客流'

    return JsonResponse(context)


def get_channel_statistics(request):
    """
    统计当天的不同购票方式的出行量
    :param request: GET /api/charts/channel
    :return: json
    """
    flag, request =verify_permissions(request)
    context = {}
    if flag:
        date = request.params.get('date', None)
        # TODO:测试时使用的指定数据
        date = '2020-01-01'
        if date:
            trip_querySet = Trips.objects.filter(in_station_time__contains=date).values('channel')
            channel_dict = pd.value_counts([i['channel']for i in trip_querySet]).to_dict()
            data = []
            for d in channel_dict.keys():
                data.append({"value": channel_dict[d], "name": d})
            context['code'] = 2000
            context['name'] = list(channel_dict.keys())
            context['data'] = data
        else:
            context['code'] = 1000
    else:
        context['code'] = 1000
        context['message'] = '未登录用户无权访问'
    return JsonResponse(context)