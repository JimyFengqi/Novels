#coding:utf-8
import scrapy
import re
from scrapy.http import Request
from liangjiu.items import LiangjiuItem

class Myspider(scrapy.Spider):
	name = "liangjiu"
	allowed_domains = ["txt909.com"]

	main_url = "https://www.txt909.com"
	shuku_url_base='http://www.zntxt.com/shuku/index_%s.html'

	txt_base_url='https://www.txt909.com/all/%s'
	zip_base_url='http://xiazai.xqishu.com/rar/%s.rar'



	def start_requests(self):
		yield Request(self.main_url)
	def parse(self, response):
		typecontent= response.xpath('//*[@class="subnav"]/ul/li')
		for info in typecontent:
			new_url   = self.main_url+info.xpath('a/@href').extract_first()
		
			yield Request(new_url,self.get_pagenum)

	def get_pagenum(self,response):	

		max_page=response.xpath('//*[@class="pager"]/ul/li[last()]/a/@href').extract_first()
		max_page = '1' if None == max_page else max_page.split('/')[-1].split('.')[0].split('-')[0]

		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,2):
			new_url=  response.url[:-6] + str(page_num) + '.html'
			print(new_url)
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,dont_filter=True)
	def get_novel(self,response):

		novel_contents=response.xpath('//*[@class="listbg"]')
		print('每一页有%d 个小说' %  len(novel_contents))
		for content in novel_contents:
			item = LiangjiuItem()

			novelname	=	content.xpath('a/@title').extract_first()
			novelurl 	=	self.main_url + content.xpath('a/@href').extract_first()
			novelid		=	novelurl.split('/')[-1].split('.')[0]

			item['novelname']		=	novelname
			item['novelid']			=	novelid
			item['novelurl']		=	novelurl
			item['txtdownload']		=	self.txt_base_url % novelid
			yield Request(novelurl,self.get_details,dont_filter=True,meta={'item':item})
	def get_details(self,response):
			item = response.meta['item']
			novelinfo = response.xpath('//*[@class="downInfoRowL"]')
			imgurl = novelinfo.xpath('span/img/@src').extract_first()

			author 	= novelinfo.xpath('li[1]/a/text()').extract_first()
			noveltype = novelinfo.xpath('li[2]/a/text()').extract_first()
			novelsize = novelinfo.xpath('li[3]/text()').extract_first()
			if 'KB' in novelsize:
				novelsize= float(re.split('KB',novelsize)[0])*1024
			elif 'MB' in novelsize:
				novelsize= float(re.split('MB',novelsize)[0])*1024*1024
			else:
				novelsize= float(novelsize)

			novelstatus = novelinfo.xpath('li[7]/text()').extract_first()

			simplyintroduce=  response.xpath('//*[@id="mainSoftIntro"]').xpath('string(.)').extract_first()
			simplyintroduce = simplyintroduce.strip()
			downloadNum     = response.xpath('//*[@class="downAddress_li"]/a/span[2]/em/text()').extract_first()

			item['author']			=	author
			item['novelstatus']		=	novelstatus
			item['downloadNum']		=	downloadNum
			item['noveltype']		=	noveltype
	
			item['novelsize']		=	novelsize

			item['imgurl']			=	imgurl
			item['zipdownload']		=	'None'
			item['simplyintroduce']	=	simplyintroduce
			

			if novelsize > 10:
				yield(item)
		