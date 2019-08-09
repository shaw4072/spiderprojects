# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from maigoo.items import MongoItem


class MaigooPipeline(object):
    def process_item(self, item, spider):
        return item


# 通用存入mongodb
class MongoPipeline(object):
    def __init__(self, crawler):
        self.mongo_host = crawler.settings.get('MONGO_HOST')
        self.mongo_port = crawler.settings.get('MONGO_PORT')
        self.mongo_db = crawler.settings.get('MONGO_DB', 'items')
        self.mongo_collection=crawler.settings.get('MONGO_COLLECTION', 'scrapy_items')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_host,port=self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item,MongoItem):
            self.db[self.mongo_collection].insert_one(dict(item))
        return item


#通用去空格(去除两边空格)
class StripPipeline(object):

    def process_item(self, item, spider):
        keys = list(item.keys())     #py3 dict.keys()返回 set
        for i in range(len(keys)):
            tmpvalue=item[keys[i]]
            if isinstance(tmpvalue,str):
                item[keys[i]]=tmpvalue.strip()
        return item

