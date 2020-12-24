#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 11:36
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : event_overview_item.py
# @Software: PyCharm
# @Desc    : 事件概述字段Item


import scrapy


class EventOverviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data = scrapy.Field()
    event_id = scrapy.Field()
    img = scrapy.Field()
    delYn = scrapy.Field()
    factor = scrapy.Field()
    pytime = scrapy.Field()

    @staticmethod
    def get_coll():
        coll_name = "event_overview"
        return coll_name
