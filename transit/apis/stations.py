# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 9:11
# @FileName: stations.py
# @Author  : CNPolaris
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import jwt_decode_handler

from userprofile.models import Profile

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
    sid = request.params.get('station_id', None)
    name = request.params.get('station_name', None)
    route = request.params.get('station_route', None)
    area = request.params.get('admin_area', None)
    # 要获取的第几页
    pagenum = request.params.get('page', 1)
    context = {'code': 2000}
    sort = request.params.get('sort', 'station_id')
    querySet = Station.objects.all()
    # 每页要显示的多少条记录
    pagelimit = 50
    # 主键id在路由中则直接能够查询唯一结果
    if sid:
        querySet = querySet.filter(station_id=sid).values()
        if querySet is not None:
            # paginator = Paginator(querySet.values(), pagelimit)
            # page = paginator.page(pagenum)
            context['code'] = 2000
            context['data'] = list(querySet)
            # total指定一共有多少页数据
            # context['total'] = paginator.count
        else:
            context['code'] = 1000
            context['message'] = "不存在该id为{}的站点".format(sid)
        return JsonResponse(context)
    elif name:
        try:
            querySet = querySet.filter(station_name=name).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "不存在站点名为{}的站点信息".format(name)
        except BaseException as e:
            context['code'] = 1000
            context['message'] = "通过站点名{}查询出现错误".format(name)
        return JsonResponse(context)
    elif route:
        try:
            route = "{}号线".format(route)
            querySet = querySet.filter(station_route=route).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "{}线路上没有站点".format(route)
        except BaseException:
            context['code'] = 1000
            context['message'] = "通过站点查询存在错误"
        return JsonResponse(context)
    elif area:
        try:
            querySet = querySet.filter(admin_area=area).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "{}行政区域没有站点".format(area)
        except BaseException:
            context['code'] = 1000
            context['message'] = "通过行政区域查询记录出现错误"
        return JsonResponse(context)
    else:
        paginator = Paginator(querySet.values().order_by(sort), pagelimit)
        page = paginator.page(pagenum)
        context['code'] = 2000
        context['data'] = list(page)
        # total指定一共有多少页数据
        context['total'] = paginator.count
    return JsonResponse(context)


def data_valid(**kwargs):
    """
    用来代替不能使用表单类的情况下数据的验证器
    :param data:
    :return: Bool
    """
    for key in _FIELDS:
        try:
            if kwargs[key] is None:
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
    context = {'code': 1000}
    # 提取数据
    station_id = request.params.get('station_id', None)
    station_name = request.params.get('station_name', None)
    station_route = request.params.get('station_route', None)
    admin_area = request.params.get('admin_area', None)
    if data_valid(station_id, station_route, station_name, admin_area) is True:
        new_station = Station(station_id=station_id,
                              station_name=station_name,
                              station_route=station_route,
                              admin_area=admin_area
                              )
        try:
            new_station.save()
            context['code'] = 2000
        except BaseException as e:
            context['code'] = 1000
            context['message'] = 'station_id为{}的站点已经存在，出现错误{}'.format(station_id, e)
    else:
        context['code'] = 1000
        context['message'] = "表单不全"
    return JsonResponse(context)


def modify_station(request):
    """
    修改记录
    :param request: PUT/json
    :return:json
    """
    context = {'code': 1000}
    sid = request.params['station_id']
    station = Station.objects.get(station_id=sid)
    if station:
        # 提取数据
        station_name = request.params.get('station_name', None)
        station_route = request.params.get('station_route', None)
        admin_area = request.params.get('admin_area', None)
        if station_name:
            station.station_name = station_name
        if station_route:
            station.station_route = station_route
        if admin_area:
            station.admin_area = admin_area
        station.save()
        context['code'] = 2000
        context['message'] = "修改成功"
    return JsonResponse(context)


def delete_station(request):
    """
    删除记录
    :param request: DELETE/json
    :return: json
    """
    context = {'code': 1000}
    sid = request.params['station_id']
    try:
        station = Station.objects.get(station_id=sid)
        station.delete()
        context['code'] = 2000
        context['message'] = 'id为{}的记录删除成功'.format(sid)
    except BaseException:
        context['code'] = 1000
        context['message'] = 'id为{}的记录不存在'.format(sid)
        return JsonResponse(context)
    return JsonResponse(context)


def dispatcher(request):
    """
    根据http请求的类型和请求体中的参数进行业务分发
    :param request:
    :return:json
    """
    token = request.GET.get('token')
    toke_user = jwt_decode_handler(token)
    user_id = toke_user["user_id"]
    user = User.objects.get(id=user_id)
    if user:
        if Profile.objects.filter(user_id=user_id).exists():
            profile = Profile.objects.get(user_id=user_id)

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

            if profile.roles != 'admin':
                if action == 'list_station':
                    return list_station(request)

            elif profile.roles == 'admin':
                if action == 'list_station':
                    return list_station(request)
                elif action == 'add_station':
                    return add_station(request)
                elif action == 'modify_station':
                    return modify_station(request)
                elif action == 'del_station':
                    return delete_station(request)
                else:
                    return JsonResponse({'code': 1000, 'message': '不支持该类型http请求'})
    else:
        return JsonResponse({
            'code': 1000,
            'message': "无权修改"
        })
