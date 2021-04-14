# -*- coding: utf-8 -*-
# @Time    : 2021/3/24 17:03
# @FileName: train_model.py
# @Author  : CNPolaris
# -*- coding: utf-8 -*-
# @Time    : 2021/3/23 17:53
# @FileName: TransitModel.py
# @Author  : CNPolaris

import pandas as pd
import copy
import logging
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import mean_absolute_error
import warnings
import lightgbm as lgb
import os
from itertools import combinations
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from copy import deepcopy
import warnings
import copy
import numpy as np
import pickle

features = ['user_id', 'in_station', 'out_station', 'channel', 'price', 'year',
            'month', 'day', 'weekday', 'in_station_hour', 'in_station_minutes',
            'out_station_hour', 'out_station_minutes']


def load_file():
    """
    导入数据
    :return: data
    """
    data = pd.read_csv('data/train/train3.csv')
    # data = data.loc[(data['day'] >= daystart) & (data['day'] <= dayend)].reset_index(drop=True)
    print("载入数据完成")
    print('*' * 100)
    return data[features]


def time_clip(df):
    # 对时间进行偏移，clip=1,即表示原来0-10分钟转换为1-11分钟
    clip = [0]
    for _clip in clip:
        df['time_clip_in'] = df['in_station_minutes'].apply(lambda x: int((x + _clip) / 10))
        df['time_clip_out'] = df['out_station_minutes'].apply(lambda x: int((x + _clip) / 10))
    print("划分时间完成")
    print('*' * 100)
    return df


def load_station():
    station = pd.read_csv('data/original/station2.csv')
    return station['station_name']


def load_weather():
    weather = pd.read_csv('data/weather/clean_weather.csv', header=0,
                          names=['date', 'max_temperature', 'min_temperature', 'weather', 'wind_force',
                                 'air_quality', 'year', 'month', 'day'])
    weather = weather[['max_temperature', 'min_temperature', 'wind_force',
                       'air_quality', 'year', 'month', 'day']]
    return weather


def perSt_perDay_perTen_count(df):
    # 统计每个站台每天每10分钟的进出流量情况
    clip = [0]
    Day_sheet = pd.DataFrame()
    Day_sheet['Standard_time'] = [t for t in range(24 * 6)]
    station = pd.read_csv('data/original/station2.csv')
    for _clip in clip:
        df['map_time_in'] = df.in_station_hour * 6 + df['time_clip_in_' + str(_clip)]
        df['map_time_out'] = df.out_station_hour * 6 + df['time_clip_out_' + str(_clip)]
        Df = copy.deepcopy(df)
        for St in station.station_name.unique():
            Day_sheet['Station_in_' + str(St)] = St
            df1 = Df[Df.in_station == St]
            temp = df1.groupby(['map_time_in', 'in_station'], as_index=False)['user_id'].count()
            dict_in = dict(zip(temp['map_time_in'].values, temp['user_id'].values))
            Day_sheet['In_' + str(St) + '_' + str(_clip)] = Day_sheet['Standard_time'].apply(
                lambda x: dict_in[x] if x in dict_in.keys() else 0)
            # for St in df.out_station.unique():
            Day_sheet['Station_out_' + str(St)] = St
            df2 = Df[Df['out_station'] == St]
            temp = df2.groupby(['map_time_out', 'out_station'], as_index=False)['user_id'].count()
            dict_out = dict(zip(temp['map_time_out'].values, temp['user_id'].values))
            Day_sheet['out_' + str(St) + '_' + str(_clip)] = Day_sheet['Standard_time'].apply(
                lambda x: dict_out[x] if x in dict_out.keys() else 0)

    print("统计每十分钟数据完成")
    print('*' * 100)
    return Day_sheet


def day_res_extract(df):
    # 提取每天每个站台每分钟的流量结果
    res = pd.DataFrame()
    date = df.value_counts(['year', 'month', 'day']).keys()
    for d in date:
        res_ = perSt_perDay_perTen_count(df[(df.year == d[0]) & (df.month == d[1]) & (df.day == d[2])])
        res_['year'] = d[0]
        res_['month'] = d[1]
        res_['day'] = d[2]
        res = pd.concat([res, res_], axis=0)
    # res.to_csv('day_res_extract.csv', index=False)
    return res


