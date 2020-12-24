#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 13:57
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : tools.py
# @Software: PyCharm
# @Desc    : 时间处理

import calendar
import datetime

from BaiduIndex.tools.DBHelper import DBHelper


def get_time_range_list(start_date, end_date):
    """
    根据开始时间和结束时间按月份获取每月第一天和最后一天
    :param start_date: 起始时间 --> str
    :param end_date: 结束时间 --> str
    :return: date_range_list -->list
    """
    date_range_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while 1:
        next_month = start_date + datetime.timedelta(days=calendar.monthrange(start_date.year, start_date.month)[1])
        month_end = next_month - datetime.timedelta(days=1)
        if month_end < end_date:
            date_range_list.append((datetime.datetime.strftime(start_date,
                                                               '%Y-%m-%d'),
                                    datetime.datetime.strftime(month_end,
                                                               '%Y-%m-%d')))
            start_date = next_month
        else:
            return date_range_list


class QueryData(object):
    def __init__(self):
        self.db_helper = DBHelper()

    def get_region_id(self):
        # 查询省份ID
        query_sql = "SELECT id FROM province_id ORDER BY id"
        return self.db_helper.query_task(query_sql)

    def get_keyword(self, table_name):
        keywords_list = []
        sql = 'SELECT distinct(keyword) FROM {}'.format(table_name)
        keywords = self.db_helper.query_task(sql)
        for keyword in keywords:
            keywords_list.append(str.lower(str(keyword[0])).strip())
        return keywords_list[2400:]


if __name__ == '__main__':
    startDate = "2020-03-01"
    endDate = "2020-09-01"
    print(get_time_range_list(startDate, endDate))