#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 11:09
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : trans_time.py
# @Software: PyCharm
# @Desc    : 将时间戳转为格式化时间
import time


def transTime(x):
    time_array = time.localtime(x / 1000)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)
