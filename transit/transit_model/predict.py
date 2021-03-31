# -*- coding: utf-8 -*-
# @Time    : 2021/3/30 22:35
# @FileName: predict.py
# @Author  : CNPolaris
from transit.models import Trips, Users, Station, TripStatistics
import pandas as pd
from units.verify import verify_permissions
from django.http import JsonResponse
import lightgbm as lgb


def weather_form():
    """
    量化天气
    :return:
    """
    return None


def get_weather_data(data):
    """
    获取天气数据
    ['max_temperature', 'min_temperature', 'wind_force','air_quality', 'year', 'month', 'day']
    :return:
    """
    weather_sheet = pd.DataFrame()
    weather_sheet['year'] = pd.to_datetime(data['date'], format='%Y-%m-%d %H:%M:%S').dt.year
    weather_sheet['month'] = pd.to_datetime(data['date'], format='%Y-%m-%d %H:%M:%S').dt.month
    weather_sheet['day'] = pd.to_datetime(data['date'], format='%Y-%m-%d %H:%M:%S').dt.day

    weather_sheet['max_temperature'] = None
    weather_sheet['min_temperature'] = None
    weather_sheet['wind_force'] = None
    weather_sheet['air_quality'] = None
    return weather_sheet


def load_station():
    """
    获取站点 并转换成list
    :return: list
    """
    station_querySet = Station.objects.values('station_name')
    return sorted(list(station_querySet))


def date_form(time):
    """
    标准化时间
    :return:
    """
    hour = pd.to_datetime(time['date'], format='%Y-%m-%d %H:%M:%S').dt.hour
    minute = pd.to_datetime(time['date'], format='%Y-%m-%d %H:%M:%S').dt.minute

    return hour * 6 + int(minute / 10)


def merge_predict_data(data):
    """
    整合预测数据
    :return: pd
    """
    predict_sheet = pd.DataFrame()
    # 规范时间
    time = date_form(data)
    predict_sheet['year'] = pd.to_datetime(data['date'], format='%Y-%m-%d %H:%M:%S').dt.year
    predict_sheet['month'] = pd.to_datetime(data['date'], format='%Y-%m-%d %H:%M:%S').dt.month
    predict_sheet['day'] = pd.to_datetime(data['date'], format='%Y-%m-%d %H:%M:%S').dt.day
    predict_sheet['weekday'] = pd.to_datetime(data['date'], format='%Y-%m-%d %H:%M:%S').dt.weekday
    predict_sheet['Standard_time'] = time

    # 整合天气数据
    predict_sheet = pd.merge(predict_sheet, get_weather_data(data), on=['year', 'month', 'day'])

    return predict_sheet


def load_model(station, label):
    """
    引入model
    :param station: station_name
    :param label: in or out
    :return: lightgbm model
    """
    gbm = lgb.Booster(f'model/model_{station}_{label}.txt')
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
    :param request: POST
    :return: json
    """

    request, flag = verify_permissions(request)
    context = {}
    if flag:
        station = load_station()
        pred_dict = {}
        predict_data = merge_predict_data(request.params)
        for sta in station:
            pred1 = predict(predict_data, sta, 'in')
            pred2 = predict(predict_data, sta, 'out')
            pred_dict[sta] = {'station': sta, 'in': pred1, 'out': pred2}
        context['code'] = 2000
        context['data'] = pred_dict

    else:
        context['code'] = 1000
        context['message'] = '未登录用户无法获取信息'
    return JsonResponse(context)
