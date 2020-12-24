#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 15:27
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : Prov_Index_Item.py
# @Software: PyCharm
# @Desc    : 省份指数字段说明


import scrapy


class ProvIndexItem(scrapy.Item):
    keyword = scrapy.Field()  # 关键词
    prov = scrapy.Field()  # 省份ID
    prov_index = scrapy.Field()  # 省份搜索指数
    date = scrapy.Field()  # 日期
    crawl_time = scrapy.Field()  # 抓取时间

    # 数据库插入语句
    def get_insert_sql(self):
        insert_sql = "insert into province_index(keyword,prov,prov_index,date,crawl_time) values(%s,%s,%s,%s,%s)"
        params = (self['keyword'], self['prov'], self['prov_index'], self['date'], self['crawl_time'])
        return insert_sql, params
