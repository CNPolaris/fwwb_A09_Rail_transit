# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 9:47
# @FileName: workdays.py
# @Author  : CNPolaris
import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json
from transit.models import Workdays
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from rest_framework_jwt.serializers import jwt_decode_handler
from userprofile.models import Profile
from django.contrib.auth.models import User

_FIELDS = ['date', 'date_class']


@csrf_exempt
def list_workday(request):
    """
    对行程信息进行列表查询，支持多条件查询
    指定查找字段 uid，dist，birth，gender，page
    :param request:GET
    :return:json
    """
    date = request.params.get('date', None)
    cls = request.params.get('date_class', None)
    # 要获取的第几页
    pagenum = request.params.get('page', 1)
    pagelimit = request.params.get('limit', 40)

    sort = request.params.get('sort')

    context = {'code': 1000}
    querySet = Workdays.objects.all()
    # 每页要显示的多少条记录
    # 主键id在路由中则直接能够查询唯一结果
    if date:
        querySet = querySet.filter(date=date).values()
        if querySet is not None:
            paginator = Paginator(querySet.values(), pagelimit)
            page = paginator.page(pagenum)
            context['code'] = 2000
            context['data'] = list(page)
            # total指定一共有多少页数据
            context['total'] = paginator.count
        else:
            context['code'] = 1000
            context['message'] = "不存在日期为{}的记录".format(date)
        return JsonResponse(context)
    elif cls:
        try:
            querySet = querySet.filter(date_class=cls).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "不存在节假日属性为{}的记录".format(cls)
        except BaseException as e:
            context['code'] = 1000
            context['message'] = "通过节假日属性{}查询出现错误{}".format(cls, e)
        return JsonResponse(context)
    else:
        paginator = Paginator(querySet.values(), pagelimit)
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
        except BaseException as e:
            print(e)
            return False
    return True


@csrf_exempt
def add_workday(request):
    """
    增加数据
    :param request: POST/json
    :return: json
    """
    # TODO:还是希望通过表单类来实现数据添加
    context = {'code': 1000}
    date = request.params.get('date', None)
    date_class = request.params.get('date_class', None)
    if data_valid(date, date_class) is True:
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
            new_day = Workdays(date=date,
                               date_class=date_class)
            try:
                new_day.save()
                context['code'] = 2000
            except BaseException as e:
                context['code'] = 1000
                context['message'] = '保存失败{}'.format(e)
                return JsonResponse(context)
        except BaseException as e:
            context['code'] = 1000
            context['message'] = '数据格式不正确{}'.format(e)
    else:
        context['code'] = 1000
        context['message'] = "表单不全或数据格式不正确"
    return JsonResponse(context)


def modify_workday(request):
    """
    修改记录
    :param request: PUT/json
    :return:json
    """
    context = {'code': 1000}
    date = request.params['date']
    date_class = request.params.get('date_class', None)
    try:
        workday = Workdays.objects.get(date=date)
        if date_class in [1, 2, 3]:
            workday.date_class = date_class
            workday.save()
            context['code'] = 2000
    except BaseException as e:
        context['code'] = 1000
        context['message'] = '日期为{}的记录不存在,出现错误{}'.format(date,e)
        return JsonResponse(context)
    else:
        context['code'] = 1000
        context['message'] = "日期属性{}不合规范".format(date_class)
    return JsonResponse(context)


def delete_workday(request):
    """
    删除记录
    :param request: DELETE/json
    :return: json
    """
    context = {'code': 1000}
    date = request.params['date']
    try:
        workday = Workdays.objects.get(date=date)
        workday.delete()
        context['code'] = 2000
    except BaseException as e:
        context['code'] = 1000
        context['message'] = '删除失败，{}'.format(e)
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
                if action == 'list_workday':
                    return list_workday(request)
            elif profile.roles == 'admin':
                if action == 'list_workday':
                    return list_workday(request)
                elif action == 'add_workday':
                    return add_workday(request)
                elif action == 'modify_workday':
                    return modify_workday(request)
                elif action == 'del_workday':
                    return delete_workday(request)
                else:
                    return JsonResponse({'code': 1000, 'message': '不支持该类型http请求'})
            else:
                return JsonResponse({'code': 1000, 'message': '无权访问'})
        else:
            return JsonResponse({'code': 1000, 'message': '无权访问'})
    else:
        return JsonResponse({'code': 1000, 'message': '无权访问'})
