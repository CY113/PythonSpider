#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 13:35
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : home_page_item.py
# @Software: PyCharm
# @Desc    : 首页字段Item
import scrapy


class HomePageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data = scrapy.Field()
    pytime = scrapy.Field()
    date = scrapy.Field()

    @staticmethod
    def get_coll(self):
        coll_name = "home_page"
        return coll_name
