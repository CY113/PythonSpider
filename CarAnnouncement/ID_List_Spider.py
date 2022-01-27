#!/usr/bin/evn python
# -*- coding:UTF-8 -*-
# @Time    : 2022/1/27 15:42
# @Author  : tianhao
# @Email   : alex.tianhao@gmail.com
# @File    : ID_List_Spider.py
# @Software: PyCharm
# @Desc    : 根据车辆类型获取车辆公告ID
import random
import re

import requests
import time

from lxml import etree
from tqdm import tqdm

from get_category import get_car_category
from tools import strong_common_retry, get_proxy


@strong_common_retry(max_retry=4, exception=(requests.ReadTimeout,))
def get_car_id(category, proxy):
    timestamp = int(time.time())
    target_url = 'http://www.chinacar.com.cn/Home/GonggaoSearch/GonggaoSearch/search_json?_dc={}'.format(
        timestamp * 100)
    headers = {
        "Accept": "application/x-json;text/x-json;charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7",
        "Content-Length": "256",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "PHPSESSID=1bg1iot1ka4iq3hii7ib3m0ll6; Hm_lvt_6c1a81e7deb77ce536977738372f872a=1640841247,{}; rel_search=1; clcp_list=896485%7C943511%7C1023506%7C1060637%7C; Hm_lpvt_6c1a81e7deb77ce536977738372f872a={}".format(
            timestamp, timestamp),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "http://www.chinacar.com.cn/ggcx_new/list.html",
        "Proxy-Connection": "keep-alive",
        "Origin": "http://www.chinacar.com.cn",
        "Host": "www.chinacar.com.cn",
    }
    params = {
        "s0": "",
        "s1": "",
        "s2": "{}".format(category),
        "s3": "",
        "s4": "",
        "s5": "",
        "s6": "",
        "s7": "",
        "s8": "",
        "s9": "",
        "s10": "",
        "s11": "",
        "s12": "",
        "s13": "",
        "s14": "",
        "s15": "",
        "s16": "",
        "s17": "",
        "s18": "",
        "s19": "",
        "s20": "0",
        "s28": "0",
        "s29": "0",
        "s30": "1",
        "s_1": "",
        "ss_1": "1",
        "s_2": "",
        "ss_2": "1",
        "s_3": "",
        "ss_3": "1",
        "s_4": "",
        "ss_4": "1",
        "s_5": "",
        "ss_5": "1",
        "s_6": "",
        "ss_6": "1",
        "s_7": "",
        "ss_7": "1",
        "s_8": "",
        "ss_8": "1",
        "s_9": "",
        "ss_9": "1",
        "page": "1",
        "start": "0",
        "limit": "400",
    }

    # 代理IP
    proxies = {
        "http": "http://{}".format(proxy)
    }
    response = requests.post(target_url, headers=headers, data=params, proxies=proxies)
    if response.status_code == 200:
        msg = re.findall('"msg":(.*?),', response.text)[0].strip('\'')
        if msg == '"ok"':
            car_id = re.findall("'tarid':(.*?),", response.text)[0].strip('\'')
            return car_id
        elif msg == '"没有查到相关数据，请更改查询条件"':
            return None
        else:
            return 'retry'
    return 'retry'


@strong_common_retry(max_retry=4, exception=(requests.ReadTimeout,))
def get_car_detail(car_id, proxy):
    timstamp = int(time.time())
    url = "http://www.chinacar.com.cn/Home/GonggaoSearch/GonggaoSearch/search_param/id/{}".format(car_id)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7",
        "Cache-Control": "max-age=0",
        "Host": "www.chinacar.com.cn",
        "Proxy-Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Cookie": "PHPSESSID=ajqbk8np4n84tl4caadganhho0; clcp_list=943511%7C; Hm_lvt_6c1a81e7deb77ce536977738372f872a={}; Hm_lpvt_6c1a81e7deb77ce536977738372f872a={}; ck_gg_1=y".format(
            timstamp, timstamp)
    }
    # 代理IP
    proxies = {
        "http": "http://{}".format(proxy)
    }
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        HTML = etree.HTML(response.text)
        result = HTML.xpath("/html/body/table/tbody/tr[2]/td[4]/span[1]/a/text()")
        r2 = HTML.xpath("/html/body/table/tbody/tr[2]/td[2]/a/text()")
        return (result, r2)


if __name__ == '__main__':
    model_list = get_car_category('model_list.csv')
    for model in tqdm(model_list[:5000]):
        ip = random.choice(get_proxy())
        carID = get_car_id(model, ip)
        car_detail = get_car_detail(carID, ip)
