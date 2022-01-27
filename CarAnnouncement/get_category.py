#!/usr/bin/evn python
# -*- coding:UTF-8 -*-
# @Time    : 2022/1/27 16:36
# @Author  : tianhao
# @Email   : alex.tianhao@gmail.com
# @File    : get_category.py
# @Software: PyCharm
# @Desc    : 获取车辆类型
import pandas as pd


def get_car_category(file_name):
    data = pd.read_csv(file_name)
    model = data['model_cn'].tolist()
    return model


if __name__ == '__main__':
    get_car_category('model_list.csv')
