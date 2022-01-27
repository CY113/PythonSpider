#!/usr/bin/evn python
# -*- coding:UTF-8 -*-
# @Time    : 2022/1/27 14:51
# @Author  : tianhao
# @Email   : alex.tianhao@gmail.com
# @File    : tools.py
# @Software: PyCharm
# @Desc    : 封装工具类
import requests
import time
import json
from functools import wraps

import wrapt


def get_proxy(num=1):
    """
    芝麻代理获取，默认每次只获取一个IP（芝麻IP可用性较高，未添加测试IP模块）
    :param num: int，默认为1，可根据实际需求更改
    :return: List，列表
    """
    result = []
    url = "http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&username=chukou01&&spec=1".format(
        num)
    response = requests.get(url)
    if response.status_code == 200:
        resp = json.loads(response.text)
        if resp['code'] == 0:
            data = resp['data']
            for d in data:
                proxy = d['ip'] + ":" + str(d['port'])
                result.append(proxy)
            return result
        elif resp['code'] == 113:
            raise AttributeError('当前IP未加入代理白名单')
        elif resp['code'] == 114:
            raise AttributeError('余额不足')
        # 在请求地址后加入&username=chukou01&&spec=1 可以无视请求限制
        elif resp['code'] == 111:
            raise AttributeError('提取链接请求太过频繁，超出限制')
        else:
            raise AttributeError('未知错误，查看Code码')
    else:
        raise ConnectionError('访问失败，请查看原因！')


def strong_common_retry(max_retry, exception):
    @wrapt.decorator  # 保留被装饰函数的元信息
    def wrapper(wrapped, instance, args, kwargs):
        """

        :param wrapped:
        :param instance:如果被装饰者为普通类方法，该值为类实例
                        如果被装饰者为 classmethod 类方法，该值为类
                        如果被装饰者为类/函数/静态方法，该值为 None
        :param args:
        :param kwargs:
        :return:
        """
        for i in range(max_retry + 1):
            try:
                res = wrapped(*args, **kwargs)
            except exception:
                print(f"第{i + 1}次重试。")
            else:
                return res
        return {}

    return wrapper


if __name__ == '__main__':
    get_proxy()
