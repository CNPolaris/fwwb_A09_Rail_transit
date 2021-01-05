from django.db.models import Count
from django.shortcuts import render
# 导入 HttpResponse 模块
from django.http import HttpResponse, JsonResponse
# 导入行程model
from .models import Trips, models
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
def echarts_data(request):
    """
    后端向前端返回json数据
    以2020.01的数据作为测试数据使用，测试完成后根据实际日期从数据库抽取数据
    :param request:
    :return: json
    """
    Trips_list_2020 = Trips.objects.filter(In_time__contains=datetime.date(2020, 1, 1)).values_list('In_time').annotate(Count("id"))
    # date_list = Trips_list_2020.dates('In_time', kind='day')
    context = {
        "key": [i[0] for i in Trips_list_2020],
        "value": [i[1] for i in Trips_list_2020]
    }
    return JsonResponse(context)