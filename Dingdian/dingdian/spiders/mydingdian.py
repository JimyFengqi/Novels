#coding:utf-8
import scrapy
import re
from scrapy.http import Request
from dingdian.items import DingdianItem
#from dingdian.items import DDNovelContentItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Myspider(scrapy.Spider):
	name = "dingdian"
	allowed_domains = ["23us.com"]
	bash_url = "http://www.23us.com/class/"
	bashurl='.html'
	
	def start_requests(self):
		#for i in range(1,11):
		for i in range(7,8):
			url=self.bash_url+str(i)+"_1"+self.bashurl
			yield Request(url,self.parse)
	
	def parse(self, response):
		
		baseurl=response.url  #此处得到的url为http://www.23us.com/class/*_1.html
		print('baseurl: [%s]' % baseurl )
		max_num=response.xpath('//*[@id="pagelink"]/a[14]/text()').extract_first()#获取当前页面的最大页码数
		print (u'max_num是：[%s]' % max_num)
		baseurl=baseurl[:-7]
				
		#for num in xrange(1,int(max_num)+1):
		for num in xrange(1,3):
			newurl=baseurl+"_"+str(num)+self.bashurl
			#此处使用dont_filter和不使用的效果不一样，使用dont_filter就能够抓取到第一个页面的内容，不用就抓不到
			#scrapy会对request的URL去重(RFPDupeFilter)，加上dont_filter则告诉它这个URL不参与去重。
			print('newurl = [%s ] ' % newurl)
			yield Request(newurl,dont_filter=True,callback=self.get_name)#将新的页面url的内容传递给get_name函数去处理
	
	def get_name(self,response):
		for nameinfo in response.xpath('//tr'):
			novel_instroduce = nameinfo.xpath('td[1]/a[1]/@href').extract_first()#小说地址
			chapterlisturl = nameinfo.xpath('td[1]/a[2]/@href').extract_first()#小说地址
			name = nameinfo.xpath('td[1]/a[2]/text()').extract_first()#小说名字
			if  novel_instroduce:
				print(u'[%s],地址为：[%s] ，当前页面是【%s】' % (name,novel_instroduce,response.url))
				yield Request(novel_instroduce,dont_filter=True,callback=self.get_novelcontent,meta={'name':name,'chapterlisturl':chapterlisturl})
			'''
			#在当前页面获取小说详情
			#print nameinfo
			name = nameinfo.xpath('td[1]/a/text()').extract_first()#小说名字
			author= nameinfo.xpath('td[3]/text()').extract_first()#小说作者
			novelurl = nameinfo.xpath('td[1]/a/@href').extract_first()#小说地址
			serialstatus = nameinfo.xpath('td[6]/text()').extract_first()#小说状态
			serialnumber = nameinfo.xpath('td[4]/text()').extract_first()#小说字数
			if  novelurl:
				targentcontent['novel_name']=name
				targentcontent['author']=author
				targentcontent['novelurl']=novelurl
				targentcontent['serialstatus']=serialstatus
				targentcontent['serialnumber']=serialnumber	
				#print name,author,novelurl,serialstatus,serialnumber
			
				yield Request(novelurl,callback=self.get_novelcontent,meta={'targentcontent':targentcontent})
			小说相关的详情可以暂时不传递
			'''
	
	def get_novelcontent(self,response):
		#targentcontent=response.meta['targentcontent']
		#print targentcontent['novelurl'],targentcontent['name']
		#title = response.xpath('//dd[1]/h1/text()').extract_first()
		novel_instroduce_url = response.url#小说地址
		novel_name=response.meta['name']#小说名字
		chapterlisturl=response.meta['chapterlisturl']#章节列表地址
		author = response.xpath('//table/tr[1]/td[2]/text()').extract_first()#作者
		serialstatus = response.xpath('//table/tr[1]/td[3]/text()').extract_first()#状态
		serialnumber = response.xpath('//table/tr[2]/td[2]/text()').extract_first()#连载字数
		category = response.xpath('//table/tr[1]/td[1]/a/text()').extract_first()#小说类别
		name_id = chapterlisturl.split('/')[-1]#小说编号
		collect_num_total=response.xpath('//table/tr[2]/td[1]/text()').extract_first()#总收藏
		click_num_total=response.xpath('//table/tr[3]/td[1]/text()').extract_first()#总点击
		
		#chapterlistul=response.xpath('//dd[2]/div[2]/p[2]/a/text()').extract_first()
		#chapterlisturl=response.xpath('//dd[2]/div[2]/p[2]/a/@href').extract_first()
		novel_breif=response.xpath('//dd[2]/p[2]').extract_first()
		'''
		print('novel_instroduce_url = %s' % novel_instroduce_url)
		print('chapterlisturl = %s' % chapterlisturl)
		print('author = %s' % len(author))
		print('serialstatus = %s' % len(serialstatus))
		print('serialnumber = %s' % len(serialnumber))
		print('category = %s' % len(category))
		print('name_id = %s' % name_id)
		print('collect_num_total = %s' % int(collect_num_total))
		print('click_num_total = %s' % int(click_num_total))
		'''


		targentcontent=DingdianItem()
		targentcontent['novel_name']=novel_name
		targentcontent['author']=author
		targentcontent['novel_instroduce_url']=novel_instroduce_url
		targentcontent['novelurl']=chapterlisturl
		targentcontent['serialstatus']=serialstatus
		targentcontent['serialnumber']=serialnumber	
		targentcontent['category']=category	
		targentcontent['name_id']=name_id	
		targentcontent['collect_num_total']=collect_num_total	
		targentcontent['click_num_total']=click_num_total	
		targentcontent['novel_breif']=novel_breif	
		#print(u'novel_name=%s,author=%s,novel_instroduce=%s,serialstatus=%s,serialnumber=%s,category=%s,name_id=%s,collect_num_total=%s,click_num_total=%s,chapterlisturl=%s'  % (novel_name,author,novel_instroduce,serialstatus,serialnumber,category,name_id,collect_num_total,click_num_total,chapterlisturl))
		#yield targentcontent
		yield Request(chapterlisturl,dont_filter=True,callback=self.get_charaterurl,meta={'targentcontent':targentcontent})
		
		
		
		
		
		
	def get_charaterurl(self,response):
		#print response.url
		item=response.meta['targentcontent']
		for contents in response.xpath('//table/tr'):
			for content in contents.xpath('td'):
				if  content.xpath('a/text()').extract_first():
					#print content.xpath('a/text()').extract_first()
					item['chapterurl']=response.url+content.xpath('a/@href').extract_first()
					item['chaptername']=content.xpath('a/text()').extract_first()
					yield item
		
		
		
		
