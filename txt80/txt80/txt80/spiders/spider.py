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
from txt80.items import Txt80Item

class Myspider(scrapy.Spider):
	name = "txt80"
	allowed_domains = ["80txt.com"]
	main_url = "https://www.80txt.com/"
	shuku_url_base='https://www.80txt.com/sort/%s.html'

	downloadpage_url_base='https://www.80txt.com/txtxz/%s/down.html'
	txt_base_url='https://txt.80txt.com/%s/%s.txt'
	zip_base_url='https://zip.80txt.com/%s/%s.zip'

	def start_requests(self):
		for i in range(1,26):
			url=self.main_url+'sort'+str(i)+'/1.html'
			yield Request(url,self.parse)
	def parse(self, response):
		noveltype = response.xpath('//*[@class="path"]/a[2]/text()').extract_first()
		max_page=response.xpath('//*[@class="last"]/text()').extract_first()
		#print(noveltype,max_page)

		new_base_url=response.url.split('html')[0][:-2]
		#print(response.url,new_base_url)
		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,3):
			new_url=new_base_url+str(page_num)+'.html'
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,meta={'noveltype':noveltype},dont_filter=True)
	def get_novel(self,response):
		noveltype=response.meta['noveltype']
		novel_contents=response.xpath('//*[@id="list_art_2013"]')
		print('当前页面[%s]  每一页有%d 个小说' %  (response.url,len(novel_contents)))

		
		item=Txt80Item()
		for content in novel_contents:
			novelname   =   content.xpath('div[2]/a/img/@title').extract_first()
			novelurl 	=	content.xpath('div[2]/a/@href').extract_first()
			novelid 	=	novelurl.split('/')[-1].split('.')[0]
			
			novelstatus =	content.xpath('div[1]/div[1]/div[2]/span[1]/text()').extract_first()
			
			author 		=	content.xpath('div[1]/div[3]/span/a/text()').extract_first()

			novelsize_downloadNum	=	content.xpath('div[1]/div[3]/span/text()').extract()
			#downloadNum	=	content.xpath('div[1]/div[3]/span/text()[4]').extract_first()
			#novelsize	=	content.xpath('div[1]/div[3]/span/text()[3]').extract_first()
			downloadNum = novelsize_downloadNum[-1].strip().split(' ')[0]
			novelsize = novelsize_downloadNum[2].strip()
			
			if 'KB' in novelsize:
				novelsize= float(re.split('KB',novelsize)[0])*1024
			elif 'MB':
				novelsize= float(re.split('MB',novelsize)[0])*1024*1024
			else:
				novelsize= float(re.split('MB',novelsize)[0])
	
			
			txtdownload	=	self.txt_base_url % (novelid,novelname)
			zipdownload	=	self.zip_base_url % (novelid,novelname)

			imgurl 		= 	content.xpath('div[2]/a/img/@src').extract_first() #图片url
			#imgurl2    =	content.xpath('div[@class="book_pic"]/a/img/@src').extract_first()#图片URL
			simplyintroduce = content.xpath('div[1]/div[2]/text()').extract_first() #书籍简介

			simplyintroduce= simplyintroduce.strip()

			item['novelname']=novelname
			item['author']=author
			item['downloadNum']=downloadNum
			item['novelstatus']=novelstatus
			item['novelurl']=novelurl
			item['imgurl']=imgurl
			item['novelid']=novelid
			item['novelsize']=novelsize
			item['noveltype']=noveltype
			item['txtdownload']=txtdownload
			item['zipdownload']=zipdownload
			item['simplyintroduce']=simplyintroduce
			
			print(novelname,author,novelid,novelsize,downloadNum,novelurl,noveltype)
			print(imgurl,txtdownload,zipdownload)
			#print(item)
			if novelsize > 20:
				yield item
			