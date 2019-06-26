# -*- coding: utf-8 -*-
# @Date     : 2019-06-24 10:11:13
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6

#coding:utf-8
import scrapy
import re
from scrapy.http import Request
from dangshuwang.items import DangshuwangItem

class Myspider(scrapy.Spider):
	name = "dangshuwang"
	allowed_domains = ["downbook.net"]
	main_url = "https://www.downbook.net"

	listtype=['https://www.downbook.net/TXT/zt/1_1.html',
		'https://www.downbook.net/TXT/list1_1.html',
		'https://www.downbook.net/TXT/list2_1.html',
		'https://www.downbook.net/TXT/list26_1.html']
	txt_url_base = 		'http://txt.downbook.net/TXT/%s.txt'
	def start_requests(self):
		for value in self.listtype:
			yield Request(value)

	def parse(self, response):
		shukulist=response.xpath('//*[@class="pdr1"]/ul/a[(@title)]/@href').extract()
		if [] == shukulist:
			shukulist=response.xpath('//*[@class="lr0"]/ul/a[(@title)]/@href').extract()
		shukulist = [self.main_url + x  for x in shukulist[:-2]]
		for url in shukulist:
			yield Request(url,self.parse_getPage,dont_filter=False)

	def parse_getPage(self, response):
		max_page = response.xpath('//*[@class="xlh"]/code/a[last()]/@href').extract_first()
		if None == max_page:
			max_page = response.xpath('//*[@class="tagpage"]/a[last()]/@href').extract_first()
		max_page= '1' if None == max_page else	max_page.split('.')[0].split('_')[-1]

		for page_num in range(1,int(max_page)+1):
		#for page_num in range(2,3):	
			new_url =   response.url[:-6] + str(page_num) + '.html'
			print(response.url,max_page,new_url)
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,dont_filter=True)
		
	def get_novel(self,response):

		novel_contents=response.xpath('//*[@class="listl"]/ul/li')
		if [] == novel_contents:
			novel_contents=response.xpath('//*[@class="listtag"]/ul/li')
		print('当前页面包含%d 个小说 %s'  % (len(novel_contents), response.url))
		for content in novel_contents:
			item					=	DangshuwangItem()
			imgurl  				=	content.xpath('a/img/@src').extract_first()	
			imgurl   				=   imgurl if 'http' in imgurl else self.main_url  + imgurl

			novelname   			=   content.xpath('a/img/@alt').extract_first()			
			novelurl 				= 	self.main_url  +	content.xpath('a/@href').extract_first()
			novelid 				= 	novelurl.split('/')[-1].split('.')[0].split('_')[-1]
			
			item['novelname']=novelname
			item['novelid']=novelid
			item['novelurl']=novelurl
			item['imgurl']=imgurl
			yield Request(novelurl,self.parse_details,meta={'item':item},dont_filter=False)


	def parse_details(self,response):
		item = response.meta['item']

		txtdownload     = 		response.xpath('//*[@class="down"]/a[2]/@href').extract_first()
		zipdownload     =		"None"
		#contents 		= 		response.xpath('//*[@class="cl1"]/ul').xpath('string(.)').extract()
		contents 		= 		response.xpath('//*[@class="cl1"]/ul/text()').extract()
		
		noveltype       =       contents[0]
		#noveltype		=		response.xpath('//*[@class="mbx"]/a[4]/text()').extract_first()
		
		author  		=  		contents[1]
		novelsize  		=  		contents[2]
		if 'KB' in novelsize:
			novelsize	= 		float(re.split('KB',novelsize)[0])*1024
		elif 'MB' in novelsize:
			novelsize	= 		float(re.split('MB',novelsize)[0])*1024*1024
		else:
			novelsize	= 		float(novelsize)
		
		novelstatus  	=  		contents[3]
		novelstatus 	=		'完结' if '全集' in  novelstatus else novelstatus

		simplyintroduce = 		response.xpath('//*[@class="jj"]').xpath('string(.)').extract_first()
		simplyintroduce = 		simplyintroduce.strip()[:150]
		downloadNum     =      	'None'


		item['author'] 			=	author
		item['noveltype']		=	noveltype
		item['downloadNum']		=	downloadNum
		item['novelstatus']		=	novelstatus
		item['novelsize']		=	novelsize
		item['txtdownload']		=	txtdownload
		item['zipdownload']		=	zipdownload
		item['simplyintroduce']	=	simplyintroduce
		if novelsize > 50:
			#print(item)
			yield(item)



		