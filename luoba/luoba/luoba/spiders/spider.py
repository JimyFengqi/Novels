#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-11 00:00:06
# @Author  : Jimy_Fengqi (jmps515@163.com)
# @Link    : https://blog.csdn.net/qiqiyingse/
# @Version : $Id$

import scrapy
import re
from scrapy.http import Request
from luoba.items import LuobaItem


class Myspider(scrapy.Spider):
	name = "luoba"
	allowed_domains = ["txt81.com"]
	main_url = "http://www.txt81.com/"
	shuku_url_base='http://www.txt81.com/shu/0_0_0_0_default_0_%s.html'

	txt_base_url='http://www.txt81.com/home/down/txt/id/%s'
	zip_base_url='http://www.txt81.com/home/down/zip/id/%s'
	img_url_base='http://www.txt81.com/Cover/%s/%s.jpg'

	def start_requests(self):
		yield Request(self.main_url+'shu/',self.parse)
	def parse(self, response):
		print(response.url)
		max_page=response.xpath('//*[@id="taoshumain"]/div[31]/a[11]/@href').extract_first()
		max_page=max_page.split('.')[-2].split('_')[-1]
		print(max_page)
		max_novel_num=response.xpath('//*[@class="bookstorbt1"]/span/text()').extract_first()
		print('max_novel_num=(%s)' % max_novel_num)
		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,2):
			new_url=self.shuku_url_base % str(page_num)
			print(new_url)
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,dont_filter=True)
	def get_novel(self,response):
		novel_contents=response.xpath('//*[@class="storelistbt5"]/ul')
		print('每一页有%d 个小说' %  len(novel_contents))
		
		item=LuobaItem()
		for content in novel_contents.xpath('li[2]'):
			#downloadNum=content.xpath('span/text()').extract_first()
			
			novelname	=	content.xpath('a[2]/@title').extract_first()
			novelurl	=	content.xpath('a[2]/@href').extract_first()
			author 		=	content.xpath('p[1]/a[1]/text()').extract_first()
			noveltype 	=	content.xpath('p[1]/a[3]/text()').extract_first()
			downloadNum =	content.xpath('span/text()').extract_first()
			downloadNum	=	downloadNum.split('：')[-1].strip()

			novelid 	=	novelurl.split('/')[-2]
			
			novelsize 	=	content.xpath('p[3]/text()').extract_first()
			novelsize	=	novelsize.split('大小：')[1].split('更新')[0].strip()
			if 'KB' in novelsize:
				novelsize= float(re.split('KB',novelsize)[0])*1024
			elif 'MB'in novelsize:
				novelsize= float(re.split('MB',novelsize)[0])*1024*1024
			else:
				novelsize = novelsize

			txtdownload	=	self.txt_base_url % (novelid)
			zipdownload	=	self.zip_base_url % (novelid)

			imgurl 		= 	content.xpath('a[1]/img[1]/@src').extract_first()
			simplyintroduce=content.xpath('p[2]/text()').extract_first().strip()

			item['novelname']=novelname
			item['author']=author
			item['novelstatus']='None'
			item['downloadNum']=downloadNum
			item['novelurl']=novelurl
			item['imgurl']=imgurl
			item['novelid']=novelid
			item['novelsize']=novelsize
			item['noveltype']=noveltype
			item['txtdownload']=txtdownload
			item['zipdownload']=zipdownload
			item['simplyintroduce']=simplyintroduce
			#print(novelname,author,novelid,noveltype,novelsize,downloadNum,novelurl)
			#print(imgurl,txtdownload,zipdownload)
			#print(simplyintroduce)
			if novelsize > 10:
				yield item