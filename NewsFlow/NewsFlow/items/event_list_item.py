#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 10:38
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : event_list_item.py
# @Software: PyCharm
# @Desc    : 事件列表字段Item


import scrapy


class EventListItem(scrapy.Item):
    event_id = scrapy.Field()  # 事件ID
    day = scrapy.Field()  # 日期
    img = scrapy.Field()  # 图片
    fristType = scrapy.Field()  # 一级分类
    infExponent = scrapy.Field()  # 总影响力
    bdInfulence = scrapy.Field()  # 百度影响力
    wbInfulence = scrapy.Field()  # 微博影响力
    wxInfulence = scrapy.Field()  # 微信影响力
    name = scrapy.Field()  # 标题
    startTime = scrapy.Field()  # 开始时间
    pytime = scrapy.Field()  # 抓取时间
    tags = scrapy.Field()  # 标签
    isEnd = scrapy.Field()  # 标签

    @staticmethod
    def get_coll():
        coll_name = "events_list"
        return coll_name
