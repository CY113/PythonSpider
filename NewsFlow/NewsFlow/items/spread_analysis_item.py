#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 14:05
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : spread_analysis_item.py
# @Software: PyCharm
# @Desc    :
import scrapy


class SpreadAnalysisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data = scrapy.Field()
    event_id = scrapy.Field()
    pytime = scrapy.Field()

    @staticmethod
    def get_coll():
        coll_name = "spread_analysis"
        return coll_name
