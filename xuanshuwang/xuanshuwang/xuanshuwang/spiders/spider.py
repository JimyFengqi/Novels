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
from xuanshuwang.items import XuanshuwangItem

class Myspider(scrapy.Spider):
	name = "xuanshuwang"
	allowed_domains = ["xuanshu.com"]
	main_url = "https://www.xuanshu.com/"
	shuku_url_base='https://www.xuanshu.com/sort/%s.html'

	downloadpage_url_base='https://www.xuanshu.com/txtxz/%s/down.html'
	txt_base_url='https://txt.xuanshu.com/%s/%s.txt'
	zip_base_url='https://zip.xuanshu.com/%s/%s.zip'

	def start_requests(self):
		#for i in range(1,2):
		for i in range(1,12):
			url=self.main_url+'soft/sort0'+str(i)+'/'+'index.html'
			yield Request(url,self.parse)
	def parse(self, response):
		noveltype = response.xpath('//*[@class="wrap position"]/span/a[2]/text()').extract_first()
		max_page=response.xpath('//*[@class="tspage"]/a[2]/@href').extract_first()
		max_page= max_page.split('/')[-1].split('.')[0].split('_')[1]
		#print(noveltype,max_page)

		new_base_url=response.url.split('.html')[0]
		#print(response.url,new_base_url)
		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,2):
			if page_num == 1:
				new_url = 	response.url
			else:						
				new_url=new_base_url+'_' +str(page_num)+'.html'
			#print('new_url  = %s' % new_url)
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,meta={'noveltype':noveltype},dont_filter=True)

	def get_novel(self,response):
		noveltype=response.meta['noveltype']
		novel_contents=response.xpath('//*[@class="listBox"]/ul/li')
		#print(' 当前页面 [%s], 每一页有%d 个小说' %  (response.url,len(novel_contents)))

		for content in novel_contents:
			xswitem=XuanshuwangItem()
			xswitem['noveltype']=response.meta['noveltype']
			novelname   =   content.xpath('a/text()').extract_first()
			if None == novelname:
				novelname   =   content.xpath('a/strong/font/text()').extract_first()
			if None == novelname:
				novelname   =   content.xpath('a/font/text()').extract_first()				

			novelname 	=  novelname  if None == novelname else	re.sub('《|》','',novelname.strip())
			novelname = novelname if '全集' not in novelname or None == novelname else novelname.split('全集')[0]


			novelurl 	= 	self.main_url  +	content.xpath('a/@href').extract_first()
			novelid 	= 	novelurl.split('.html')[0].split('/')[-1]
			imgurl 		=	self.main_url + content.xpath('a/img/@src').extract_first()
			author      =   content.xpath('div[1]/a[1]/text()').extract_first()
			xswitem['novelname']=novelname
			xswitem['author']=author
			xswitem['novelid']=novelid
			xswitem['novelurl']=novelurl
			xswitem['imgurl']=imgurl
			#print(novelname,novelurl,imgurl,author)

			yield Request(novelurl,self.parse_details,meta={'xswitem':xswitem},dont_filter=True)

	def parse_details(self,response):
		xswitem = response.meta['xswitem']
		#print(xswitem)
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

		simplyintroduce = 		response.xpath('//*[@class="showInfo"]').xpath('string(.)').extract()
		simplyintroduce = simplyintroduce[0].strip()

		txtdownload		=		response.xpath('//*[@class="showDown"]/ul/li[2]/a/@href').extract_first()
		zipdownload		=		response.xpath('//*[@class="showDown"]/ul/li[1]/a/@href').extract_first()

		# print(xswitem['novelname'],xswitem['author'],downloadNum,novelsize ,novelstatus)
		# print(xswitem['novelid'],xswitem['imgurl'],xswitem['noveltype'],xswitem['novelurl'])
		# print(txtdownload,zipdownload)
		# print(simplyintroduce)

			


		xswitem['downloadNum']=downloadNum
		xswitem['novelstatus']=novelstatus
		xswitem['novelsize']=novelsize
		xswitem['txtdownload']=txtdownload
		xswitem['zipdownload']=zipdownload
		xswitem['simplyintroduce']=simplyintroduce
		


		#print(xswitem)
		if novelsize > 20:
			yield xswitem
		