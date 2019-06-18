

#coding:utf-8
import scrapy
import re
from scrapy.http import Request
from qishuwang.items import QishuwangItem

class Myspider(scrapy.Spider):
	name = "qishuwang"
	allowed_domains = ["qishu.cc"]
	listtype=["http://www.qishu.cc/xuanhuan/list1_1.html",
	"http://www.qishu.cc/yanqing/list2_1.html",
	"http://www.qishu.cc/wuxia/list3_1.html",
	"http://www.qishu.cc/danmei/list4_1.html",
	"http://www.qishu.cc/xiaoyuan/list5_1.html",
	"http://www.qishu.cc/kehuan/list6_1.html",
	"http://www.qishu.cc/chuanyeu/list7_1.html",
	"http://www.qishu.cc/wangyou/list8_1.html",
	"http://www.qishu.cc/wangyou/list8_1.html",
	"http://www.qishu.cc/lishi/list9_1.html",
	"http://www.qishu.cc/yanqing/list10_1.html",
	"http://www.qishu.cc/wenxue/list11_1.html"]

	main_url = "http://www.qishu.cc"



	txt_base_url='http://xiazai.xqishu.com/txt/%s.txt'
	zip_base_url="http://xiazai.xqishu.com/rar/%s.rar"

	def start_requests(self):
		for url in self.listtype:
			yield Request(url,self.parse)
	def parse(self, response):
		max_page=response.xpath('//*[@class="mainNextPage"]/var/code/a[last()]/text()').extract_first()
		noveltype = response.xpath('//*[@class="crumb"]/span/a[last()]/text()').extract_first()

		new_url_base=response.url[:-6]
		for page_num in range(1,int(max_page)+1):
		#for page_num in range(1,2):
						
			new_url= new_url_base + str(page_num) +'.html'
			#print('noveltype = %s,max_page=%s, new_url  = %s' % (noveltype,max_page,new_url))
			#dont_filter 如果不加入这个参数， 那么第一页默认已经爬过了，在下一级函数，就不会再次获取其页面内容
			yield Request(new_url,self.get_novel,meta={'noveltype':noveltype},dont_filter=True)

	def get_novel(self,response):
		noveltype=response.meta['noveltype']
		novel_contents=response.xpath('//*[@class="mainListInfo"]')
		print(' 当前页面类型[%s]地址 [%s], 每一页有%d 个小说' %  (noveltype,response.url,len(novel_contents)))

		
		for content in novel_contents:
			item=QishuwangItem()
			item['noveltype']=	noveltype	

			novelname   =   content.xpath('div[1]/span/a/@title').extract_first()
			novelname   = novelname.split(' TXT全集')[0] if "TXT全集" in novelname else novelname
			novelurl  	=   self.main_url+content.xpath('div[1]/span/a/@href').extract_first()
			novelid 	= 	novelurl.split('/')[-1].split('.')[0]
			downloadNum    = content.xpath('div[3]/text()').extract_first()
			txtdownload		=		self.txt_base_url % novelname
			zipdownload		=		self.zip_base_url % novelname
	
			item['novelname']=novelname
	
			item['novelid']=novelid
			item['novelurl']=novelurl
			item['downloadNum']=downloadNum
			item['txtdownload']=txtdownload
			item['zipdownload']=zipdownload
			item['imgurl']= 'None'

			#print(item)
			#print(novelname,novelurl,imgurl,novelid,author)

			yield Request(novelurl,self.parse_details,meta={'item':item},dont_filter=True)
			
	def parse_details(self,response):
		item = response.meta['item']
	
		novelInfo	= 	response.xpath('//*[@class="downInfoRowL"]').xpath('string(.)').extract()
		novelInfo = novelInfo[0].split('\r\n\t\t\t\t\t')

		author = novelInfo[3].split('：')[-1]
		novelsize = novelInfo[4].split('：')[-1]

		if 'KB' in novelsize:
			novelsize	= 		float(re.split(' KB',novelsize)[0])*1024
		elif 'MB' in novelsize:
			novelsize	= 		float(re.split(' MB',novelsize)[0])*1024*1024
		else :
			novelsize	= 	novelsize	
		simplyintroduce = 		response.xpath('//*[@id="mainSoftIntro"]').xpath('string(.)').extract()
		#simplyintroduce = 		simplyintroduce.strip()
		if len(simplyintroduce) == 1:
			if '下载后请在24小时之内删除.' in simplyintroduce[0]:
				simplyintroduce= simplyintroduce[0].split('下载后请在24小时之内删除.')[-1].strip()
			else:
				simplyintroduce=simplyintroduce[0].strip()
		else:
			simplyintroduce = 'None'
	

	
		item['novelstatus']= 'None'
		item['novelsize']=novelsize
		item['author']=author
	
		item['simplyintroduce']=simplyintroduce


		#print(item)
		yield item		
		