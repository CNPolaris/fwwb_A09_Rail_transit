from django.db.models import Count
from django.shortcuts import render
# 导入 HttpResponse 模块
from django.http import HttpResponse, JsonResponse
# 导入行程model
from .models import Trips, models, Users
# 导入表单类
from .forms import TripsForm
# 引入redirect重定向模块
from django.shortcuts import render, redirect
import json
import datetime
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# 首页展示图谱视图
# def index(request):
#     return render(request, 'index.html')


def index(request):
    # 初始化查询集
    Trips_list = Trips.objects.all()
    # trips_data_list = Trips_list.filter(In_time__year=2014)
    # date_list = Trips_list.dates('In_time', kind='month')
    # x = []
    # y = []
    # for date in date_list:
    #     temp = str(date).split('-')
    #     x.append(str(date))
    #     y.append(trips_data_list.filter(
    #         In_time__contains=datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))).count())
    context = {
        # 'trips': trips_data_list,
        # 'x': x,
        # 'y': y,
    }
    return render(request, 'index.html', context)
    # return HttpResponse(json.dumps(data), content_type='application/json')
    # return JsonResponse(data)


@csrf_exempt
def echarts_data_month(request):
    """
    后端向前端返回json数据
    以2020.01的数据作为测试数据使用，测试完成后根据实际日期从数据库抽取数据
    :param request:
    :return: json
    key: 某年月日内的所有入站时间
    value: 根据入站时间In_time进行分类统计后的每组对应的数量
    """
    Trips_list_2020 = Trips.objects.filter(In_time__contains=datetime.date(2020, 1, 1)).values_list('In_time').annotate(
        Count("id"))
    # date_list = Trips_list_2020.dates('In_time', kind='day')
    context = {
        "key": [i[0] for i in Trips_list_2020],
        "value": [i[1] for i in Trips_list_2020]
    }
    return JsonResponse(context)


@csrf_exempt
def echarts_data_user(request):
    """
    用户年龄结构分析
    :param request:Get
    :return: Json
    age: 用户年龄的分组
    count: 不同年龄段的用户数量
    """
    User_list = Users.objects.values_list('Birth').annotate(Count("id"))
    # 年龄阶段分组
    age_stage = [list(range(0, 7)), list(range(7, 18)), list(range(18, 41)), list(range(41, 66))]
    # 记录不同年龄段的个数
    count = [0, 0, 0, 0, 0]
    # 获取互联网时间的年份
    This_year = datetime.date.today().year
    for line in User_list:
        # 当前的日期减去用户的出生年
        age = This_year - line[0]
        if age in age_stage[0]:
            count[0] = count[0] + line[1]
        elif age in age_stage[1]:
            count[1] = count[1] + line[1]
        elif age in age_stage[2]:
            count[2] = count[2] + line[1]
        elif age in age_stage[3]:
            count[3] = count[3] + line[1]
        else:
            count[4] = count[4] + line[1]
    # 向前端返回的数据
    context = {
        "age": ["0-6", "7-17", "18-40", "41-65", "66+"],
        "count": count
    }
    return JsonResponse(context)
