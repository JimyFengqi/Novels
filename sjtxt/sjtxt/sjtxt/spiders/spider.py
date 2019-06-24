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
from sjtxt.items import SjtxtItem

class Myspider(scrapy.Spider):
	name = "sjtxt"
	allowed_domains = ["xsjtxt.com"]
	main_url = "https://www.xsjtxt.com"

	listtype=['https://www.xsjtxt.com/soft/%s/Soft_0%s_1.html'% (x,x) for x in range(15)]
	listtype.append('https://www.xsjtxt.com/soft/quanben/index_1.html')


	def start_requests(self):
		for value in self.listtype:
			yield Request(value)

	def parse(self, response):
		max_page=response.xpath('//*[@class="tspage"]/a[last()]/@href').extract_first()
		max_page= '1' if None == max_page else	max_page.split('/')[-1].split('.')[0].split('_')[-1]
		#print(response.url,max_page)
		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,2):	
			new_url =   response.url[:-6] + str(page_num) + '.html'
			#print(new_url)
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,dont_filter=True)

	def get_novel(self,response):

		novel_contents=response.xpath('//*[@class="listBox"]/ul/li')
		#print(' 当前页面 [%s], 每一页有%d 个小说' %  (response.url,len(novel_contents)))

		for content in novel_contents:
			item					=	SjtxtItem()
		
			novelname   			=   content.xpath('a/text()').extract_first()			
			novelname 	=  novelname  if None == novelname else	re.sub('《|》','',novelname.strip())
			novelname = novelname if '全集' not in novelname or None == novelname else novelname.split('全集')[0]

			novelurl 	= 	self.main_url  +	content.xpath('a/@href').extract_first()
			novelid 	= 	novelurl.split('.html')[0].split('/')[-1][8:]

			imgurl 		=	self.main_url + content.xpath('a/img/@src').extract_first()
			#imgurl	    =   imgurl if 'http' in imgurl else  self.main_url + imgurl
			item['novelname']=novelname
			item['novelid']=novelid
			item['novelurl']=novelurl
			item['imgurl']=imgurl

			yield Request(novelurl,self.parse_details,meta={'item':item},dont_filter=False)


	def parse_details(self,response):
		item = response.meta['item']
		noveltype		=		response.xpath('//*[@class="wrap position"]/span/a[2]/text()').extract_first()
		contents 		= 		response.xpath('//*[@class="detail_right"]/ul/li/text()').extract()
		downloadNum     =      	contents[0].split('：')[1]
		novelsize     	=      	contents[1].split('：')[1]
		if 'KB' in novelsize:
			novelsize	= 		float(re.split('KB',novelsize)[0])*1024
		elif 'MB' in novelsize:
			novelsize	= 		float(re.split('MB',novelsize)[0])*1024*1024
		else:
			novelsize	= 		novelsize

		novelstatus 	= 		contents[4].split('：')[1]

		author 			=		contents[5].split('：')[1]
		author 			= 		'None'  if '' == author else author

		#simplyintroduce = 		response.xpath('//*[@class="showInfo"]').xpath('string(.)').extract()
		simplyintroduce = 		response.xpath('//*[@class="showInfo"]/p/text()').extract_first()
		simplyintroduce = 		simplyintroduce.strip()

		zipdownloadinfo		=		response.xpath('//*[@class="showDown"]/ul/li[3]/script/text()').extract_first()
		zipdownloadinfo	    =		re.split('\(|\)|\"',zipdownloadinfo)
		zipdownload	 		=		zipdownloadinfo[4]
		#print(zipdownloadinfo)
		try:
			txtdownloadinfo		=	    response.xpath('//*[@class="showDown"]/ul/li[4]/script/text()').extract_first()
			txtdownloadinfo	    =		re.split('\(|\)|\"',txtdownloadinfo)
			txtdownload	 		=		txtdownloadinfo[4]
		except:
			txtdownload    		=		'None'



		item['author'] 			=	author
		item['noveltype']		=	noveltype
		item['downloadNum']		=	downloadNum
		item['novelstatus']		=	novelstatus
		item['novelsize']		=	novelsize
		item['txtdownload']		=	txtdownload
		item['zipdownload']		=	zipdownload
		item['simplyintroduce']	=	simplyintroduce
		yield(item)


