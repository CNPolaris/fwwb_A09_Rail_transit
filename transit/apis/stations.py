# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 9:11
# @FileName: stations.py
# @Author  : CNPolaris

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json
from transit.models import Station
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage

_FIELDS = ["station_id", "station_name", "station_route", "admin_area"]


@csrf_exempt
def list_station(request):
    """
    对行程信息进行列表查询，支持多条件查询
    指定查找字段 sid，name，route，area，page
    :param request:GET
    :return:json
    """
    sid = request.params.get('sid', None)
    name = request.params.get('name', None)
    route = request.params.get('route', None)
    area = request.params.get('area', None)
    # 要获取的第几页
    pagenum = request.params.get('page', 1)
    context = {'ret': 0}
    querySet = Station.objects.all().order_by('station_id')
    # 每页要显示的多少条记录
    pagelimit = 50
    # 主键id在路由中则直接能够查询唯一结果
    if sid:
        querySet = querySet.filter(station_id=sid).values()
        if querySet is not None:
            paginator = Paginator(querySet.values(), pagelimit)
            page = paginator.page(pagenum)
            context['retlist'] = list(page)
            # total指定一共有多少页数据
            context['total'] = paginator.count
        else:
            context['ret'] = 1
            context['msg'] = "不存在该id为{}的站点".format(sid)
        return JsonResponse(context)
    elif name:
        try:
            querySet = querySet.filter(station_name=name).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['retlist'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['ret'] = 1
                context['msg'] = "不存在站点名为{}的站点信息".format(name)
        except BaseException as e:
            print(e)
            context['ret'] = 1
            context['msg'] = "通过站点名{}查询出现错误".format(name)
        return JsonResponse(context)
    elif route:
        try:
            route = "{}号线".format(route)
            querySet = querySet.filter(station_route=route).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['retlist'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['ret'] = 1
                context['msg'] = "{}线路上没有站点".format(route)
        except BaseException:
            context['msg'] = "通过站点查询存在错误"
        return JsonResponse(context)
    elif area:
        try:
            querySet = querySet.filter(admin_area=area).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['retlist'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['ret'] = 1
                context['msg'] = "{}行政区域没有站点".format(area)
        except BaseException:
            context['ret'] = 1
            context['msg'] = "通过行政区域查询记录出现错误"
        return JsonResponse(context)
    else:
        paginator = Paginator(querySet.values(), pagelimit)
        page = paginator.page(pagenum)
        context['retlist'] = list(page)
        # total指定一共有多少页数据
        context['total'] = paginator.count
    return JsonResponse(context)


def data_valid(data):
    """
    用来代替不能使用表单类的情况下数据的验证器
    :param data:
    :return: Bool
    """
    for key in _FIELDS:
        try:
            if data[key] is None:
                return False
            else:
                return True
        except BaseException as e:
            print(e)
            return False
    return True


@csrf_exempt
def add_station(request):
    """
    增加数据
    :param request: POST/json
    :return: json
    """
    # TODO:还是希望通过表单类来实现数据添加
    context = {'ret': 0}
    data = request.params.get("data", None)
    if data is not None:
        if data_valid(data) is True:
            new_station = Station(station_id=data['station_id'],
                                  station_name=data['station_name'],
                                  station_route=data['station_route'],
                                  admin_area=data['admin_area'],
                                  )
            try:
                new_station.save()
            except BaseException:
                context['ret'] = 1
                context['msg'] = 'station_id为{}的站点已经存在'.format(data['sid'])
                return JsonResponse(context)
            context['id'] = new_station.station_id
        else:
            context['ret'] = 1
            context['msg'] = "表单不全"
    else:
        context['ret'] = 1
        context['msg'] = "表单不能为空"
    return JsonResponse(context)


def modify_station(request):
    """
    修改记录
    :param request: PUT/json
    :return:json
    """
    context = {'ret': 0}
    sid = request.params['sid']
    newdata = request.params['newdata']

    try:
        station = Station.objects.get(station_id=sid)
    except BaseException:
        context['ret'] = 1
        context['msg'] = 'id为{}的记录不存在'.format(sid)
        return JsonResponse(context)
    if 'station_name' in newdata:
        station.station_name = newdata['station_name']
    if 'station_route' in newdata:
        station.station_route = newdata['station_route']
    if 'admin_area' in newdata:
        station.admin_area = newdata['admin_area']
    station.save()
    context['ret'] = 0
    return JsonResponse(context)


def delete_station(request):
    """
    删除记录
    :param request: DELETE/json
    :return: json
    """
    context = {'ret': 0}
    sid = request.params['sid']
    try:
        station = Station.objects.get(station_id=sid)
    except BaseException:
        context['ret'] = 1
        context['msg'] = 'id为{}的记录不存在'.format(sid)
        return JsonResponse(context)
    station.delete()
    return JsonResponse(context)


def dispatcher(request):
    """
    根据http请求的类型和请求体中的参数进行业务分发
    :param request:
    :return:json
    """
    # 将请求参数统一放在request的params属性中，方便后续处理
    # GET请求 参数在url中，通过request对象的GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数从request对象的body属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_station':
        return list_station(request)
    elif action == 'add_station':
        return add_station(request)
    elif action == 'modify_station':
        return modify_station(request)
    elif action == 'del_station':
        return delete_station(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})