def completion(df):
    in_station = df.in_station.unique()
    out_station = df.out_station.unique()
    for sta_in in in_station:
        if df['In_' + str(sta_in) + '_0'].isnull().sum() > 0:
            df['In_' + str(sta_in) + '_0'].fillna(df['In_' + str(sta_in) + '_0'].mean(), inplace=True)

    for sta_out in out_station:
        if df['Station_out_' + str(sta_out) + '_0'].isnull().sum() > 0:
            df['Station_out_' + str(sta_out) + '_0'].fillna(sta_out, inplace=True)
        if df['out_' + str(sta_out) + '_0'].isnull().sum() > 0:
            df['out_' + str(sta_out) + '_0'].fillna(df['In_' + str(sta_out) + '_0'].mean(), inplace=True)
    return df


def merge_weather(df):
    weather = load_weather()
    mer = pd.merge(df, weather, on=['year', 'month', 'day'])
    return mer


def train(df, station, label):
    train_data_ = copy.deepcopy(df)
    train_ = copy.deepcopy(train_data_)

    pred = [i for i in train_.columns if i not in ['in', 'out']]

    target = train_[label]
    train_selected = train_[pred]
    test = train_[pred]

    predictions = np.zeros(len(test))
    oof_lgb = np.zeros(len(train_))

    params = {
        'learning_rate': 0.02,
        'boosting': 'gbdt',
        'objective': 'regression',
        'metric': 'rmse',
        'num_leaves': 30,
        'feature_fraction': 0.85,
        'bagging_fraction': 0.85,
        'bagging_freq': 5,
        'seed': 1,
        'bagging_seed': 1,
        'feature_fraction_seed': 11,
        'min_data_in_leaf': 20,
        'max_depth': 7,
        'nthread': -1,
        'verbose': -1,
        # 'lambda_l2':0.7
    }

    n_splits = 5
    folds = KFold(n_splits=n_splits, shuffle=True, random_state=15)

    for n_fold, (train_idx, valid_idx) in enumerate(folds.split(train_selected, target)):
        print('the %s training start ...' % n_fold)

        trn_data = lgb.Dataset(train_selected.iloc[train_idx], label=target.iloc[train_idx])
        val_data = lgb.Dataset(train_selected.iloc[valid_idx], label=target.iloc[valid_idx])
        clf = lgb.train(
            params=params,
            train_set=trn_data,
            num_boost_round=20000,
            valid_sets=[trn_data, val_data],
            early_stopping_rounds=100,
            verbose_eval=200
        )

        clf.save_model(f'model/model_{station}_{label}.txt')

        oof_lgb[valid_idx] = clf.predict(train_selected.iloc[valid_idx], num_iteration=clf.best_iteration)
        predictions += clf.predict(test, num_iteration=clf.best_iteration) / folds.n_splits
        print('*' * 100)
    return predictions


def gen_train_data():
    data = load_file()
    data = time_clip(data)
    data = day_res_extract(df=data)
    data = completion(data)
    data = merge_weather(data)
    print('整合训练集完成')
    print('*' * 100)
    return data


def echo_station_train():
    # train_data = gen_train_data()
    train_data = pd.read_csv('testMerge.csv')
    station = load_station()
    label = ['in', 'out']
    for l in label:
        for sta in station:
            DataSheet = pd.DataFrame()
            DataSheet['Standard_time'] = train_data['Standard_time']
            DataSheet['year'] = train_data['year']
            DataSheet['month'] = train_data['month']
            DataSheet['day'] = train_data['day']
            DataSheet['max_temperature'] = train_data['max_temperature']
            DataSheet['min_temperature'] = train_data['min_temperature']
            DataSheet['wind_force'] = train_data['wind_force']
            DataSheet['air_quality'] = train_data['air_quality']
            DataSheet['in'] = train_data['In_' + str(sta) + '_0']
            DataSheet['out'] = train_data['out_' + str(sta) + '_0']
            train(DataSheet, sta, l)
            print('站点{}-{}模型完成'.format(sta, l))
            print('*' * 100)


if __name__ == "__main__":
    echo_station_train()

