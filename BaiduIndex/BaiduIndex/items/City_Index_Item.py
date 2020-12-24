#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 15:27
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : City_Index_Item.py
# @Software: PyCharm
# @Desc    : 城市指数字段说明


import scrapy


class CityIndexItem(scrapy.Item):
    keyword = scrapy.Field()  # 关键词
    city = scrapy.Field()  # 城市ID
    city_index = scrapy.Field()  # 城市搜索指数
    prov = scrapy.Field()  # 所属省份ID
    date = scrapy.Field()  # 日期
    crawl_time = scrapy.Field()  # 抓取时间

    # 数据库插入语句
    def get_insert_sql(self):
        insert_sql = "insert into city_index(keyword,city,city_index,prov,date,crawl_time) values(%s,%s,%s,%s,%s,%s)"
        params = (self['keyword'], self['city'], self['city_index'], self['prov'], self['date'], self['crawl_time'])
        return insert_sql, params
