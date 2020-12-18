# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.utils.project import get_project_settings


class AmapPipeline:
    def __init__(self):
        self.settings = get_project_settings()
        self.host = self.settings['MONGO_HOST']
        self.port = self.settings['MONGO_PORT']
        self.db = self.settings['MONGO_DB']

    def process_item(self, item, spider):
        client = pymongo.MongoClient(self.host)
        db = client[self.db]
        coll_name = item['belong']
        coll = db[coll_name]
        coll.insert(dict(item))  # 根据城市名称插入相应表
        return item
