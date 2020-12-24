#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 15:09
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : crawl_ins.py
# @Software: PyCharm
# @Desc    : Ins爬虫抓取
import base64
import json
import logging
import re
import time
from urllib.parse import urlencode

import requests


def get_hash():
    """
    获取query_hash
    :return:
    """
    return "7dabc71d3e758b1ec19ffb85639e427b"


def getFirstPage(label):
    """
    如果是第一页，需要获取end_cursor和csrf_token
    :param label:
    :return:
    """
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36",
        "cookie": 'ig_did=C09A5BCE-D68E-4033-A3F3-9EF1E7C97DAC; mid=Xroa-AALAAFrkYx5vf2bVdFd9a1E; csrftoken=XlD7OxRbbD4l4QoUOqPp4HVLDEWP6ehM; ds_user_id=30659194200; sessionid=30659194200%3AfVwlHA2ZGINGlr%3A14; shbid=5599; shbts=1592291859.2780437'
    }
    url = "https://www.instagram.com/explore/tags/{}/".format(label)
    response = requests.get(url, headers=headers, verify=False)
    data = {"node": []}
    if response.status_code == 200:
        res = re.search('_sharedData = {"config":(.*);</script>', response.text).group().strip(
            "_sharedData = ").strip(
            ";</script>")
        result = json.loads(res)
        data["csrf_token"] = result["config"]["csrf_token"]
        data["end_cursor"] = \
            result["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
        data["has_next_page"] = \
            result["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"][
                "has_next_page"]
        edges = result["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        for edge in edges:
            node = {
                "type_name": edge["node"]["__typename"],
                "shortcode": edge["node"]["shortcode"],
                "timestamp": time.time(),
                "display_url": "https://contentfacapi.intcolon.com/img?addr=" + base64.b64encode(
                    edge["node"]["thumbnail_resources"][2]["src"].encode("utf-8")).decode("utf-8")}
            data["node"].append(node)
        return data


def get_url_list(label, csrf_token=None, end_cursor=None):
    """
    获取缩略图页面数据
    :param label: # 标签名
    :param csrf_token: # 跨域token
    :param end_cursor: # after
    :return:
    """
    data = {"node": []}
    if csrf_token is None or end_cursor is None:
        first = getFirstPage(label)
        return first
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
            "accept-language": "zh-CN,zh;q=0.9",
            "x-csrftoken": csrf_token
        }
        variable_dict = {
            "tag_name": label.strip(" ").replace(" ", "").lower(),
            "first": 12,
            "after": end_cursor
        }
        query_hash = get_hash()
        params = {
            "query_hash": query_hash,
            "variables": json.dumps(variable_dict)
        }
        url = 'https://www.instagram.com/graphql/query/?{}'.format(urlencode(params))
        response = requests.get(url, headers=headers, verify=False)
        try:
            if response.status_code == 200:
                res = json.loads(response.text)
                print(res)
                info = res["data"]["hashtag"]["edge_hashtag_to_media"]
                data["csrf_token"] = csrf_token
                data["end_cursor"] = info["page_info"]["end_cursor"]  # 起始
                data["has_next_page"] = info["page_info"]["has_next_page"]  # 翻页标识
                edges = info["edges"]
                for edge in edges:
                    node = {
                        "type_name": edge["node"]["__typename"],
                        "shortcode": edge["node"]["shortcode"],
                        "timestamp": time.time(),
                        "display_url": "https://contentfacapi.intcolon.com/img?addr=" + base64.b64encode(
                            edge["node"]["thumbnail_resources"][2]["src"].encode("utf-8")).decode("utf-8")}
                    data["node"].append(node)
                return data
            else:
                logging.warning(response.text)
        except Exception as e:
            logging.error(response.text)


def getStream(addr):
    img_url = base64.b64decode(addr)
    response = requests.get(img_url, stream=True, verify=False)
    if response.status_code == 200:
        for i in response.iter_content(1024):
            yield i
    else:
        logging.error(response.text)


def get_detail(short_code):
    url = "https://www.instagram.com/graphql/query/?query_hash=c9ba52b58dde9f9195170a871b72ba4a&variables=%7B%22shortcode%22%3A%22{}%22%2C%22child_comment_count%22%3A3%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22has_threaded_comments%22%3Atrue%7D".format(
        short_code)
    response = requests.get(url, verify=False)
    try:
        if response.status_code == 200:
            info = json.loads(response.text)
            data = info["data"]["shortcode_media"]
            __typename = data["__typename"]
            node = {}
            node["typeName"] = __typename
            if __typename == "GraphVideo":  # 视频
                node["url"] = "https://contentfacapi.intcolon.com/img?addr=" + base64.b64encode(
                    data["video_url"].encode("utf-8")).decode(
                    "utf-8")  # 展示地址
                node["download_url"] = "https://contentfacapi.intcolon.com/download?addr=" + base64.b64encode(
                    data["video_url"].encode("utf-8")).decode("utf-8") + "&type_name=video"  # 下载地址
                return node
            elif __typename == "GraphSidecar":  # 组图
                url_list = data["edge_sidecar_to_children"]["edges"]
                node["url"] = []
                node["download_url"] = []
                for url in url_list:
                    node["url"].append("https://contentfacapi.intcolon.com/img?addr=" + base64.b64encode(
                        url["node"]["display_url"].encode("utf-8")).decode("utf-8"))
                    node["download_url"].append("https://contentfacapi.intcolon.com/download?addr=" + base64.b64encode(
                        url["node"]["display_url"].encode("utf-8")).decode("utf-8") + "&type_name=image")
                return node

            elif __typename == "GraphImage":  # 单图
                node["url"] = "https://contentfacapi.intcolon.com/img?addr=" + base64.b64encode(
                    data["display_url"].encode("utf-8")).decode("utf-8")
                node["download_url"] = "https://contentfacapi.intcolon.com/download?addr=" + base64.b64encode(
                    data["display_url"].encode("utf-8")).decode("utf-8") + "&type_name=image"
                return node
    except Exception as e:
        logging.error(response.text)


def download(addr):
    url = base64.b64decode(addr)
    response = requests.get(url, stream=True)
    return response.content
