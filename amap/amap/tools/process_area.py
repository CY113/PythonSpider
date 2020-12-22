#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/18 16:01
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : process_area.py
# @Software: PyCharm
# @Desc    : 辅助方法
import pandas as pd


def getCeil(lat_min, lat_max, lng_min, lng_max):
    """
    将给定区域分成经纬度边长为0.03的正方形碎片
    :param lat_min: 最小纬度
    :param lat_max: 最大纬度
    :param lng_min: 最小经度
    :param lng_max: 最大经度
    :return: List of str
    """
    lat_min = float(lat_min)
    lat_max = float(lat_max)
    lng_min = float(lng_min)
    lng_max = float(lng_max)
    ceil_list = []
    temp_lng = lng_min
    while temp_lng < lng_max:
        temp_lat = lat_min
        while temp_lat < lat_max:
            ceil_list.append(str(round(temp_lng, 6)) + ',' + str(round(temp_lat + 0.3, 6)) + "|" + str(
                round(temp_lng + 0.3, 6)) + ',' + str(round(temp_lat, 6)))
            temp_lat += 0.3
        temp_lng += 0.3
    return ceil_list


def get_area_list():
    """
    获取城市列表，最大最小经纬度
    :return:
    """
    try:
        # data = pd.read_excel("./城市列表.xlsx")
        data = pd.read_excel("amap/tools/城市列表.xlsx")
        data['lng_min'], data['lat_max'] = list(zip(*data["top_left"].str.split(",")))
        data['lng_max'], data['lat_min'] = list(zip(*data["bottom_right"].str.split(",")))
        return data[["city", "lng_min", "lat_max", "lng_max", "lat_min"]].to_dict(orient='records')
    except Exception as e:
        raise ValueError('检查Excel文件，错误为'.format(e))


if __name__ == '__main__':
    data = get_area_list()[0]
    name, lat_min, lat_max, lng_min, lng_max = data['city'],data['lat_min'],data['lat_max'],data['lng_min'],data['lng_max']
    print(len(getCeil(lat_min, lat_max, lng_min, lng_max)))
    print(getCeil(lat_min, lat_max, lng_min, lng_max))
