# -*- coding: utf-8 -*-
# @Time    : 2021/3/30 22:35
# @FileName: predict.py
# @Author  : CNPolaris
from transit.models import Trips, Users, Station, TripStatistics
import pandas as pd
from units.verify import verify_permissions
from django.http import JsonResponse
import lightgbm as lgb
import os
from fwwb_A09_Rail_transit.settings import BASE_DIR

MODEL_PATH = os.path.join(BASE_DIR, 'static', 'model')
STANDARD_TIME = ['0:10', '0:20', '0:30', '0:40', '0:50', '0:60', '1:10', '1:20', '1:30', '1:40', '1:50', '1:60', '2:10',
                 '2:20', '2:30', '2:40', '2:50', '2:60', '3:10', '3:20', '3:30', '3:40', '3:50', '3:60', '4:10', '4:20',
                 '4:30', '4:40', '4:50', '4:60', '5:10', '5:20', '5:30', '5:40', '5:50', '5:60', '6:10', '6:20', '6:30',
                 '6:40', '6:50', '6:60', '7:10', '7:20', '7:30', '7:40', '7:50', '7:60', '8:10', '8:20', '8:30', '8:40',
                 '8:50', '8:60', '9:10', '9:20', '9:30', '9:40', '9:50', '9:60', '10:10', '10:20', '10:30', '10:40',
                 '10:50', '10:60', '11:10', '11:20', '11:30', '11:40', '11:50', '11:60', '12:10', '12:20', '12:30',
                 '12:40', '12:50', '12:60', '13:10', '13:20', '13:30', '13:40', '13:50', '13:60', '14:10', '14:20',
                 '14:30', '14:40', '14:50', '14:60', '15:10', '15:20', '15:30', '15:40', '15:50', '15:60', '16:10',
                 '16:20', '16:30', '16:40', '16:50', '16:60', '17:10', '17:20', '17:30', '17:40', '17:50', '17:60',
                 '18:10', '18:20', '18:30', '18:40', '18:50', '18:60', '19:10', '19:20', '19:30', '19:40', '19:50',
                 '19:60', '20:10', '20:20', '20:30', '20:40', '20:50', '20:60', '21:10', '21:20', '21:30', '21:40',
                 '21:50', '21:60', '22:10', '22:20', '22:30', '22:40', '22:50', '22:60', '23:10', '23:20', '23:30',
                 '23:40', '23:50', '23:60']


def weather_form():
    """
    量化天气
    :return:
    """
    return None


def load_station():
    """
    获取站点 并转换成list
    :return: list
    """
    station_querySet = Station.objects.values('station_name')
    station_list = [sta['station_name'] for sta in station_querySet]
    return sorted(station_list)


def merge_predict_data(**kwargs):
    """
    整合预测数据
    :return: pd
    """
    predict_sheet = pd.DataFrame()
    predict_sheet['Standard_time'] = [kwargs['standard_time']]
    # predict_sheet['year'] = [kwargs['year']]
    predict_sheet['month'] = [kwargs['month']]
    predict_sheet['day'] = [kwargs['day']]
    predict_sheet['weekday'] = [kwargs['weekday']]
    # 整合天气数据

    predict_sheet['max_temperature'] = [15]
    predict_sheet['min_temperature'] = [14]
    predict_sheet['wind_force'] = [3]
    predict_sheet['air_quality'] = [60]

    return predict_sheet


def load_model(station, label):
    """
    引入model
    :param station: station_name
    :param label: in or out
    :return: lightgbm model
    """
    model_path = f'model_{station}_{label}.txt'
    gbm = lgb.Booster(model_file=os.path.join(MODEL_PATH, model_path))
    return gbm


def predict(df, station, label):
    """
    进行预测
    :param label: in or out
    :param station: station_name
    :param df: pd
    :return: int and label
    """
    # 导入模型
    gbm = load_model(station, label)
    y_pred = gbm.predict(df)
    return int(y_pred[0])


def normal_predict(request):
    """
    预测主方法
    :param request: GET
    :return: json
    """

    flag, request = verify_permissions(request)
    context = {}
    if flag:
        station = load_station()
        in_list = []
        out_list = []
        # year = request.params.get('year', None)
        month = request.params.get('month', None)
        day = request.params.get('day', None)
        hour = request.params.get('hour', None)
        minute = request.params.get('minute', None)
        standard_time = int(hour) * 6 + int(int(minute) / 10)
        weekday = request.params.get('weekday', None)

        predict_data = merge_predict_data(month=int(month), day=int(day), standard_time=standard_time,
                                          weekday=int(weekday))

        for sta in station:
            in_list.append(predict(predict_data, sta, 'in'))
            out_list.append(predict(predict_data, sta, 'out'))

        context['code'] = 2000
        context['label'] = station
        context['in_list'] = in_list
        context['out_list'] = out_list

    else:
        context['code'] = 1000
        context['message'] = '未登录用户无法获取信息'
    return JsonResponse(context)
