import django
from django.db.models import Count
from django.shortcuts import render
# 导入 HttpResponse 模块
from django.http import HttpResponse, JsonResponse
import time
# 导入行程model
from .models import Trips, models, Users, Workdays, Station, TripStatistics
# 导入表单类
from .forms import TripsForm
# 引入redirect重定向模块
from django.shortcuts import render, redirect
import datetime
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from django.db import close_old_connections


# Create your views here.
# 首页展示图谱视图
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def echarts_monthflow(request, date):
    """
    后端向前端返回json数据
    :param date: 前端使用api时需要带上date数据 如2020-01-01
    :param request:
    :return: json
    key: 某年月日内的所有入站时间
    value: 根据入站时间In_time进行分类统计后的每组对应的数量
    """
    print(date)
    Trips_list_2020 = Trips.objects.filter(in_station_time__contains=date).values_list(
        'in_station_time').annotate(
        Count("id"))
    # date_list = Trips_list_2020.dates('In_time', kind='day')
    context = {
        "key": [i[0] for i in Trips_list_2020],
        "value": [i[1] for i in Trips_list_2020]
    }
    return JsonResponse(context)


@csrf_exempt
def echarts_agestruct(request):
    """
    用户年龄结构分析
    :param request:Get
    :return: Json
    age: 用户年龄的分组
    count: 不同年龄段的用户数量
    """
    User_list = Users.objects.values_list('birth').annotate(Count("user_id"))
    # 年龄阶段分组
    age_stage = [list(range(0, 7)), list(range(7, 18)), list(range(18, 41)), list(range(41, 66))]
    # 记录不同年龄段的个数
    count = [0, 0, 0, 0, 0]
    # 获取互联网时间的年份
    This_year = datetime.date.today().year
    if User_list:
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


@csrf_exempt
def echarts_dailyflow(request, year):
    """
    每天实时客流量统计
    :param year: web发送请求时所附带的当前年份参数
    :param request: Get
    :return: json
    """
    # 从Tripstatistics中获取每一天的实时出行人数
    EachDay_list = TripStatistics.objects.filter(date__contains=year)
    if EachDay_list:
        each_day = []
        each_day_flow = []
        for line in EachDay_list:
            each_day.append(line.date)
            each_day_flow.append(line.count)
        # api响应的数据
        context = {
            "date": each_day,
            "date_flow": each_day_flow
        }
        return JsonResponse(context)
    else:
        return JsonResponse({})


@csrf_exempt
def load_dataoftrip(request):
    """
    向数据库中导入trip的数据
    :param request:
    :return:
    """
    # FIXME(CNPolaris): 导入trip时由于数据量较大会导致django长时间连接mysql而出现数据库连接丢失的情况
    from itertools import islice
    django.db.close_old_connections()
    # data = pd.read_csv("E:\学习资料\第十二届服创大赛A类数据（部分企业）\新建文件夹\客流预测分析大数据附件\\trips.csv", parse_dates=['进站时间', '出站时间'])
    data = open("E:\学习资料\第十二届服创大赛A类数据（部分企业）\新建文件夹\客流预测分析大数据附件\\trips.csv")
    Trips_list = []
    print("Trips写入开始")
    start = time.clock()
    # for index, row in data.iterrows():
    #     Trips_list.append(Trips(user_id_id=row['用户ID'], in_station=row['进站名称'], in_station_time=row['进站时间'],
    #                             out_station=row['出站名称'],
    #                             out_station_time=row['出站时间'], channel=row['渠道编号'], price=row['价格']))
    for row in islice(data, 2, None):
        str = row.split(",")
        str[6] = str[6].strip("\n")
        Trips_list.append(Trips(user_id_id=str[0], in_station=str[1],
                                in_station_time=datetime.datetime.strptime(str[2], '%Y-%m-%d %H:%M:%S'),
                                out_station=str[3],
                                out_station_time=datetime.datetime.strptime(str[4], '%Y-%m-%d %H:%M:%S'),
                                channel=str[5], price=str[6]))
    print("读取完成")
    data.close()
    Trips.objects.bulk_create(Trips_list)
    end = time.clock()
    print("Trips写入完成，用时 %s" % (end - start))
    return JsonResponse({})


@csrf_exempt
def load_dataofuser(request):
    """
    向数据库中写入用户信息Users
    :param request:
    :return:
    """
    # TODO(CNPolaris):为前端提供数据实时导入的api，以及相应的反馈
    import pandas as pd
    data = pd.read_csv("E:\学习资料\第十二届服创大赛A类数据（部分企业）\客流预测分析大数据附件\\NewUsers.csv")
    Users_list = []
    print("user写入开始")
    start = time.clock()
    for index, row in data.iterrows():
        Users_list.append(Users(user_id=row.User_id, dist=row.Dist, birth=row.Birth, gender=row.Gender))
    Users.objects.bulk_create(Users_list)
    end = time.clock()
    print("user写入完成，用时 %s" % (end - start))
    return JsonResponse({})


@csrf_exempt
def load_dataofworkday(request):
    """
    向数据库中写入节假日数据
    :param request:
    :return:
    """
    # TODO(CNPolaris):为前端提供数据实时导入的api，以及相应的反馈
    import pandas as pd
    data = pd.read_csv("E:\学习资料\第十二届服创大赛A类数据（部分企业）\客流预测分析大数据附件\\newWorkdays2020.csv")
    Workdays_list = []
    print("workdays写入开始")
    start = time.clock()
    for index, row in data.iterrows():
        close_old_connections()
        Workdays_list.append(Workdays(date=row.date, date_class=row['class']))
    Workdays.objects.bulk_create(Workdays_list)
    end = time.clock()
    print("workdays写入完成,用时 %s" % (end - start))
    return JsonResponse({})


@csrf_exempt
def load_dataofstation(request):
    """
    向数据库中写入station数据
    :param request:
    :return:
    """
    # TODO(CNPolaris):为前端提供数据实时导入的api，以及相应的反馈
    import pandas as pd
    data = pd.read_csv("E:\学习资料\第十二届服创大赛A类数据（部分企业）\新建文件夹\客流预测分析大数据附件\station.csv")
    Station_list = []
    print("Station写入开始")
    start = time.clock()
    for index, row in data.iterrows():
        Station_list.append(Station(station_id=row['编号'], station_name=row['站点名称'], station_route=row['线路'],
                                    admin_area=row['行政区域']))
    Station.objects.bulk_create(Station_list)
    end = time.clock()
    print("Station写入完成，用时%s" % (end - start))
    return JsonResponse({})
