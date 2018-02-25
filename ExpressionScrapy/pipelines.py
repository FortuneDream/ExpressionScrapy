# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

# 对于item的处理，重复的检查
from scrapy.exceptions import DropItem


from ExpressionScrapy.items import GaoxiaodoutuItem


class ExpressionscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


# 去重
class DuplicatePipeline(object):
    def __init__(self):
        self.set = set()

    def process_item(self, item, spider):
        if isinstance(item, GaoxiaodoutuItem):
            if item['pic_id'] in self.set:
                raise DropItem("Duplicate Item found : %s" % item)
            else:
                self.set.add(item['pic_id'])
                return item
        return item


# 存入mongodb
class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 拿到setting配置信息
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # 表名
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
