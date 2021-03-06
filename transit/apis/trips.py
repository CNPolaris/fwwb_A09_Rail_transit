# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 17:11
# @FileName: trips.py
# @Author  : CNPolaris
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json
from transit.models import Trips, Users, Station
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
import datetime
from rest_framework_jwt.serializers import jwt_decode_handler
from rest_framework_jwt.settings import api_settings

from userprofile.models import Profile

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
    # 每页的限制数
    pagelimit = request.params.get('limit', 40)
    sort = request.params.get('sort')
    context = {'code': 1000}
    querySet = Trips.objects.all()
    # 主键id在路由中则直接能够查询唯一结果
    if id:
        try:
            querySet = querySet.filter(id=id).values()
            context['code'] = 2000
            context['data'] = list(querySet)
            return JsonResponse(context)
        except BaseException as e:
            context['code'] = 1000
            context['message'] = "不存在该id"
            # return JsonResponse(context)
    elif uid:
        querySet = querySet.filter(user_id=uid).values()
        if querySet is not None:
            paginator = Paginator(querySet.values().order_by(sort), pagelimit)
            page = paginator.page(pagenum)
            context['code'] = 2000
            context['data'] = list(page)
            # total指定一共有多少页数据
            context['total'] = paginator.count
        else:
            context['code'] = 1000
            context['message'] = "不存在该乘客的出行记录"
        # return JsonResponse(context)
    elif station:
        try:
            querySet = querySet.filter(Q(in_station=station) | Q(out_station=station)).values().order_by(sort)
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "不存在该站点的出行记录"
        except BaseException as e:
            context['code'] = 1000
            context['message'] = "不存在该站点"
        # return JsonResponse(context)
    elif date:
        try:
            querySet = querySet.filter(Q(in_station_time__contains=date) | Q(out_station_time__contains=date)).values().order_by(sort)
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "不存在该日期的出行记录"
        except BaseException as e:
            context['message'] = "日期查询出行记录存在错误"
        # return JsonResponse(context)
    elif chan:
        try:
            querySet = querySet.filter(channel=chan).values()
            if querySet is not None:
                paginator = Paginator(querySet.values().order_by(sort), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "不存在该乘客的出行记录"
        except BaseException as e:
            context['code'] = 1000
            context['message'] = "通过购票方式查询出行记录出现错误"
        # return JsonResponse(context)
    elif pce:
        try:
            querySet = querySet.filter(price=pce).values()
            if querySet is not None:
                paginator = Paginator(querySet.values().order_by(sort), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "该票价的出行记录为空"
        except BaseException as e:
            context['code'] = 1000
            context['message'] = "通过票价查询出行记录出现错误"
        # return JsonResponse(context)
    else:
        paginator = Paginator(querySet.values().order_by(sort), pagelimit)
        page = paginator.page(pagenum)
        context['code'] = 2000
        context['data'] = list(page)
        # total指定一共有多少页数据
        context['total'] = paginator.count
    return JsonResponse(context)


def data_valid(user_id, in_station, in_station_time, out_station, out_station_time, price, channel):
    """
    用来代替不能使用表单类的情况下数据的验证器
    :return: Bool
    """
    if user_id is None:
        return False
    if in_station is None or not Station.objects.get(station_name=in_station):
        return False
    if in_station_time is None:
        return False
    if out_station is None or Station.objects.get(station_name=out_station):
        return False
    if out_station_time is None:
        return False
    if channel is None or not isinstance(channel, int):
        return False
    if price is None or not isinstance(price, int):
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
    context = {'code': 1000}
    # 提取数据
    user_id = request.params.get('user_id_id')
    in_station = request.params.get('in_station', None)
    in_station_time = request.params.get('in_station_time', None)
    out_station = request.params.get('out_station', None)
    out_station_time = request.params.get('out_station_time', None)
    price = request.params.get('price', None)
    channel = request.params.get('channel', None)

    if data_valid(user_id, in_station, in_station_time, out_station, out_station_time, price, channel) is True:

        new_trip = Trips(in_station=in_station,
                         in_station_time=datetime.datetime.strptime(in_station_time, "%Y-%m-%d %H:%M:%S.%f"),
                         out_station=out_station,
                         out_station_time=datetime.datetime.strptime(out_station_time, "%Y-%m-%d %H:%M:%S.%f"),
                         channel=channel,
                         price=price)
        try:
            new_trip.user_id = Users.objects.get(user_id=user_id)
            new_trip.save()
            context['code'] = 2000
        except BaseException as e:
            context['code'] = 1000
            context['message'] = 'user_id不存在,出现错误{}'.format(e)
            return JsonResponse(context)
        context['id'] = new_trip.id
    else:
        context['code'] = 1000
        context['message'] = "表单不全"
    return JsonResponse(context)


def modify_trip(request):
    """
    修改记录
    :param request: PUT/json
    :return:json
    """
    context = {'code': 1000}
    tid = request.params['id']
    # 查找要修改的数据项
    trip = Trips.objects.get(id=tid)
    if trip:
        # 提取数据
        in_station = request.params.get('in_station', None)
        in_station_time = request.params.get('in_station_time', None)
        out_station = request.params.get('out_station', None)
        out_station_time = request.params.get('out_station_time', None)
        price = request.params.get('price', None)
        channel = request.params.get('channel', None)
        # 修改数据
        if in_station is not None:
            trip.in_station = in_station
        if in_station_time is not None:
            trip.in_station_time = in_station_time
        if out_station is not None:
            trip.out_station = out_station
        if out_station_time is not None:
            trip.out_station_time = out_station_time
        if channel is not None:
            trip.channel = channel
        if price is not None:
            trip.price = price
        # 保存
        trip.save()
    context['code'] = 2000
    context['message'] = "修改成功"
    return JsonResponse(context)


def delete_trip(request):
    """
    删除记录
    :param request: DELETE/json
    :return: json
    """
    context = {'code': 1000}
    tid = request.params['id']
    try:
        trip = Trips.objects.get(id=tid)
        trip.delete()
        context['code'] = 2000
        context['message'] = 'id为{}的记录删除成功'.format(tid)
    except BaseException:
        context['code'] = 1000
        context['message'] = 'id为{}的记录不存在'.format(tid)
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
                if action == 'list_trip':
                    return list_trip(request)

            elif profile.roles == 'admin':
                if action == 'list_trip':
                    return list_trip(request)
                elif action == 'add_trip':
                    return add_trip(request)
                elif action == 'modify_trip':
                    return modify_trip(request)
                elif action == 'del_trip':
                    return delete_trip(request)
                else:
                    return JsonResponse({'code': 1000, 'message': '不支持该类型http请求'})
            else:
                return JsonResponse({
                    'code': 1000,
                    'message': "无权修改"
                })
    else:
        return JsonResponse({
            'code': 1000,
            'message': "无权修改"
        })
