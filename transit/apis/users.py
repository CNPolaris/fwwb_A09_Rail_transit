# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 9:29
# @FileName: users.py
# @Author  : CNPolaris
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json
from transit.models import Users
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage

_FIELDS = ['user_id', 'dist', 'birth', 'gender']


@csrf_exempt
def list_user(request):
    """
    对行程信息进行列表查询，支持多条件查询
    指定查找字段 uid，dist，birth，gender，page
    :param request:GET
    :return:json
    """
    uid = request.params.get('uid', None)
    dist = request.params.get('dist', None)
    birth = request.params.get('birth', None)
    gender = request.params.get('gender', None)
    # 要获取的第几页
    pagenum = request.params.get('page', 1)
    context = {'ret': 0}
    querySet = Users.objects.all()
    # 每页要显示的多少条记录
    pagelimit = 50
    # 主键id在路由中则直接能够查询唯一结果
    if uid:
        querySet = querySet.filter(user_id=uid).values()
        if querySet is not None:
            paginator = Paginator(querySet.values(), pagelimit)
            page = paginator.page(pagenum)
            context['retlist'] = list(page)
            # total指定一共有多少页数据
            context['total'] = paginator.count
        else:
            context['ret'] = 1
            context['msg'] = "不存在id为{}的乘客".format(uid)
        return JsonResponse(context)
    elif dist:
        try:
            querySet = querySet.filter(dist=dist).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['retlist'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['ret'] = 1
                context['msg'] = "不存在省份为{}的乘客".format(dist)
        except BaseException as e:
            print(e)
            context['ret'] = 1
            context['msg'] = "通过省编号{}查询出现错误".format(dist)
        return JsonResponse(context)
    elif birth:
        try:
            querySet = querySet.filter(birth=birth).order_by('birth')
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['retlist'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['ret'] = 1
                context['msg'] = "没有出生时间为{}的乘客".format(birth)
        except BaseException:
            context['msg'] = "通过出生时间查询存在错误"
        return JsonResponse(context)
    elif gender:
        try:
            querySet = querySet.filter(gender=gender).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['retlist'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['ret'] = 1
                context['msg'] = "没有性别为{}的乘客".format(gender)
        except BaseException:
            context['ret'] = 1
            context['msg'] = "通过性别查询记录出现错误"
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
    if 'user_id' not in data or data['user_id'] is None:
        return False
    if 'birth' not in data or not isinstance(data['birth'], int):
        return False
    if 'gender' not in data or not data['gender'] in [0, 1]:
        return False
    if 'dist' not in data or not isinstance(data['dist'], int):
        return False
    return True


@csrf_exempt
def add_user(request):
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
            new_user = Users(user_id=data['user_id'],
                             dist=data['dist'],
                             birth=data['birth'],
                             gender=data['gender'],
                             )
            try:
                new_user.save()
            except BaseException:
                context['ret'] = 1
                context['msg'] = 'user_id为{}的乘客已经存在'.format(data['uid'])
                return JsonResponse(context)
            context['id'] = new_user.user_id
        else:
            context['ret'] = 1
            context['msg'] = "表单不全"
    else:
        context['ret'] = 1
        context['msg'] = "表单不能为空"
    return JsonResponse(context)


def modify_user(request):
    """
    修改记录
    :param request: PUT/json
    :return:json
    """
    context = {'ret': 0}
    uid = request.params['uid']
    newdata = request.params['newdata']

    try:
        user = Users.objects.get(user_id=uid)
    except BaseException:
        context['ret'] = 1
        context['msg'] = 'id为{}的记录不存在'.format(uid)
        return JsonResponse(context)
    if 'gender' in newdata and newdata['gender'] in [0, 1]:
        user.gender = newdata['gender']
    if 'dist' in newdata and isinstance(newdata['dist'], int):
        user.dist = newdata['dist']
    if 'birth' in newdata and isinstance(newdata['birth'], int):
        user.birth = newdata['birth']
    user.save()
    context['ret'] = 0
    return JsonResponse(context)


def delete_user(request):
    """
    删除记录
    :param request: DELETE/json
    :return: json
    """
    context = {'ret': 0}
    uid = request.params['uid']
    try:
        user = Users.objects.get(user_id=uid)
    except BaseException:
        context['ret'] = 1
        context['msg'] = 'id为{}的记录不存在'.format(uid)
        return JsonResponse(context)
    user.delete()
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
    if action == 'list_user':
        return list_user(request)
    elif action == 'add_user':
        return add_user(request)
    elif action == 'modify_user':
        return modify_user(request)
    elif action == 'del_user':
        return delete_user(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})
