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
from aiqu.items import AiquItem

class Myspider(scrapy.Spider):
	name = "aiqu"
	allowed_domains = ["27xs.cc"]
	listtype={'xuanhuan':'玄幻魔法','wuxia':'武侠修真','dushi':'现代都市','yanqing':'言情小说',
	'chuanyue':'穿越小说','wangyou':'网游小说','kongbu':'恐怖小说','kehuan':'科幻小说','quanben':'全本小说'
	}
	main_url = "https://www.27xs.cc/"
	shuku_url_base='https://www.27xs.cc/%s/list_%s.html'

	downloadpage_url_base='https://www.27xs.cc/txt%s/'
	txt_base_url='http://down.27xs.cc/txt/%s.txt'
	zip_base_url='http://down.27xs.cc/zip/%s.zip'

	def start_requests(self):
		#for i in range(1,2):
		for key,value in self.listtype.items():
			url=self.shuku_url_base % (key,'1')
			yield Request(url,self.parse,meta={'noveltype':value,'novelkey':key})
	def parse(self, response):
		noveltype=response.meta['noveltype']
		novelkey=response.meta['novelkey']


		max_page=response.xpath('//*[@class="pagelink"]/a[last()-1]/@href').extract_first()
		max_page= max_page.split('/')[-1].split('.')[0].split('_')[-1]
		print(noveltype,max_page)

		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,2):
						
			new_url= self.shuku_url_base % (novelkey,str(page_num))
			#print('new_url  = %s' % new_url)
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,meta={'noveltype':noveltype},dont_filter=True)

	def get_novel(self,response):
		noveltype=response.meta['noveltype']
		novel_contents=response.xpath('//*[@class="details list-type"]/ul/li')
		print(' 当前页面 [%s], 每一页有%d 个小说' %  (response.url,len(novel_contents)))

		for content in novel_contents:
			item=AiquItem()
			item['noveltype']=	noveltype	
			novelname   =   content.xpath('span[2]/a/text()').extract_first()
			'''
			if None == novelname:
				novelname   =   content.xpath('a/strong/font/text()').extract_first()
			if None == novelname:
				novelname   =   content.xpath('a/font/text()').extract_first()				
			novelname 	=  novelname  if None == novelname else	re.sub('《|》','',novelname.strip())
			novelname = novelname if '全集' not in novelname or None == novelname else novelname.split('全集')[0]
			'''
			novelurl 	= 	content.xpath('span[2]/a/@href').extract_first()
			novelid 	= 	novelurl.split('/')[-2].split('b')[-1]
			author      =   content.xpath('span[3]/text()').extract_first()
			novelstatus	=	content.xpath('span[5]/text()').extract_first()
			item['novelname']=novelname
			item['author']=author
			item['novelid']=novelid
			item['novelurl']=novelurl
			item['novelstatus']=novelstatus
			
			#print(novelname,novelurl,novelstatus,novelid,author)
			download_page= self.downloadpage_url_base % (novelid)
			yield Request(download_page,self.parse_details,meta={'item':item},dont_filter=True)

	def parse_details(self,response):
		item = response.meta['item']
	
		imgurl = response.xpath('//*[@class="book-img"]/img/@src').extract_first()
		if imgurl == None:
			imgurl = 'None'
		downloadNum     =      	'None'
		novelsize     	=      	response.xpath('//*[@class="downmenu"]/a[1]/text()').extract_first()
		print(novelsize)
		novelsize 		=		re.findall('\((.*?)\)', novelsize)[0] if 'TXT全集' in novelsize else '0'

		if 'KB' in novelsize:
			novelsize	= 		float(re.split(' KB',novelsize)[0])*1024
		elif 'MB' in novelsize:
			novelsize	= 		float(re.split(' MB',novelsize)[0])*1024*1024
		else:
			novelsize	= 		novelsize

		#print(novelsize)

		simplyintroduce = 		response.xpath('//*[@class="book-info"]/p[contains(@class,"book-intro")]').xpath('string(.)').extract_first()
		simplyintroduce = 		simplyintroduce.strip() 
		try:
			if len(simplyintroduce) < 2:
				simplyintroduce = 		response.xpath('//*[@class="book-info"]/p[3]').xpath('string(.)').extract_first()
				simplyintroduce = 		simplyintroduce.strip() 
		except:
			try:
				simplyintroduce = 		response.xpath('//*[@class="book-info"]/dd/').xpath('string(.)').extract_first()
				simplyintroduce =		simplyintroduce.strip() 
			except:
				simplyintroduce = 'None'
		#print(item['novelname'],novelsize,imgurl,simplyintroduce)
		
		txtdownload		=		self.txt_base_url % (item['novelname'])
		zipdownload		=		self.zip_base_url % (item['novelname'])

		# print(xswitem['novelname'],xswitem['author'],downloadNum,novelsize ,novelstatus)
		# print(xswitem['novelid'],xswitem['imgurl'],xswitem['noveltype'],xswitem['novelurl'])
		# print(txtdownload,zipdownload)
		# print(simplyintroduce)

			


		item['downloadNum']=downloadNum
		item['imgurl']=imgurl

		item['novelsize']=novelsize
		item['txtdownload']=txtdownload
		item['zipdownload']=zipdownload
		item['simplyintroduce']=simplyintroduce
		


		#print(item)
		if novelsize > 20:
			#print(item)
			yield item
		