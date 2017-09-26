# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class RestaurantItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rid = Field()
    name = Field()
    classify = Field()
    avgCost = Field()
    tel = Field()
    address = Field()
    hours = Field()
    environmentRate = Field()
    serviceRate = Field()
    tasteRate = Field()

class UserRate(Item):
    userId = Field()
    userTasteRate = Field()
    userServiceRate = Field()
    userEnviromentRate = Field()
    restaurantId = Field()
    usefulCount = Field()

class UserComment(Item):
    rid = Field()
    uid = Field()
    rate = Field()
    context = Field()
