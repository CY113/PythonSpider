#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 12:28
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : start.py
# @Software: PyCharm
# @Desc    : 搜索指数爬虫启动文件
import random
import time

from index.DBHelper import DBHelper
from index.config import COOKIES, IP_Pool
from index.search_index import BaiduIndex
from index.utils import get_key_from_excel


def main(keyword_list, start_date, end_date):
    db = DBHelper()
    insert_sql = "INSERT INTO baidu_index(keyword,_index, date, crawl_time) VALUES (%s, %s, %s, %s)"
    cookie = random.choice(COOKIES)
    ip = random.choice(IP_Pool)
    for keyword in keyword_list:
        index = BaiduIndex(keyword=keyword, start_date=start_date, end_date=end_date, cookies=cookie, ip=ip)
        data = index.get_index()
        for index in data:
            keyword = index["keyword"]
            _index = index["index"]
            date = index["date"]
            crawl_time = time.strftime("%Y-%m-%d", time.localtime())  # 抓取时间
            db.insert_task(insert_sql, (keyword, _index, date, crawl_time))
        time.sleep(1)


if __name__ == '__main__':
    # 文件位置
    # file_path = r"需要跑的关键词-3.xlsx"
    # column_name = "关键词"  # 关键词列名
    # keywords = get_key_from_excel(file_path, column_name)
    # keywords_list = pd.read_csv(path, sep="\n", index_col=None, header=None,encoding="utf-8-sig")[0].tolist()
    keywords = ['斯柯达']
    main(keywords, start_date="2020-03-01", end_date="2020-04-01")
