# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import logging
from ipeenCrawl.items import *
from urllib.parse import quote_plus
from pymongo import MongoClient, ASCENDING
from scrapy.exceptions import DropItem

class IpeencrawlPipeline(object):
    def __init__(self, host, port, db_name, db_collection, user, password):
        uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), host)
        self.db_collection = db_collection
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('LOCALHOST'),
            port=crawler.settings.get('PORT'),
            db_name=crawler.settings.get('MONGO_DATABASE'),
            db_collection=crawler.settings.get('COLLECTIONS'),
            user=crawler.settings.get('USER'),
            password=crawler.settings.get('PASSWORD'),
        )

    def process_item(self, item, spider):
        if isinstance(item, RestaurantItem):
            validate_item = ['rid', 'name', 'avgCost', 'address', 'classify', 'environmentRate', 'serviceRate', 'tasteRate']
            if self.validate_data(validate_item, item):
                self.deal_restaurant(item)
                self.db[self.db_collection['restaurant']].insert_one(dict(item))
            else:
                raise DropItem('Loss Data')
        elif isinstance(item, UserComment):
            validate_item = ['rid', 'uid', 'context', 'rate']
            if self.validate_data(validate_item, item):
                self.deal_user(item)
                self.db[self.db_collection['comment']].insert_one(dict(item))
            else:
                raise DropItem('Loss Data')
        return item

    def deal_restaurant(self, item):
        item['rid'] = self.search_str('([0-9]+)', item['rid'])
        item['avgCost'] = int(self.search_str('[0-9]+', item['avgCost'], default = 0))
        item['tel'] = self.search_str('[0-9]+-[0-9]+-[0-9]+', item['tel'])
        item['address'] = self.search_str('([0-9.0-9]+,[0-9.0-9]+)', item['address'])
        tmp_time = set()
        for line in item['hours']:
            for time in re.findall('[0-9]+:[0-9]+~[0-9]+:[0-9]+', line):
                tmp_time.add(time)
        item['hours'] = list(tmp_time)

    def deal_user(self, item):
        item['uid'] = self.search_str('home/([0-9A-Za-z]+)', item['uid'], group_num=1)
        item['rid'] = self.search_str('[0-9]+', item['rid'])

    def validate_data(self, validate_item, item):
        for key in validate_item:
            if item.get(key, default=None) is None:
                logging.info('----------------------------------------------------')
                return False
        return True
    
    def search_str(self, pattern, line, default = '', group_num = 0):
        if line is not None and pattern is not None:
            result = re.search(pattern, line)
            if result:
                return result.group(group_num)
        return default

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()
