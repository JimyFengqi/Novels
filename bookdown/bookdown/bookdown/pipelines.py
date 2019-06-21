# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo,sqlite3
from bookdown import settings
class BookdownPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object): 
    def __init__(self,mongo_url,mongo_db): 
        self.mongo_url = mongo_url 
        self.mongo_db = mongo_db 
    @classmethod 
    def from_crawler(cls,crawler): 
        return cls( 
            mongo_url = crawler.settings.get('MONGO_URL'), 
            mongo_db = crawler.settings.get('MONGO_DB') 
        ) 
    def open_spider(self,spider): 
        self.client = pymongo.MongoClient(self.mongo_url) 
        self.db = self.client[self.mongo_db] 
    def process_item(self,item,spider): 
        #name = item.__class__.__name__
        tablename=item['noveltype']
        self.db[tablename].insert(dict(item)) 
        return item 
    def close_spider(self,spider): 
        self.client.close() 

class Sqlite3Pipeline(object):#创建一个新的类，用来做保存数据到数据库的工作
    def __init__(self,dbname,tablename):
        #初始化数据库名称，sqlite数据库是一个文件，dbname写成文件名就行，如果在当前目录下，就只写文件名，如果不在，请写上绝对路径
        self.dbname = dbname
        self.tablename= tablename

    @classmethod#是一个类方法，用@classmethod标识
    def from_crawler(cls,crawler):#他的参数crawler，我们就可以拿到scrapy的所有核心组件，如全局配置的每个信息，然后创建一个pipeline实例，参数cls就是class
        return cls(
            dbname=crawler.settings.get('SQLITE_DBNAME'),
            tablename = crawler.settings.get('SQLITE_TABLE')
            )
        #最后返回一个class实例，在settings.py中加入：DBNAME = "你的数据库的名称，如果在当前目录下，就只写文件名，如果不在，请写上绝对路径"

    def open_spider(self,spider):#该方法在spider被打开的时候开启，我们可以在这里做一些初始化工作
        self.conn = sqlite3.connect(self.dbname)#如连接数据库
        self.cx = self.conn.cursor()#创建游标

    def process_item(self,item,spider):#该方法才是实际用来存储数据的
        data = dict(item)#将item变成字典形式
        keys = ','.join(data.keys())#将字典的键值做成“，”隔开的字符串
        values = ','.join(['%s'] * len(data))#根据data字典的长度建立对应长度数的“%s”
        sql = 'insert or ignore into %s(%s) values %s' %(self.tablename,keys,tuple(data.values()))
        #print(sql)
        self.cx.execute(sql)#执行sql语句
        self.conn.commit()#提交
        return item#返回item

    def close_spider(self,spider):#该方法在spider被关闭的时候打开，我们可以在这里做一些收尾工作，
        self.conn.close()#例如：关闭数据库