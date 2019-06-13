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
from zhuajishuwu.items import ZhuajishuwuItem

class Myspider(scrapy.Spider):
	name = "zhuajishuwu"
	allowed_domains = ["zhuaji.org"]
	main_url = "https://www.zhuaji.org/"
	shuku_url_base='https://www.zhuaji.org/shuku/lastupdate_%s_0_2_0_0_%s.html'

	downloadpage_url_base='https://www.zhuaji.org/txtxz/%s.html'

	txt_base_url='https://txt.xuanshu.com/%s/%s.txt'
	zip_base_url='https://zip.xuanshu.com/%s/%s.zip'

	def start_requests(self):
		#for i in range(1,3):
		for i in range(1,11):
			url=self.shuku_url_base % (str(i),'1')
			yield Request(url,self.parse,meta={'noveltypeid':str(i),'novellengthid':'0'})
	def parse(self, response):
		noveltypeid = response.meta['noveltypeid']
		novellengthid = response.meta['novellengthid']
		noveltype = response.xpath('//*[@class="tdr"]/a[contains(@class,"cur")]/strong/text()').extract_first()#//a[@class = 'cur']
		#noveltype2 = response.xpath('//*[@class="tdr"]/a[@class = "cur"]/strong/text()').extract_first()#多个标签中选择特定的一个
		max_page=response.xpath('//*[@class="pagelink"]/a[last()]/@href').extract_first()   #选择标签中最后一个
		max_page= max_page.split('/')[-1].split('.')[0].split('_')[-1]
		#print( '小说类型=%s ,当前字数种类=%s, 当前种类最大页面=%s,'  % (noveltype,novellengthid,max_page))

		
		if int(max_page)  > 9:
			for i in range (1,6):
				url = self.main_url+'shuku/lastupdate_'+noveltypeid+'_'+str(i)+'_2_0_0_1.html'
				#print ('yield [%s]type again , 第%d 种'  % (noveltype,i))
				yield Request(url,self.parse,meta={'noveltypeid':noveltypeid,'novellengthid':str(i)},dont_filter=True)
		else: 
			for page_num in range(1,int(max_page)+1):
			#for page_num in range(1,2):
								
				new_url=self.main_url+'shuku/lastupdate_'+noveltypeid+'_'+novellengthid+'_2_0_0_'+str(page_num)+'.html'
				#print('new_url  = %s' % new_url)
				#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
				yield Request(new_url,self.get_novel,meta={'noveltype':noveltype},dont_filter=True)
		
	def get_novel(self,response):
		noveltype=response.meta['noveltype']
		novel_contents=response.xpath('//*[@class="book_list lazyload_box"]/ul/li')
		#print(' 当前页面 [%s], 每一页有%d 个小说' %  (response.url,len(novel_contents)))

		for content in novel_contents:
			zhuajiItem=ZhuajishuwuItem()
			zhuajiItem['noveltype']=response.meta['noveltype']
			novelname   =   content.xpath('dl/dd[1]/a/text()').extract_first()

			novelurl 	= 	content.xpath('div/a/@href').extract_first()
			novelid 	= 	novelurl.split('/')[-1]
			imgurl 		=	content.xpath('div/a/img/@src').extract_first()
			author      =   content.xpath('dl/dd[2]/span/text()').extract_first()
			zhuajiItem['novelname']=novelname
			zhuajiItem['author']=author
			zhuajiItem['novelid']=novelid
			zhuajiItem['novelurl']=novelurl
			zhuajiItem['imgurl']=imgurl
			download_page= self.downloadpage_url_base % novelid
			#print(novelname,novelurl,imgurl,author)

			yield Request(download_page,self.parse_details,meta={'zhuajiItem':zhuajiItem},dont_filter=True)

	def parse_details(self,response):
		zhuajiItem = response.meta['zhuajiItem']
		#print(zhuajiItem)
		contents 		= 		response.xpath('//*[@class="show_num"]/ul/li/text()').extract()

		downloadNum     =      	contents[6].split('：')[1]
		novelsize     	=      	contents[2].split('：')[1]
		if 'KB' in novelsize:
			novelsize	= 		float(re.split('KB',novelsize)[0])*1024
		elif 'M':
			novelsize	= 		float(re.split('M',novelsize)[0])*1024*1024
		else:
			novelsize	= 		float(re.split('M',novelsize)[0])


		novelstatus 	= 		'完结'

		simplyintroduce = 		response.xpath('//*[@class="txt_description"]/p[1]/text()').extract_first()
		simplyintroduce = 		simplyintroduce.strip()

		txtdownload		=		'NULL'
		zipdownload		=		'NULL'

		# print(zhuajiItem['novelname'],zhuajiItem['author'],downloadNum,novelsize ,novelstatus)
		# print(zhuajiItem['novelid'],zhuajiItem['imgurl'],zhuajiItem['noveltype'],zhuajiItem['novelurl'])
		# print(txtdownload,zipdownload)
		# print(simplyintroduce)

			


		zhuajiItem['downloadNum']=downloadNum
		zhuajiItem['novelstatus']=novelstatus
		zhuajiItem['novelsize']=novelsize
		zhuajiItem['txtdownload']=txtdownload
		zhuajiItem['zipdownload']=zipdownload
		zhuajiItem['simplyintroduce']=simplyintroduce
		


		#print(zhuajiItem)
		if novelsize > 20:
			yield zhuajiItem
		