#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 13:55
# @Author  : Tian Hao
# @Email   : hao.tian@intcolon.cn
# @File    : DBHelper.py
# @Software: PyCharm
# @Desc    : 数据库封装


import pymysql
from scrapy.utils.project import get_project_settings


class DBHelper(object):
    def __init__(self):
        self.settings = get_project_settings()
        self.host = self.settings["MYSQL_HOST"]
        self.port = self.settings["MYSQL_PORT"]
        self.user = self.settings["MYSQL_USER"]
        self.password = self.settings["MYSQL_PASSWD"]
        self.db = self.settings["MYSQL_DBNAME"]
        # 数据库连接有数量限制，所以初始化时建立一次连接或连接池
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                    passwd=self.password, db=self.db,
                                    charset='utf8')

    def insert_task(self, sql, params):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        cur.close()

    def query_task(self, sql, *params):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        results = cur.fetchall()
        cur.close()
        return results

    def query_fetchone_task(self, sql, params):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        results = cur.fetchone()
        cur.close()
        return results

    def update_task(self, sql, params):
        """
        更新数据库表
        :param sql: str
                SQL语句
        :param params: tuple
                参数
        :return:
        """
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        cur.close()

    def delete_task(self, sql, params):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        cur.close()
