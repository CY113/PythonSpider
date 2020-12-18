#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/18 17:11
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : start.py
# @Software: PyCharm
# @Desc    : 爬虫启动文件

from scrapy.cmdline import execute

execute("scrapy crawl polygon -s JOBDIR=crawls/amap".split())
