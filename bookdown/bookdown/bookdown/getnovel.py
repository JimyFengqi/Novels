# -*- coding: utf-8 -*-
# @Date     : 2018-11-08 11:29:27
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6
import re
import os
import sys
import pymongo
import requests
import shutil

class PymongoDataSave():
	def __init__(self,data='test'):
		self.s=requests.session()
		self.client=pymongo.MongoClient()
		self.wuxian=self.client.xuanshuxiaoshuo

		self.txthandler=  Handletxt()
		
	def saveDataInDB(self,db,datalist,):
		print(datalist)
		table=self.wuxian[db]
		table.insert_one(datalist)

	def getData(self,db):
		table=self.wuxian[db]
		datalist=table.find()
		#print('类型【%s】 有小说【%d】部' % (db,len(datalist)))
		f_fail=open('E:\\python_study\\炫书\\炫书小说\\'+db+'.txt','w',encoding='utf-8')
		i=1
		for item in datalist:
			novelname=item['novelname']
			author=item['author']
			downloadNum=item['downloadNum']
			noveltype=item['noveltype']
			novelurl=item['novelurl']
			novelid=item['novelid']
			novelsize=item['novelsize']
			txtdownload=item['txtdownload']
			zipdownload=item['zipdownload']

			info='i=[%d],novelname=%s,author=%s,novelid=%s,noveltype=%s,novelsize=%s,downloadNum=%s,novelurl=%s' % (i,novelname,author,novelid,noveltype,novelsize,downloadNum,novelurl)
			print(info)
			i=i+1
			novelpath='E:\\python_study\\炫书\\炫书小说'+'/'+noveltype
			handlenovelpath='E:\\python_study\\炫书\\炫书小说原始'+'/'+noveltype
			failconvertpath='E:\\python_study\\炫书\\炫书小说原始not'+'/'+noveltype
			if not os.path.exists(novelpath):
				os.makedirs(novelpath)
			if not os.path.exists(handlenovelpath):
				os.makedirs(handlenovelpath)
			if not os.path.exists(failconvertpath):
				os.makedirs(failconvertpath)

			txtpath=novelpath+'/'+novelname+'.txt'
			handletxtpath=handlenovelpath+'/'+novelname+'.txt'
			failconvertxtpath=failconvertpath+'/'+novelname+'.txt'

			fileflag=True
			#if os.path.exists(handletxtpath):
				#continue
			if not os.path.exists(txtpath):
				fileflag=self.save_file_with_response(txtpath,txtdownload)
			
			
			if (not fileflag ):
				f_fail.write(info)
				f_fail.write('\n')
			''''
			elif  (not self.txthandler.handletxt(txtpath,handletxtpath)) :
				f_fail.write(info)
				f_fail.write('\t\t\t 已经转换过了\n')
				#shutil.copy(txtpath,failconvertxtpath)
				self.txthandler.delete_txt_without_encoding(txtpath,failconvertxtpath)
			'''

		f_fail.close()

	def save_file_with_response(self,filename, url):
		def get_url_response(url):
			headers ={
		            'Accept': '*/*',
		            'Accept-Encoding': 'identity;q=1, *;q=0',
		            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		            'Connection': 'keep-alive',
		            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',		 
		            'Range': 'bytes=0-'
		           }
			#r = s.get(url, headers=headers, stream=True)
			#r = s.get(url, stream=True)
			try:
				r = self.s.get(url)
			except Exception as e:
				print('filename=[%s] 获取其网页失败'% filename)
				print(e)
				return False
			#print(r)
			return r
		content = get_url_response(url)
		if content == False:
			return False
		else:
			with open(filename, 'wb') as fd:
			    for chunk in content.iter_content(chunk_size=128):
		        	fd.write(chunk)
			return True
	
	def print_database_and_table_name(self):
		a=0
		for database in self.client.database_names():
			if 'xuanshuxiaoshuo' == database:
				for table in self.client['xuanshuxiaoshuo'].collection_names():
					#print('table [%s] is in database [%s]' %(table,database))
					print('"%s",'% table)
				for table in self.client['xuanshuxiaoshuo'].collection_names():	
					a=a+self.wuxian[table].find().count()
					print('"%s  [%d/%d]",'% (table,self.wuxian[table].find().count(),a))
			#for table in self.client[database].collection_names():
			#	print('table [%s] is in database [%s]' %(table,database))



class Handletxt():
	def __init__(self):
		self.novelpath='无限novel\\东方玄幻'

	def getfilelist(self,path):
		filelist=[]
		for file in os.listdir(path):
			novel=path+'\\'+file
			print(novel)
			new_novel=r'E:\python_study\wuxianxiaoshuo\无限小说原始not\东方玄幻'+'\\'+file
			new_novel1=r'E:\python_study\wuxianxiaoshuo\无限小说原始\东方玄幻'+'\\'+file
			if not self.handletxt(novel,new_novel1):
				self.delete_txt_without_encoding(novel,new_novel)
			filelist.append(novel)
		print(len(filelist))
		return filelist


		'''
		for parent,dirnames,filenames in os.walk(path):

			#case 1:
			for dirname in dirnames:
				print("parent folder is:" + parent)
				print("dirname is:" + dirname)
			#case 2
			for filename in filenames:
				print("parent folder is:" + parent)
				print("filename with full path:"+ os.path.join(parent,filename))
		'''
	def handletxt(self,path,newpath):
		def delete_txt_with_encoding(path,newpath,openEncoding='gbk'):
			if os.path.exists(path):
				fread1=open(path,'r',encoding=openEncoding)
			else:
				return False
			try:
				f1=fread1.readlines()
				fread1.close()
				if len(f1)<1:
					return False
				if '用户上传之内容开始' in f1[1] and '用户上传之内容结束' in f1[-2]:
					f1=f1[2:-2]
				#os.remove(path)
				fwrite1=open(newpath,'w',encoding='utf-8')
				fwrite1.writelines(f1)
				fwrite1.close()
				return True
			except Exception as e1:
				fread1.close()
				print('[%s] 以【%s】 编码格式不能处理' % (path,openEncoding))
				print(e1)
				return False

		if delete_txt_with_encoding(path,newpath):
			return True
		else:
			return delete_txt_with_encoding(path,newpath,openEncoding='ASNI')

	def delete_txt_without_encoding(self,path,newpath):
		fread1=open(path,'rb')
		f1=fread1.readlines()
		if len(f1)<1:
			return False
		if '用户上传之内容开始' in f1[1].decode('gbk') and '用户上传之内容结束' in f1[-2].decode('gbk'):
			f1=f1[2:-2]
		fread1.close()

		fwrite1=open(newpath,'wb')
		fwrite1.writelines(f1)
		fwrite1.close()

def test():
	tasthandle=Handletxt()
	#tasthandle.getfilelist(r'E:\python_study\wuxianxiaoshuo\无限小说原始not\异世大陆')
	tasthandle.getfilelist(r'E:\python_study\wuxianxiaoshuo\无限小说\东方玄幻')
#test()
b=[
"名著其他  [450/16201]",
"历史架空  [2633/11357]",
"科幻战争  [2846/8724]",
"网游同人  [3060/34007]",
"仙侠修真  [4394/15751]",
"都市官场  [5878/5878]",
"玄幻奇幻  [8833/42840]"
"穿越言情  [14746/30947]",
]
a=["都市官场","科幻战争",
"历史架空","仙侠修真",
"名著其他","穿越言情",
"网游同人","玄幻奇幻"]
#print(sys.argv[1])
mymongo=PymongoDataSave()
#mymongo.print_database_and_table_name()
mymongo.getData('仙侠修真')
