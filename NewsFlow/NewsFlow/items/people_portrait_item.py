#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 13:56
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : people_portrait_item.py
# @Software: PyCharm
# @Desc    :

import scrapy


class PeoplePortraitItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data = scrapy.Field()
    event_id = scrapy.Field()
    pytime = scrapy.Field()

    @staticmethod
    def get_coll(self):
        coll_name = "people_portrait"
        return coll_name
