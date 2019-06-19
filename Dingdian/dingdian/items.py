# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	novel_name = scrapy.Field()#小说名字
	author = scrapy.Field()#作者
	novel_instroduce_url=scrapy.Field()#小说简介地址
	novelurl=scrapy.Field()#小说章节列表地址
	serialstatus = scrapy.Field()#状态
	serialnumber = scrapy.Field()#连载字数
	category = scrapy.Field()#小说类别
	name_id = scrapy.Field()#小说编号
	collect_num_total=scrapy.Field()#总收藏
	click_num_total=scrapy.Field()#总点击
	novel_breif=scrapy.Field()#小说简介
	
	chapterurl = scrapy.Field()#小说章节地址
	chaptername = scrapy.Field()#小说章节名字


'''
class DDNovelContentItem(scrapy.Item):
	id_name = scrapy.Field()#小说编号
	chaptercontent = scrapy.Field()#小说章节内容名字
	num = scrapy.Field()#小说名字
	chaptername = scrapy.Field()#小说章节名字
	chapterurl = scrapy.Field()#小说章节地址
'''