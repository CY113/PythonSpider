#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 11:40
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : MongoDBHelper.py
# @Software: PyCharm
# @Desc    : 链接Mongo数据库
import datetime

import pymongo
from scrapy.utils.project import get_project_settings


class MongoDBHelper:
    def __init__(self):
        settings = get_project_settings()
        mongo_url = settings["MONGO_URL"]
        mongo_db = settings["MONGO_DB"]
        client = pymongo.MongoClient(mongo_url)
        self.db = client[mongo_db]

    def get_status(self, event_id):
        """
        后端标识查询
        :param event_id: 事件ID
        :return:
        """
        coll = self.db["event_overview"]
        data = coll.find_one({"event_id": event_id}, {"delYn": 1, "factor": 1})
        if data:
            return data["delYn"], data["factor"]
        else:
            return None, None

    def get_event_id(self):
        """
        去重查询事件ID
        :return:
        """
        eventList = []

        coll_list = self.db["events_list"]
        coll_overview = self.db["event_overview"]
        events = coll_list.find({}, {"event_id": 1, "_id": 0})
        new_count = 0  # 新增事件计数
        continue_count = 0  # 未结束事件计数
        complete_count = 0  # 三天内结束事件，因存在事件已结束知微仍更新的情况，所以事件结束时间超过3天的事件不去爬取
        for event_id in events:
            flag = coll_overview.find({"event_id": event_id["event_id"]})
            if flag.count() != 0:
                try:
                    for x in flag:
                        latestTime = datetime.datetime.strptime(x["data"]["hourHeatRatio"][-1]["timePoint"],
                                                                '%Y-%m-%d %H')
                        pytime = datetime.datetime.strptime(x["pytime"], '%Y-%m-%d %H:%M:%S')
                        if not x["data"]["isEnd"]:
                            continue_count += 1
                            eventList.append(event_id["event_id"])
                        elif x["data"]["isEnd"] and (pytime - latestTime).days < 3:
                            complete_count += 1
                            eventList.append(event_id["event_id"])
                except:
                    eventList.append(event_id["event_id"])
            else:
                new_count += 1
                eventList.append(event_id["event_id"])
        print("待爬取事件个数：{}，其中新增事件{}个，未结束事件{}个，3天内结束事件{}个".format(new_count + continue_count + complete_count, new_count,
                                                                continue_count, complete_count))
        return eventList

    def get_event_id_img(self):
        """
        去重查询事件ID
        :return:
        """
        eventList = []

        coll_list = self.db["events_list"]
        coll_overview = self.db["event_overview"]
        events = coll_list.find({}, {"event_id": 1, "img": 1, "_id": 0})
        new_count = 0  # 新增事件计数
        continue_count = 0  # 未结束事件计数
        complete_count = 0  # 三天内结束事件，因存在事件已结束知微仍更新的情况，所以事件结束时间超过三天的事件不去爬取
        for event_id in events:
            flag = coll_overview.find({"event_id": event_id["event_id"]})
            if flag.count() != 0:
                try:
                    for x in flag:
                        latestTime = datetime.datetime.strptime(x["data"]["hourHeatRatio"][-1]["timePoint"],
                                                                '%Y-%m-%d %H')
                        pytime = datetime.datetime.strptime(x["pytime"], '%Y-%m-%d %H:%M:%S')
                        if not x["data"]["isEnd"]:
                            continue_count += 1
                            eventList.append((event_id["event_id"], event_id["img"]))
                        elif x["data"]["isEnd"] and (pytime - latestTime).days < 3:
                            complete_count += 1
                            eventList.append((event_id["event_id"], event_id["img"]))
                except:
                    eventList.append((event_id["event_id"], event_id["img"]))
            else:
                new_count += 1
                eventList.append((event_id["event_id"], event_id["img"]))
        print("待爬取事件个数：{}，其中新增事件{}个，未结束事件{}个，三天内结束事件{}个".format(new_count + continue_count + complete_count, new_count,
                                                                continue_count, complete_count))
        return eventList
