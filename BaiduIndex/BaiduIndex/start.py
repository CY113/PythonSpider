#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 14:23
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : start.py
# @Software: PyCharm
# @Desc    : 爬虫启动文件

from scrapy.cmdline import execute
# execute("scrapy crawl prov_index".split())  # 抓取省份指数
# execute("scrapy crawl city_index".split())  # 抓取城市指数
execute("scrapy crawl sex_age".split())  # 抓取人群属性指数