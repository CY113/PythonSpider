#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 13:39
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : media_view_item.py
# @Software: PyCharm
# @Desc    :

import scrapy


class MediaViewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data = scrapy.Field()
    event_id = scrapy.Field()
    pytime = scrapy.Field()

    @staticmethod
    def get_coll():
        coll_name = "media_view"
        return coll_name
