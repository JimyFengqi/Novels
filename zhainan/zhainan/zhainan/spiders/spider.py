#coding:utf-8
import scrapy
import re
from scrapy.http import Request
from zhainan.items import ZhainanItem

class Myspider(scrapy.Spider):
	name = "zhainan"
	allowed_domains = ["zntxt.com"]

	typelist=['/shuku/','/new/','/xuanhuan/','/xiuzhen/','/dushi/','/yanqing/','/lishi/','/kehuan/','/wangyou/','/mingzhu/']
	typelist2=['/new/','/xuanhuan/','/xiuzhen/','/dushi/','/yanqing/','/lishi/','/kehuan/','/wangyou/','/mingzhu/']

	main_url = "http://www.zntxt.com"
	shuku_url_base='http://www.zntxt.com/shuku/index_%s.html'

	txt_base_url='http://xiazai.xqishu.com/txt/%s.txt'
	zip_base_url='http://xiazai.xqishu.com/rar/%s.rar'



	def start_requests(self):
		for ntype in self.typelist:
			starturl=self.main_url + ntype
			yield Request(starturl,meta={'ntype':ntype})
	def parse(self, response):
		ntype = response.meta['ntype']
		max_page=response.xpath('//*[@id="splitpage"]/ul/li[last()]/a/@href').extract_first()
		max_page = max_page.split('_')[-1].split('.')[0]
		print(max_page)
		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,3):
			if page_num == 1:
				new_url = self.main_url + ntype
			else:
				new_url=self.shuku_url_base % str(page_num)
			print(new_url)
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,dont_filter=True)
	def get_novel(self,response):
		novel_contents=response.xpath('//*[@class="slist"]')
		print('每一页有%d 个小说' %  len(novel_contents))
		for content in novel_contents:
			item 		=	ZhainanItem()
			imgurl 		=	content.xpath('div[1]/a/img/@src').extract_first()
			novelname	=	content.xpath('div[1]/a/img/@alt').extract_first()
			if novelname:
				novelname	=	novelname.split('《')[1].split('》')[0]

			novelurl 	=	self.main_url + content.xpath('div[1]/a/@href').extract_first()
			novelid		=	novelurl.split('/')[-1].split('.')[0]
			downloadNum	=	content.xpath('div[2]/h4/span/b/text()').extract_first()
			downloadNum = 	re.findall('\d+',downloadNum)[0]

			noveltype	=	content.xpath('div[2]/p[1]/b/a[1]/text()').extract_first()
			author		=	content.xpath('div[2]/p[1]/b/a[2]/text()').extract_first()

			novelinfo 	=	content.xpath('div[2]/p[3]/text()').extract_first()
			novelinfo	=	re.split('：|\|',novelinfo)
			novelsize	=	novelinfo[-1]
			if 'KB' in novelsize:
				novelsize= float(re.split('KB',novelsize)[0])*1024
			elif 'MB' in novelsize:
				novelsize= float(re.split('MB',novelsize)[0])*1024*1024
			else:
				novelsize= novelsize

			novelstatus = novelinfo[2]

			simplyintroduce=content.xpath('div[2]/p[2]/text()').extract_first()
			simplyintroduce = simplyintroduce.strip().replace('文案',"")


			txtdownload	=	self.txt_base_url % (novelname)
			zipdownload	=	self.zip_base_url % (novelname)
	


			item['novelname']		=	novelname
			item['author']			=	author
			item['novelstatus']		=	novelstatus
			item['downloadNum']		=	downloadNum
			item['novelurl']		=	novelurl
			item['novelid']			=	novelid
			item['novelsize']		=	novelsize
			item['noveltype']		=	noveltype
			item['imgurl']			=	imgurl
			item['txtdownload']		=	txtdownload
			item['zipdownload']		=	zipdownload
			item['simplyintroduce']	=	simplyintroduce
			

			if novelsize > 10:
				yield item
			