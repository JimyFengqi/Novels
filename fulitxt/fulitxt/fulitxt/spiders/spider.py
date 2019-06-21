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
from fulitxt.items import FulitxtItem

class Myspider(scrapy.Spider):
	name = "fulitxt"
	allowed_domains = ["fltxt.com"]
	main_url = "http://www.fltxt.com"
	shuku_url_first_base='http://www.fltxt.com/%s/index.html'
	shuku_url_base='http://www.fltxt.com/%s/index_%s.html'

	downloadpage_url_base='https://www.xuanshu.com/txtxz/%s/down.html'
	txt_base_url='https://txt.xuanshu.com/%s/%s.txt'
	zip_base_url='https://zip.xuanshu.com/%s/%s.zip'


	listtype={'xuanhuan':'玄幻魔法','chuanyue':'穿越重生','wuxia':'武侠修真','jsli':'军事历史','youxi':'网游竞技',
	'dushi':'都市言情','xiaoyuan':'热血校园', 	'kongbu':'恐怖灵异','kehuan':'科幻未来','xuanyi':'悬疑推理'
	}

	def start_requests(self):
		for key,value in self.listtype.items():
			url=self.shuku_url_first_base % key
			yield Request(url,self.parse,meta={'noveltype':value,'novelkey':key})

	def parse(self, response):
		noveltype = response.meta['noveltype']
		novelkey = response.meta['novelkey']


		max_page=response.xpath('//*[@class="tspage"]/a[last()]/@href').extract_first()
		max_page= '1' if None == max_page else	max_page.split('/')[-1].split('.')[0].split('_')[1]
		#print(noveltype,max_page)
		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,2):
			if page_num == 1:
				new_url = 	self.shuku_url_first_base % novelkey
			else:						
				new_url =   self.shuku_url_base  % (novelkey,page_num)

			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,meta={'noveltype':noveltype},dont_filter=True)

	def get_novel(self,response):
		noveltype=response.meta['noveltype']
		novel_contents=response.xpath('//*[@class="listBox"]/ul/li')
		#print(' 当前页面 [%s], 每一页有%d 个小说' %  (response.url,len(novel_contents)))

		for content in novel_contents:
			item					=	FulitxtItem()
			item['noveltype'] 	=	noveltype
			novelname   			=   content.xpath('a/text()').extract_first()
			novelurl 	= 	self.main_url  +	content.xpath('a/@href').extract_first()
			novelid 	= 	novelurl.split('.html')[0].split('/')[-1]
			imgurl 		=	self.main_url + content.xpath('a/img/@src').extract_first()

			item['novelname']=novelname
			item['novelid']=novelid
			item['novelurl']=novelurl
			item['imgurl']=imgurl
			#print(novelname,novelurl,imgurl,author)
			yield Request(novelurl,self.parse_details,meta={'item':item},dont_filter=False)
			
	def parse_details(self,response):
		item = response.meta['item']

		contents 		= 		response.xpath('//*[@class="detail_right"]/ul/li/text()').extract()

		downloadNum     =      	contents[1].split('：')[1]
		novelsize     	=      	contents[2].split('：')[1]
		if 'KB' in novelsize:
			novelsize	= 		float(re.split('KB',novelsize)[0])*1024
		elif 'MB' in novelsize:
			novelsize	= 		float(re.split('MB',novelsize)[0])*1024*1024
		else:
			novelsize	= 		novelsize


		novelstatus 	= 		contents[5].split('：')[1]
		author 			=		response.xpath('//*[@class="detail_right"]/ul/li[7]/a/text()').extract_first()
		simplyintroduce = 		response.xpath('//*[@class="showInfo"]').xpath('string(.)').extract()
		simplyintroduce = simplyintroduce[0].strip()

		txtdownload		=		response.xpath('//*[@class="showDown"]/ul/li[1]/a/@href').extract_first()
		zipdownload		=		'None'

		item['author']=author
		item['downloadNum']=downloadNum
		item['novelstatus']=novelstatus
		item['novelsize']=novelsize
		item['txtdownload']=txtdownload
		item['zipdownload']=zipdownload
		item['simplyintroduce']=simplyintroduce
		
		yield(item)


	