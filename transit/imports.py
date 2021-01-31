# -*- coding: utf-8 -*-
# @Time    : 2021/1/10 10:28
# @FileName: imports.py
# @Author  : CNPolaris
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from .models import Trips, Users, Workdays, Station, TripStatistics
from django.views.decorators.csrf import csrf_exempt
import time
import django

@csrf_exempt
def load_dataoftrip(request):
    """
    向数据库中导入trip的数据
    :param request:
    :return:
    """
    # FIXME(CNPolaris): 导入trip时由于数据量较大会导致django长时间连接mysql而出现数据库连接丢失的情况
    from itertools import islice
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
