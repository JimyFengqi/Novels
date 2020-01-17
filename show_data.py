from pyecharts import Bar
import sqlite3 




class MyData():
	def __init__(self,db_path):
		self.db_path=db_path
		self.conn = sqlite3.connect(self.db_path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
		self.cursor=self.conn.cursor() 
		self.tablenames = self.cursor.execute("select name from sqlite_master where type='table'") #获取表名
		self.tablename = self.tablenames.fetchall()[0][0]                   #fetchall得到的是一个list,里面每个元素是(a,)这种类型的
		

	def get_colName(self):
		col_names =self.cursor.execute('pragma table_info({})'.format(self.tablename)).fetchall()
		colname = [x[1] for x in col_names]
		print (colname)

	#统计每种小说额数量	
	def get_noveltypeNum(self):
		exectCmd = 'select noveltype from %s' % (self.tablename)
		rows= self.cursor.execute(exectCmd).fetchall()    #该例程执行一个 SQL 语句
		a = set([row[0] for row in rows])
		data = [] 
		for t in list(a):
			noveltypenum = self.cursor.execute('select * from %s where noveltype="%s" ' % (self.tablename,t)).fetchall()
			data.append((t,len(noveltypenum)) )
		data.sort(key=self.takesecond,reverse=False)
		return data

	#为了排序比较函数	
	def takesecond(self,elem):
		return float(elem[1])

	def readFromSqllite(self,datatype1,datatype2):
		exectCmd = 'select %s,%s from %s' % (datatype1,datatype2,self.tablename)
		rows= self.cursor.execute(exectCmd).fetchall()    #该例程执行一个 SQL 语句
		data = [row for row in rows]
		data.sort(key=self.takesecond,reverse=False)
		return data[:10]





	def close(self): 
		self.conn.close()


db_path   = 'zhuajishuwudb.sqlite3'
mydata    = MyData(db_path)
d1=mydata.get_noveltypeNum()


def drawecharts(namelist,numlist):
	'''
	title -> str
	主标题文本，支持 \n 换行，默认为空

	subtitle -> str
	副标题文本，支持 \n 换行，默认为 空

	width -> int
	画布宽度，默认为 800（px）

	height -> int
	画布高度，默认为 400（px）

	title_color -> str
	主标题文本颜色，默认为 ‘#000’

	subtitle_color -> str

	副标题文本颜色，默认为 ‘#aaa’

	background_color -> str

	画布背景颜色，默认为 ‘#fff’

	page_title -> str
	指定生成的 html 文件中 <title> 标签的值。默认为’Echarts’

	renderer -> str
	指定使用渲染方式，有 ‘svg’ 和 ‘canvas’ 可选，默认为 ‘canvas’。
	'''

	bar = Bar("小说数量统计", "2019-6-28", title_color='red', title_pos='right', width=1200, height=600,background_color='#fff') 
	'''
	is_random -> bool
	是否随机排列颜色列表，默认为 False

	label_color -> list
	自定义标签颜色。全局颜色列表，所有图表的图例颜色均在这里修改。如 Bar 的柱状颜色，Line 的线条颜色等等。

	is_label_show -> bool
	是否正常显示标签，默认不显示。标签即各点的数据项信息

	label_pos -> str
	标签的位置，Bar 图默认为’top’。有’top’, ‘left’, ‘right’, ‘bottom’, ‘inside’,’outside’可选

	label_text_color -> str
	标签字体颜色，默认为 “#000”

	label_text_size -> int
	标签字体大小，默认为 12

	is_random -> bool
	是否随机排列颜色列表，默认为 False

	label_formatter -> function
	'''
	bar.add("下载数量", namelist, numlist, is_more_utils=True,is_label_show=True, is_datazoom_show=False,legend_pos='left',is_convert=False,is_random=True) 


	# 其他主题：vintage,macarons,infographic,shine，roma 
	bar.use_theme("vintage")     #单个主题更换
	#  from pyecharts import configure    #全局主题更换
	#  configure(global_theme='vintage')  #全局主题更换
	bar.show_config()
	bar.render()

def drawecharts2(namelist,numlist):
	'''
	title -> str
	主标题文本，支持 \n 换行，默认为空

	subtitle -> str
	副标题文本，支持 \n 换行，默认为 空

	width -> int
	画布宽度，默认为 800（px）

	height -> int
	画布高度，默认为 400（px）

	title_color -> str
	主标题文本颜色，默认为 ‘#000’

	subtitle_color -> str

	副标题文本颜色，默认为 ‘#aaa’

	background_color -> str

	画布背景颜色，默认为 ‘#fff’

	page_title -> str
	指定生成的 html 文件中 <title> 标签的值。默认为’Echarts’

	renderer -> str
	指定使用渲染方式，有 ‘svg’ 和 ‘canvas’ 可选，默认为 ‘canvas’。
	'''

	bar = Funnel("小说数量统计", "2019-6-28", title_color='red', title_pos='right', width=1200, height=600,background_color='#fff') 
	'''
	is_random -> bool
	是否随机排列颜色列表，默认为 False

	label_color -> list
	自定义标签颜色。全局颜色列表，所有图表的图例颜色均在这里修改。如 Bar 的柱状颜色，Line 的线条颜色等等。

	is_label_show -> bool
	是否正常显示标签，默认不显示。标签即各点的数据项信息

	label_pos -> str
	标签的位置，Bar 图默认为’top’。有’top’, ‘left’, ‘right’, ‘bottom’, ‘inside’,’outside’可选

	label_text_color -> str
	标签字体颜色，默认为 “#000”

	label_text_size -> int
	标签字体大小，默认为 12

	is_random -> bool
	是否随机排列颜色列表，默认为 False

	label_formatter -> function
	'''
	bar.add("下载数量", namelist, numlist, is_more_utils=True,is_label_show=True, is_datazoom_show=False,legend_pos='left',is_convert=False,is_random=True) 


	# 其他主题：vintage,macarons,infographic,shine，roma 
	bar.use_theme("vintage")     #单个主题更换
	#  from pyecharts import configure    #全局主题更换
	#  configure(global_theme='vintage')  #全局主题更换
	bar.show_config()
	bar.render('a.png')

#d1 = mydata.readFronSqllite('novelname','novelsize')
drawecharts([a[0] for a in d1],[a[1] for a in d1])
