#coding:utf-8
import scrapy
import re
from scrapy.http import Request
from mianhuatang.items import MianhuatangItem

class Myspider(scrapy.Spider):
	name = "mianhuatang"
	allowed_domains = ["mianhuatang2.com"]

	main_url = "https://www.mianhuatang2.com/"

	shuku_url_base='https://www.mianhuatang2.com/qb/%s.htm'
	txt_base_url='https://www.mianhuatang2.com/download.aspx?'

	def start_requests(self):
		yield Request('https://www.mianhuatang2.com/qb/1.htm')
	def parse(self, response):
		max_page=response.xpath('//*[@class="pagerdiv"]/ul/li[last()]/a/@href').extract_first()
		max_page = max_page.split('/')[-1].split('.')[0]
		print(max_page)
		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,5):
			new_url=self.shuku_url_base % str(page_num)
			print(new_url)
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,dont_filter=True)
	def get_novel(self,response):
		novel_contents=response.xpath('//*[@class="l"]/ul/li')
		print('每一页有%d 个小说' %  len(novel_contents))
		for content in novel_contents:
			item 		=	MianhuatangItem()
			noveltype	=	content.xpath('span[1]/text()').extract_first()
			noveltype   = 	re.sub('\[|\]','',noveltype)

			novelname	=	content.xpath('span[2]/a/text()').extract_first()
			novelurl 	=	content.xpath('span[2]/a/@href').extract_first()
			novelid		=	novelurl.split('/')[-2]
			author		=	content.xpath('span[4]/text()').extract_first()

			item['novelname']		=	novelname
			item['author']			=	author
			item['noveltype']		=	noveltype
			item['novelurl']		=	novelurl
			item['novelid']			=	novelid

			yield Request(novelurl,self.parse_details,meta={'item':item},dont_filter=False)

	def parse_details(self,response):
		item = response.meta['item']
		imgurl	=	response.xpath('//*[@id="fmimg"]/img/@src').extract_first()
		imgurl	= imgurl if 'https' in imgurl else "https"+imgurl


		simplyintroduce	=	response.xpath('//*[@id="intro"]/p[1]/text()').extract_first()
		simplyintroduce = 	simplyintroduce.strip().replace('[收起]',"")

		txtdownload	=	response.xpath('//*[@id="info"]/div[2]/script/text()').extract_first()
		txtdownload = 	re.split('\'|\n',txtdownload)
		txtdownload =	self.txt_base_url+txtdownload[5]+txtdownload[8]

		novelstatus = 	'None'
		downloadNum = 	'None'
		novelsize	=	'None'
		zipdownload	=	'None'

		item['novelstatus']		=	novelstatus
		item['downloadNum']		=	downloadNum
		item['novelsize']		=	novelsize
		item['imgurl']			=	imgurl
		item['txtdownload']		=	txtdownload
		item['zipdownload']		=	zipdownload
		item['simplyintroduce']	=	simplyintroduce
		
		yield(item)