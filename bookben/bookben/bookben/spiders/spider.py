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
from bookben.items import BookbenItem

class Myspider(scrapy.Spider):
	name = "bookben"
	allowed_domains = ["bookben.net"]
	listtype={'xuanhuan':'玄幻魔法','xiuzhen':'武侠修真','dushi':'现代都市',
	'chuanyue':'穿越小说','wangyou':'网游小说','kehuan':'科幻小说','qita':'其他小说'
	}
	listtypetest={'xuanhuan':'玄幻魔法'}
	main_url = "https://www.bookben.net"
	shuku_url_base='https://www.bookben.net/%s/%s.html'

	downloadpage_url_base='https://www.bookben.net/down/all/%s.txt'



	txt_base_url='http://down.27xs.cc/txt/%s.txt'
	zip_base_url='http://down.27xs.cc/zip/%s.zip'

	def start_requests(self):
		
		for key,value in self.listtype.items():
		#for key,value in self.listtypetest.items():
			url=self.shuku_url_base % (key,'1')
			yield Request(url,self.parse,meta={'noveltype':value,'novelkey':key})
	def parse(self, response):
		noveltype=response.meta['noveltype']
		novelkey=response.meta['novelkey']

		print(noveltype)
		max_page=response.xpath('//*[@class="page"]/ul/li[last()]/a/@href').extract_first()
		max_page= max_page.split('/')[-1].split('.')[0]
		print(noveltype,max_page)

		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,2):
						
			new_url= self.shuku_url_base % (novelkey,str(page_num))
			#print('new_url  = %s' % new_url)
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,meta={'noveltype':noveltype},dont_filter=True)

	def get_novel(self,response):
		noveltype=response.meta['noveltype']
		novel_contents=response.xpath('//*[@class="lblr"]/dl')
		#print(' 当前页面类型[%s]地址 [%s], 每一页有%d 个小说' %  (noveltype,response.url,len(novel_contents)))

		
		for content in novel_contents:
			item=BookbenItem()
			item['noveltype']=	noveltype	
			novelname   =   content.xpath('dd[1]/a/@title').extract_first()
			novelurl  	=   self.main_url+content.xpath('dd[1]/a/@href').extract_first()
			imgurl  	=   content.xpath('dd[1]/a/img/@src').extract_first()
			imgurl		=   imgurl if 'https'  in imgurl else 'https://www.bookben.net'+imgurl

			author  	=   content.xpath('dd[3]/text()').extract_first()
			author 		=	author.split('：')[-1]
			
			novelid 	= 	novelurl.split('/')[-1].split('.')[0]

			item['novelname']=novelname
			item['author']=author
			item['novelid']=novelid
			item['novelurl']=novelurl
			item['imgurl']=imgurl
			
			#print(novelname,novelurl,imgurl,novelid,author)

			yield Request(novelurl,self.parse_details,meta={'item':item},dont_filter=True)
		
	def parse_details(self,response):
		item = response.meta['item']
	
		novelstatus 	= 	response.xpath('//*[@class="yxjj"]/dd[3]/text()').extract_first()
		novelstatus		= 	novelstatus if '完结' not in novelstatus else '完结'
		downloadNum     =   'None'

		novelsize     	=   response.xpath('//*[@class="yxjj"]/dd[4]/text()').extract_first()
		novelsize =  float(int(novelsize.split('万')[0])*10000/2) if '万'  in novelsize else novelsize
		#print(novelsize)
		
		

		simplyintroduce = 		response.xpath('//*[@class="nylr"]/dl/dd/p/text()').extract_first()
		simplyintroduce = 		simplyintroduce.strip()[2:] 

		#print(item['novelname'],novelsize,imgurl,simplyintroduce)
		
		txtdownload		=		self.txt_base_url % (item['novelid'])
		zipdownload		=		'None'


		item['downloadNum']=downloadNum
		item['novelstatus']=novelstatus
		item['novelsize']=novelsize
		item['txtdownload']=txtdownload
		item['zipdownload']=zipdownload
		item['simplyintroduce']=simplyintroduce


		if novelsize > 20:
			#print(item)
			yield item		
		