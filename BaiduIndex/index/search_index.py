#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 10:34
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : search_index.py
# @Software: PyCharm
# @Desc    : 搜索指数爬虫


from urllib.parse import urlencode
import datetime
import json

from index.utils import get_key, decrypt_func, http_get


class BaiduIndex:
    """
        百度搜索指数
        :keywords; list
        :start_date; string '2018-10-02'
        :end_date; string '2018-10-02'
        :area; int, search by cls.province_code/cls.city_code
    """
    _all_kind = ['all']

    def __init__(
            self,
            *,
            keyword: str,
            start_date: str,
            end_date: str,
            cookies: str,
            ip: str,
            area=0
    ):
        self.keyword = keyword
        self.area = area
        self.start_date = start_date
        self.end_date = end_date
        self.cookies = cookies
        self.ip = ip

    def get_index(self):
        """
        获取百度指数
        返回的数据格式为:
        {
            'keyword': '武林外传',
            'type': 'wise',
            'date': '2019-04-30',
            'index': '202'
        }
        """
        try:
            result = self._get_encrypt_datas(
                start_date=self.start_date,
                end_date=self.end_date,
                keyword=self.keyword
            )
            if result == (None, None):
                with open("fail.txt", "a", encoding="utf-8") as f:
                    f.write(self.keyword + '\n')
                print('没有该关键词' + ":" + str(self.keyword))
            else:
                encrypt_datas, uniqid = result
                key = get_key(uniqid, self.cookies, self.ip)
                for encrypt_data in encrypt_datas:
                    for kind in self._all_kind:
                        encrypt_data[kind]['data'] = decrypt_func(
                            key, encrypt_data[kind]['data'])
                    for formated_data in self._format_data(encrypt_data):
                        yield formated_data
        except Exception as e:
            print(e)

    def _get_encrypt_datas(self, start_date, end_date, keyword):
        """
        :start_date; str, 2018-10-01
        :end_date; str, 2018-10-01
        :keyword; list, ['1', '2', '3']
        """
        word_list = [[{'name': keyword, 'wordType': 1}]]
        request_args = {
            'word': json.dumps(word_list),
            'startDate': start_date,
            'endDate': end_date,
            'area': self.area,
        }
        url = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
        html = http_get(url, self.cookies, self.ip)
        datas = json.loads(html)

        if datas['data'] != '':
            uniqid = datas['data']['uniqid']
            encrypt_datas = []
            for single_data in datas['data']['userIndexes']:
                encrypt_datas.append(single_data)
            return (encrypt_datas, uniqid)
        else:
            return (None, None)

    def _format_data(self, data):
        """
            格式化堆在一起的数据
        """
        keyword = str(data['word'])
        start_date = datetime.datetime.strptime(data['all']['startDate'], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(data['all']['endDate'], '%Y-%m-%d')
        date_list = []
        while start_date <= end_date:
            date_list.append(start_date)
            start_date += datetime.timedelta(days=1)

        for kind in self._all_kind:
            index_datas = data[kind]['data']
            for i, cur_date in enumerate(date_list):
                try:
                    index_data = index_datas[i]
                except IndexError:
                    index_data = ''
                formated_data = {
                    'keyword': json.loads(keyword.replace('\'', '"'))[0]['name'],
                    'type': kind,
                    'date': cur_date.strftime('%Y-%m-%d'),
                    'index': index_data if index_data else '0'
                }
                yield formated_data
