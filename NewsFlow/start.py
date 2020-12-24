#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 16:15
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : start.py
# @Software: PyCharm
# @Desc    : 爬虫启动该文件


import os


def tick():
    print("正在爬取任务：event_list")
    os.system("scrapy crawl event_list")
    print("正在爬取任务：home_page")
    os.system("scrapy crawl home_page")
    print("正在爬取任务：event_overview")
    os.system("scrapy crawl event_overview")
    print("正在爬取任务：media_view")
    os.system("scrapy crawl media_view")
    print("正在爬取任务：media_view_2")
    os.system("scrapy crawl media_view_2")
    print("正在爬取任务：people_portrait")
    os.system("scrapy crawl people_portrait")
    print("正在爬取任务：spread_analysis")
    os.system("scrapy crawl spread_analysis")


if __name__ == '__main__':
    tick()
