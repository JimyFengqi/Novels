# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhuajishuwuItem(scrapy.Item):
    novelname = scrapy.Field()
    author = scrapy.Field()
    novelid = scrapy.Field()
    noveltype = scrapy.Field()
    novelsize = scrapy.Field()
    novelstatus = scrapy.Field()
    downloadNum = scrapy.Field()
    novelurl = scrapy.Field()
    imgurl=scrapy.Field()
    txtdownload=scrapy.Field()
    zipdownload=scrapy.Field()
    simplyintroduce=scrapy.Field()

