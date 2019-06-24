# -*- coding: utf-8 -*-
# @Date     : 2019-06-24 17:18:10
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6

# -*- coding: utf-8 -*-  
from scrapy import cmdline  
import sqlite3,os  

class DbManager(object):
    def __init__(self):
        #self.dbname=os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))+'\\'+"sjtxtdb.sqlite3"
        self.dbname=os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))+'/'+"sjtxtdb.sqlite3"
        print(self.dbname)
        self.db = sqlite3.connect(self.dbname)
        self.cursor = self.db.cursor()
        self.tablename= 'sjtxt_novel'
        self.initDB(self.tablename)
    def initDB(self,tablename):        
        if not os.path.exists(self.dbname) or os.path.getsize(self.dbname) < 10:
            create_novel_tableString = """
            CREATE TABLE IF NOT EXISTS %s(
            id integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
            "novelname" text  unique NOT NULL, 
            "author" text NOT NULL, 
            "novelid" text NOT NULL, 
            "noveltype" text NOT NULL, 
            "novelsize" text NOT NULL, 
            "downloadnum" text NOT NULL, 
            "novelurl" text NOT NULL, 
            "novelstatus" text NOT NULL,
            "imgurl" text NOT NULL,
            "txtdownload" text NOT NULL, 
            "zipdownload" text NOT NULL,
            "simplyintroduce" text NOT NULL
            )""" % tablename
            print(create_novel_tableString)

            self.cursor.execute(create_novel_tableString)
            self.db.commit()  
            print('DB file not exist, create a new.')

a=DbManager()
name = 'sjtxt'  
cmd = 'scrapy crawl {0}'.format(name)  
cmdline.execute(cmd.split())