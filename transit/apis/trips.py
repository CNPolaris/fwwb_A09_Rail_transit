# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 17:11
# @FileName: trips.py
# @Author  : CNPolaris
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json
from transit.models import Trips, Users
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
import datetime

_FIELDS = ['user_id', 'in_station', 'in_station_time', 'out_station', 'out_station_time', 'channel', "price"]


@csrf_exempt
def list_trip(request):
    """
    对行程信息进行列表查询，支持多条件查询
    指定查找字段 id，station，date，channel，price, user_id
    :param request:GET
    :return:json
    """
    id = request.GET.get('id', None)
    uid = request.params.get('uid', None)
    station = request.params.get('station', None)
    date = request.params.get('date', None)
    chan = request.params.get('channel', None)
    pce = request.params.get('price', None)
    # 要获取的第几页
    pagenum = request.params.get('page', 1)
    context = {'ret': 0}
    querySet = Trips.objects.all()
    # 每页要显示的多少条记录
    pagelimit = 50
    # 主键id在路由中则直接能够查询唯一结果
    if id:
        try:
            querySet = querySet.get(id=id).values()
            context['retlist'] = list(querySet)
            return JsonResponse(context)
        except BaseException as e:
            print(e)
            context['ret'] = 1
            context['msg'] = "不存在该id"
            return JsonResponse(context)
    elif uid:
        querySet = querySet.filter(user_id=uid).values()
        if querySet is not None:
            paginator = Paginator(querySet.values(), pagelimit)
            page = paginator.page(pagenum)
            context['retlist'] = list(page)
            # total指定一共有多少页数据
            context['total'] = paginator.count
        else:
            context['ret'] = 1
            context['msg'] = "不存在该乘客的出行记录"
        return JsonResponse(context)
    elif station:
        try:
            querySet = querySet.filter(Q(in_station=station) | Q(out_station=station)).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['retlist'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['ret'] = 1
                context['msg'] = "不存在该站点的出行记录"
        except BaseException as e:
            print(e)
            context['ret'] = 1
            context['msg'] = "不存在该站点"
        return JsonResponse(context)
    elif date:
        try:
            querySet = querySet.filter(Q(in_station_time__contains=date) | Q(out_station_time__contains=date)).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['retlist'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['ret'] = 1
                context['msg'] = "不存在该日期的出行记录"
        except BaseException as e:
            context['msg'] = "日期查询出行记录存在错误"
        return JsonResponse(context)
    elif chan:
        try:
            querySet = querySet.filter(channel=chan).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['retlist'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['ret'] = 1
                context['msg'] = "不存在该乘客的出行记录"
        except BaseException as e:
            print(e)
            context['ret'] = 1
            context['msg'] = "通过购票方式查询出行记录出现错误"
        return JsonResponse(context)
    elif pce:
        try:
            querySet = querySet.filter(price=pce).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['retlist'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['ret'] = 1
                context['msg'] = "该票价的出行记录为空"
        except BaseException as e:
            print(e)
            context['ret'] = 1
            context['msg'] = "通过票价查询出行记录出现错误"
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
    fields = ['user_id', 'in_station', 'in_station_time', 'out_station', 'out_station_time', 'channel', "price"]
    for key in fields:
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
def add_trip(request):
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
            for key in ['in_station_time', 'out_station_time']:
                data[key] = datetime.datetime.strptime(data[key], "%Y-%m-%d %H:%M:%S.%f")
            new_trip = Trips(in_station=data['in_station'],
                             in_station_time=data['in_station_time'],
                             out_station=data['out_station'],
                             out_station_time=data['out_station_time'],
                             channel=data['channel'],
                             price=data['price'])
            try:
                new_trip.user_id = Users.objects.get(user_id=data['user_id'])
                new_trip.save()
            except BaseException:
                context['ret'] = 1
                context['msg'] = 'user_id不存在'
                return JsonResponse(context)
            context['id'] = new_trip.id
        else:
            context['ret'] = 1
            context['msg'] = "表单不全"
    else:
        context['ret'] = 1
        context['msg'] = "表单不能为空"
    return JsonResponse(context)


def modify_trip(request):
    """
    修改记录
    :param request: PUT/json
    :return:json
    """
    context = {'ret': 0}
    tid = request.params['id']
    newdata = request.params['newdata']

    try:
        trip = Trips.objects.get(id=tid)
    except BaseException:
        context['ret'] = 1
        context['msg'] = 'id为{}的记录不存在'.format(tid)
        return JsonResponse(context)
    for key in _FIELDS:
        if key in newdata:
            trip[key] = newdata[key]
    trip.save()
    context['ret'] = 0
    return JsonResponse(context)


def delete_trip(request):
    """
    删除记录
    :param request: DELETE/json
    :return: json
    """
    context = {'ret': 0}
    tid = request.params['id']
    try:
        trip = Trips.objects.get(id=tid)
    except BaseException:
        context['ret'] = 1
        context['msg'] = 'id为{}的记录不存在'.format(tid)
        return JsonResponse(context)
    trip.delete()
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
    if action == 'list_trip':
        return list_trip(request)
    elif action == 'add_trip':
        return add_trip(request)
    elif action == 'modify_trip':
        return modify_trip(request)
    elif action == 'del_trip':
        return delete_trip(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})
