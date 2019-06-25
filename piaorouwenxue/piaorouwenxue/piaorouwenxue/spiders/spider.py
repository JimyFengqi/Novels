# -*- coding: utf-8 -*-
# @Date     : 2018-11-07 17:11:13
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6

#coding:utf-8
import scrapy
import re
from scrapy.http import Request
from piaorouwenxue.items import PiaorouwenxueItem

class Myspider(scrapy.Spider):
	name = "piaorouwenxue"
	allowed_domains = ["prwx.com"]
	main_url = "https://www.prwx.com"
	shuku_url_base='https://www.prwx.com/all/0_0_%s.html'
	

	def start_requests(self):
		yield Request(self.main_url+'/all.html',self.parse)
	def parse(self, response):

		max_page=response.xpath('//*[@class="pagelink"]/a[last()]/@href').extract_first()
		max_page  = max_page.split('/')[-1].split('.')[0].split('_')[-1]
		
		for page_num in range(1,int(max_page)+1):
		#for page_num in range(2,3):
			new_url=self.shuku_url_base % str(page_num)
			print(new_url)
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,dont_filter=True)
	def get_novel(self,response):
		novel_contents=response.xpath('//*[@id="content"]/table[2]/tr')
		print (len(novel_contents))
		novel_contents = novel_contents[1:]
		print('每一页有%d 个小说' %  len(novel_contents))
		for content in novel_contents:
			item 				= 		PiaorouwenxueItem()

			novelname			=		content.xpath('td[1]/a/text()').extract_first()
			novelurl			=		content.xpath('td[1]/a/@href').extract_first()
			novelid 			=		novelurl.split('/')[-1].split('.')[0]
			author 				=		content.xpath('td[3]/text()').extract_first()
			novelstatus  		= 		content.xpath('td[6]/text()').extract_first()
			novelstatus  		=       novelstatus  if '连载' in novelstatus else '完结'

			item['novelname']	=		novelname
			item['author']		= 		author
			item['novelid']		= 		novelid
			item['novelstatus'] =		novelstatus
			item['novelurl']   	=		novelurl
			#print(item)
			yield Request(novelurl,self.get_details,dont_filter=True,meta={'item':item})

	def get_details(self,response):
		item		=	response.meta['item']
		imgurl		=	response.xpath('//*[@id="content"]/table/tr[4]/td/table/tr/td[2]/a/img/@src').extract_first()

		contents    =  	response.xpath('//*[@id="content"]/table/tr[1]/td/table')

		downloadNum	=	contents.xpath('tr[4]/td[2]/text()').extract_first()
		downloadNum	= 	downloadNum.split('：')[-1]


		noveltype  	= 	contents.xpath('tr[2]/td[1]/text()').extract_first()
		noveltype	= 	noveltype.split('：')[-1]

		novelsize  	= 	contents.xpath('tr[2]/td[4]/text()').extract_first()
		novelsize	= 	float(novelsize.split('：')[-1].split('字')[0])*2

		#novelstatus = 	contents.xpath('tr[2]/td[3]/text()').extract_first()
		#novelstatus = 	novelstatus.split('：')[-1]

		simplyintroduce = 	response.xpath('//*[@id="content"]/table/tr[4]/td/table/tr/td[2]/div').xpath('string(.)').extract_first().strip()
		simplyintroduce = 	simplyintroduce.replace('\xa0','').split('内容简介：')[-1][:200]

		zipdownload     = 	'None'		
		downloadpage_ur = 	response.xpath('//*[@id="content"]/table/tr[4]/td/table/tr/td[1]/a[last()]/@href').extract_first()

		item['downloadNum']=downloadNum
		item['novelsize']=novelsize
		item['noveltype']=noveltype
		item['imgurl']=imgurl
	
		item['zipdownload']=zipdownload
		item['simplyintroduce']=simplyintroduce
		yield Request(downloadpage_ur,self.get_download,meta={'item':item},dont_filter=True)

	def get_download(self,response):
		item = response.meta['item']
		txtdownload =  response.xpath('//*[@id="TxtdownTop"]/a[2]/@href').extract_first()
		item['txtdownload']=txtdownload
		#print(item)
		yield(item)