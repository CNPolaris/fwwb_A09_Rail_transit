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

MODEL_PATH = os.path.join(BASE_DIR, 'static\model\\')


def weather_form():
    """
    量化天气
    :return:
    """
    return None


def get_weather_data(**kwargs):
    """
    获取天气数据
    ['max_temperature', 'min_temperature', 'wind_force','air_quality', 'year', 'month', 'day']
    :return:
    """
    weather_sheet = pd.DataFrame()
    weather_sheet['year'] = [kwargs['year']]
    weather_sheet['month'] = [kwargs['month']]
    weather_sheet['day'] = [kwargs['day']]

    weather_sheet['max_temperature'] = [15]
    weather_sheet['min_temperature'] = [14]
    weather_sheet['wind_force'] = [3]
    weather_sheet['air_quality'] = [60]
    return weather_sheet


def load_station():
    """
    获取站点 并转换成list
    :return: list
    """
    station_querySet = Station.objects.values('station_name')
    station_list = [sta['station_name'] for sta in station_querySet]
    return station_list


def merge_predict_data(**kwargs):
    """
    整合预测数据
    :return: pd
    """
    predict_sheet = pd.DataFrame()
    predict_sheet['Standard_time'] = [kwargs['standard_time']]
    predict_sheet['year'] = [kwargs['year']]
    predict_sheet['month'] = [kwargs['month']]
    predict_sheet['day'] = [kwargs['day']]
    # predict_sheet['weekday'] = [kwargs['weekday']]
    # 整合天气数据
    predict_sheet = pd.merge(predict_sheet, get_weather_data(**kwargs), on=['year', 'month', 'day'])
    return predict_sheet


def load_model(station, label):
    """
    引入model
    :param station: station_name
    :param label: in or out
    :return: lightgbm model
    """
    model_path = f'model_{station}_{label}.txt'
    gbm = lgb.Booster(model_file=MODEL_PATH + model_path)
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
    return y_pred


def main(request):
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
        year = request.params.get('year', None)
        month = request.params.get('month', None)
        day = request.params.get('day', None)
        hour = request.params.get('hour', None)
        minute = request.params.get('minute', None)
        standard_time = int(hour) * 6 + int(int(minute) / 10)
        weekday = request.params.get('weekday', None)

        predict_data = merge_predict_data(year=int(year), month=int(month), day=int(day), standard_time=standard_time,
                                          weekday=int(weekday))

        for sta in station:
            pred1 = predict(predict_data, sta, 'in')
            pred2 = predict(predict_data, sta, 'out')
            in_list.append(int(pred1[0]))
            out_list.append(int(pred2[0]))

        context['code'] = 2000
        context['label'] = station
        context['in_list'] = in_list
        context['out_list'] = out_list

    else:
        context['code'] = 1000
        context['message'] = '未登录用户无法获取信息'
    return JsonResponse(context)
