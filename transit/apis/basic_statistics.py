# -*- coding: utf-8 -*-
# @Time    : 2021/3/17 15:57
# @FileName: basic_statistics.py
# @Author  : CNPolaris

from transit.models import Trips, Users, Workdays, Station, TripStatistics
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from ..units import verify


def get_in_station(request):
    """
    获取当前在站点内的总人数
    :param request: /api/charts/allin
    :return: get
    """
    flag, request = verify.verify_permissions(request)
    context = {}
    if flag:
        date = request.params.get('date', None)
        # TODO：这里为了保证测试时可以使用，指定了数据
        date = '2020-01-01'
        if date:
            trip_querySet_count = Trips.objects.filter(in_station_time__lte=date, out_station_time__gt=date).count()
            context['code'] = 2000
            context['data'] = trip_querySet_count

        else:
            context['code'] = 1000
            context['data'] = 0
            context['message'] = "获取数据失败"
    else:
        context['code'] = 1000
        context['message'] = "未登录用户无法访问"
    return JsonResponse(context)


def get_historical_travel(request):
    """
    获取历史出行总量
    :param request:/api/charts/historical/travel
    :return: json
    """
    flag, request = verify.verify_permissions(request)
    context = {}
    if flag:
        date = request.params.get('date', None)
        # TODO：这里为了保证测试时可以使用，指定了数据
        date = '2020-01-01'
        trip_QuerySet = Trips.objects.all()
        context['code'] = 2000
        context['endVal'] = trip_QuerySet.count()
        if date:
            trip_QuerySet = trip_QuerySet.filter(in_station_time__contains=date)
            context['endValNow'] = trip_QuerySet.count()
        else:
            context['endValNow'] = 0
    else:
        context['code'] = 1000
        context['message'] = '未登录用户无法访问'
    return JsonResponse(context)


def get_today_income(request):
    """
    获取当日营运额
    :param request: /api/charts/today/income
    :return: json
    """
    flag, request = verify.verify_permissions(request)
    context = {}
    if flag:
        date = request.params.get('date', None)
        # TODO：这里为了保证测试时可以使用，指定了数据
        date = '2020-01-01'
        if date:
            trip_querySet = Trips.objects.filter(in_station_time__contains=date).values('price')
            if trip_querySet:
                today_income = trip_querySet.aggregate(income=Sum('price'))
                context['code'] = 2000
                context['income'] = today_income['income']
            else:
                context['code'] = 2000
                context['income'] = 0
            return JsonResponse(context)
        else:
            context['income'] = 0
    else:
        context['code'] = 1000
        context['message'] = '未登录用户无法访问'
    return JsonResponse(context)
