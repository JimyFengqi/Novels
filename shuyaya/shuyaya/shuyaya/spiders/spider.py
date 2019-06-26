#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-11 00:00:06
# @Author  : Jimy_Fengqi (jmps515@163.com)
# @Link    : https://blog.csdn.net/qiqiyingse/
# @Version : $Id$

import scrapy
import re
from scrapy.http import Request
from shuyaya.items import ShuyayaItem


class Myspider(scrapy.Spider):
	name = "shuyaya"
	allowed_domains = ["shuyaya.cc"]
	main_url = "https://www.shuyaya.cc/all"
	shuku_url_base='https://www.xuanquge.com/shuku/0_0_0_0_default_0_%s.html'

	txt_base_url='https://txt.xuanquge.com/home/down/txt/id/%s'
	zip_base_url='http://down.shuyaya.cc/zip/%s.zip'
	img_url_base='https://img.xuanquge.com/Cover/%s/%s.jpg'
	def start_requests(self):
		yield Request(self.main_url,self.parse)

	def parse(self, response):
		#print(response.url)
	
		max_novel_num=response.xpath('//*[@class="aubook2 clearfix"]/h4')
		print('max_novel_num=(%d)' % len(max_novel_num))

		#part_novel = max_novel_num[0:10]
		#for novel in part_novel:
		for novel in max_novel_num:

			novelname = novel.xpath('a/text()').extract_first()
			novelurl = novel.xpath('a/@href').extract_first()
			novelid  = novelurl.split('/')[-2]
			author = novel.xpath('text()').extract_first()
			author = author.split('/')[-1]

			item=ShuyayaItem()
			item['novelname']=novelname
			item['author']=author
			item['novelid']=novelid
			item['novelurl']=novelurl

			yield Request(novelurl,self.get_novel,dont_filter=True,meta={'item':item})

	def get_novel(self,response):
		item = response.meta['item']

		novelstatus=response.xpath('//*[@class="con_lwrap"]/span/@class').extract_first()
		novelstatus = '已完结' if  novelstatus == 'ywjico' else '连载中'

		zipdownload	    = 	self.zip_base_url % (item['novelname'])
		imgurl 			=   response.xpath('//*[@class="con_limg"]/img/@src').extract_first()
		simplyintroduce =	response.xpath('//*[@class="r_cons"]/text()').extract_first()
		simplyintroduce = simplyintroduce.replace('内容简介：','').strip()

		noveltype 	= 	response.xpath('//*[@class="r420"]/p/span[2]/a/text()').extract_first()
		novelsize 	= 	response.xpath('//*[@class="r420"]/p/span[4]/text()').extract_first()

		if 'KB' in novelsize:
			novelsize= float(re.split('KB',novelsize)[0])*1024
		elif 'MB' in novelsize:
			novelsize= float(re.split('MB',novelsize)[0])*1024*1024
		else:
			novelsize= novelsize


		item['downloadNum']=	'None'
		item['imgurl']=imgurl
		item['novelsize']=novelsize
		item['novelstatus']=novelstatus
		item['noveltype']=noveltype
		item['txtdownload']='None'
		item['zipdownload']=zipdownload
		item['simplyintroduce']=simplyintroduce
		if novelsize > 10:
			#print(item)
			yield item
			