# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 9:29
# @FileName: passenger.py
# @Author  : CNPolaris
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json
from transit.models import Users
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from rest_framework_jwt.serializers import jwt_decode_handler
from django.contrib.auth.models import User
from userprofile.models import Profile

_FIELDS = ['user_id', 'dist', 'birth', 'gender']


@csrf_exempt
def list_passenger(request):
    """
    对行程信息进行列表查询，支持多条件查询
    指定查找字段 uid，dist，birth，gender，page
    :param request:GET
    :return:json
    """
    uid = request.params.get('passenger_id', None)
    dist = request.params.get('dist', None)
    birth = request.params.get('birth', None)
    gender = request.params.get('gender', None)
    # 要获取的第几页
    pagenum = request.params.get('page', 1)
    # 每页要显示的多少条记录
    pagelimit = request.params.get('limit', 40)
    sort = request.params.get('sort', None)
    context = {'code': 1000}
    querySet = Users.objects.all()
    # 主键id在路由中则直接能够查询唯一结果
    if uid:
        querySet = querySet.filter(user_id=uid).values()
        if querySet is not None:
            paginator = Paginator(querySet.values(), pagelimit)
            page = paginator.page(pagenum)
            context['code'] = 2000
            context['data'] = list(page)
            # total指定一共有多少页数据
            context['total'] = paginator.count
        else:
            context['code'] = 1000
            context['message'] = "不存在id为{}的乘客".format(uid)
        return JsonResponse(context)
    elif dist:
        try:
            querySet = querySet.filter(dist=dist).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "不存在省份为{}的乘客".format(dist)
        except BaseException as e:
            context['code'] = 1000
            context['message'] = "通过省编号{}查询出现错误{}".format(dist, e)
        return JsonResponse(context)
    elif birth:
        try:
            querySet = querySet.filter(birth=birth).order_by('birth')
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "没有出生时间为{}的乘客".format(birth)
        except BaseException as e:
            context['code'] = 1000
            context['message'] = "通过出生时间查询存在错误{}".format(e)
        return JsonResponse(context)
    elif gender:
        try:
            querySet = querySet.filter(gender=gender).values()
            if querySet is not None:
                paginator = Paginator(querySet.values(), pagelimit)
                page = paginator.page(pagenum)
                context['code'] = 2000
                context['data'] = list(page)
                # total指定一共有多少页数据
                context['total'] = paginator.count
            else:
                context['code'] = 1000
                context['message'] = "没有性别为{}的乘客".format(gender)
        except BaseException as e:
            context['code'] = 1000
            context['message'] = "通过性别查询记录出现错误{}".format(e)
        return JsonResponse(context)
    else:
        paginator = Paginator(querySet.values(), pagelimit)
        page = paginator.page(pagenum)
        context['code'] = 2000
        context['data'] = list(page)
        # total指定一共有多少页数据
        context['total'] = paginator.count
    return JsonResponse(context)


def data_valid(user_id, dist, birth, gender):
    """
    用来代替不能使用表单类的情况下数据的验证器
    :return: Bool
    """
    if user_id is None:
        return False
    if birth is None or not isinstance(birth, int):
        return False
    if gender is None or not gender in [0, 1]:
        return False
    if dist is None or not isinstance(dist, int):
        return False
    return True


@csrf_exempt
def add_passenger(request):
    """
    增加数据
    :param request: POST/json
    :return: json
    """
    # TODO:还是希望通过表单类来实现数据添加
    context = {'code': 1000}
    user_id = request.params.get("passenger_id", None)
    dist = request.params.get('dist', None)
    birth = request.params.get('birth', None)
    gender = request.params.get('birth', None)

    if data_valid(user_id, dist, birth, gender) is True:
        new_user = Users(user_id=user_id,
                         dist=dist,
                         birth=birth,
                         gender=gender,
                         )
        try:
            new_user.save()
            context['code'] = 2000
        except BaseException as e:
            context['code'] = 1000
            context['message'] = 'user_id为{}的乘客已经存在,出现错误{}'.format(user_id, e)
            return JsonResponse(context)
    else:
        context['code'] = 1000
        context['message'] = "表单不全"
    return JsonResponse(context)


def modify_passenger(request):
    """
    修改记录
    :param request: PUT/json
    :return:json
    """
    context = {'ret': 1000}
    uid = request.params['passenger_id']
    try:
        user = Users.objects.get(user_id=uid)
        if user:
            # 提取数据
            gender = request.params.get('passenger_id', None)
            dist = request.params.get('dist', None)
            birth = request.params.get('birth', None)
            if gender is not None and gender in [0, 1]:
                user.gender = gender
            if dist is not None and isinstance(dist, int):
                user.dist = dist
            if birth is not None and isinstance(birth, int):
                user.birth = birth
            user.save()
            context['code'] = 2000
    except BaseException as e:
        context['code'] = 1000
        context['message'] = 'id为{}的记录不存在,出现错误{}'.format(uid, e)
        return JsonResponse(context)
    return JsonResponse(context)


def delete_passenger(request):
    """
    删除记录
    :param request: DELETE/json
    :return: json
    """
    context = {'code': 1000}
    uid = request.params['passenger_id']
    try:
        user = Users.objects.get(user_id=uid)
        user.delete()
        context['code'] = 2000
    except BaseException as e:
        context['code'] = 1000
        context['message'] = 'id为{}的记录不存在,出现错误{}'.format(uid, e)
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
            if profile.roles != 'admin' or not user.is_superuser:
                if action == 'list_passenger':
                    return list_passenger(request)
            elif profile.roles == 'admin' or user.is_superuser:
                if action == 'list_passenger':
                    return list_passenger(request)
                elif action == 'add_passenger':
                    return add_passenger(request)
                elif action == 'modify_passenger':
                    return modify_passenger(request)
                elif action == 'del_passenger':
                    return delete_passenger(request)
                else:
                    return JsonResponse({'code': 1000, 'message': '不支持该类型http请求'})
    else:
        return JsonResponse({'code': 1000, 'message': '无访问权限'})

