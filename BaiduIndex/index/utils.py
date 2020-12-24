#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 10:34
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : utils.py
# @Software: PyCharm
# @Desc    : 函数封装


import datetime
import json

import pandas as pd
import requests

headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}


def get_time_range_list(start_date, end_date):
    """
        切分时间段
    """
    date_range_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while 1:
        temp_date = start_date + datetime.timedelta(days=300)
        if temp_date > end_date:
            date_range_list.append((start_date, end_date))
            break
        date_range_list.append((start_date, temp_date))
        start_date = temp_date + datetime.timedelta(days=1)
    return date_range_list


def http_get(url, cookies, ip):
    """
        发送get请求, 程序中所有的get都是调这个方法
        如果想使用多cookies抓取, 和请求重试功能
        在这自己添加
    """
    _headers = headers.copy()
    _headers['Cookie'] = cookies
    response = requests.get(url, headers=_headers, timeout=5, proxies={"https": ip})
    if response.status_code != 200:
        raise requests.Timeout
    return response.text


def get_key(uniq_id, cookies, ip):
    """
    """
    url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniq_id
    html = http_get(url, cookies, ip)
    data = json.loads(html)
    key = data['data']
    return key


def decrypt_func(key, data):
    """
        数据解密方法
    """
    a = key
    i = data
    n = {}
    s = []
    for o in range(len(a) // 2):
        n[a[o]] = a[len(a) // 2 + o]
    for r in range(len(data)):
        s.append(n[i[r]])
    return ''.join(s).split(',')


def get_key_from_excel(path, column):
    """
    从excel或csv中读取关键词列表,百度指数关键词默认小写
    :param path:  文件路径 -->str
    :param column: 关键词列列名 -->str
    :return: 关键词列表 --》list
    """
    keyword_list = []
    data = pd.read_excel(path)
    keywords = data[column].to_list()
    for keyword in keywords:
        keyword_list.append(keyword)
    return keyword_list
