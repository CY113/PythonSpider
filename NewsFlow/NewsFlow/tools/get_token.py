#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 10:46
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : get_token.py
# @Software: PyCharm
# @Desc    : 根据账号获取登录token


import requests
import json
import random


def get_token():
    url = "https://ef.zhiweidata.com/loginPhonePwd.do"
    user_list = ["12345674567", "12345674567", "12345674567", "12345674567"]
    data = {
        "phone": random.choice(user_list),
        "password": "MTIzNDU2YWJj",
    }
    headers = {
        "Host": "ef.zhiweidata.com",
        "Connection": "keep-alive",
        "Content-Length": "46",
        "Accept": "application/json,text/plain,*/*",
        "Sec-Fetch-Dest": "empty",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "Origin": "https://ef.zhiweidata.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Referer": "https://ef.zhiweidata.com/login",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "zh-CN,zh",
        "q": "0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    res = requests.post(url, json=data, headers=headers)
    if res.status_code == 200:
        result = json.loads(res.text)
        if result["state"]:
            token = result["data"]["token"]
            return token
        else:
            raise ValueError("密码错误，请检查")
    elif res.status_code == 403:
        raise ValueError('账号出现问题，请查看原因')


if __name__ == '__main__':
    results = get_token()
    print(results)
