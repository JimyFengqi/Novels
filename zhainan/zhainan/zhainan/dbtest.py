import sqlite3,os  

class DbManager(object):
    def __init__(self):
        #self.dbname=os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))+'\\'+"zhainandb.sqlite3"
        self.dbname=os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))+'/'+"testdb.sqlite3"
        print(self.dbname)
        self.db = sqlite3.connect(self.dbname)
        self.cursor = self.db.cursor()
        self.tablename= 'test_novel'
        self.initDB(self.tablename)
    def initDB(self,tablename):        
        if not os.path.exists(self.dbname) or os.path.getsize(self.dbname) < 10:
            create_novel_tableString = """
            CREATE TABLE IF NOT EXISTS %s(
            id integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
            novelname text unique NOT NULL, 
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


    def insertData(self,item):
        data = dict(item)#将item变成字典形式
        keys = ','.join(data.keys())#将字典的键值做成“，”隔开的字符串
        values = ','.join(['%s'] * len(data))#根据data字典的长度建立对应长度数的“%s”
        sql = 'insert or ignore into %s(%s) values %s' %(self.tablename,keys,tuple(data.values()))
        print(sql)
        self.cursor.execute(sql)#执行sql语句
        self.db.commit()#提交

a=DbManager()
data={'author': '不爱吃草的羊',
 'downloadNum': '0',
 'imgurl': 'http://img.xqishu.com/pic/x_201948001.jpg',
 'novelid': '73972',
 'novelname': '篮球之上帝之鞭',
 'novelsize': 2485125.12,
 'novelstatus': '已完结 ',
 'noveltype': '青春校园',
 'novelurl': 'http://www.zntxt.com/txt/73972.html',
 'simplyintroduce': '他是狡猾的狐狸，他是勇猛的雄狮，他是突然窜入篮球世界的精明野蛮人，他是东部旧王朝的新君主，他是踩过旧时代开启新世纪的篮球帝王，他是NBA的阿提拉，他是上帝手中的皮鞭。他是福克斯－莱昂，篮球界的上帝之鞭。...',
 'txtdownload': 'http://xiazai.xqishu.com/txt/篮球之上帝之鞭.txt',
 'zipdownload': 'http://xiazai.xqishu.com/rar/篮球之上帝之鞭.rar'}
data1={'author': '从0',
 'downloadNum': '0',
 'imgurl': 'http://img.xqishu.com/pic/x_201947998.jpg',
 'novelid': '73975',
 'novelname': '全球狂欢夜',
 'novelsize': 1059061.76,
 'novelstatus': '已完结 ',
 'noveltype': '科幻世界',
 'novelurl': 'http://www.zntxt.com/txt/73975.html',
 'simplyintroduce': '：2028年，一场空前浩劫悄然而至，席卷全球，整个世界在刹那间暗无天日。“想要活下去吗？那么，抽签吧。”那未知的存在发出了一声面向全世界人类的命令。宋辛捏着凭空出现在眼前的一张纸片，听到那声音说：“可怜的倒霉蛋哟，恭喜...',
 'txtdownload': 'http://xiazai.xqishu.com/txt/全球狂欢夜.txt',
 'zipdownload': 'http://xiazai.xqishu.com/rar/全球狂欢夜.rar'}
data2={'author': '白眼镜猫',
 'downloadNum': '0',
 'imgurl': 'http://img.xqishu.com/pic/x_201947997.jpg',
 'novelid': '73976',
 'novelname': '圣光并不会保佑你',
 'novelsize': 3208642.56,
 'novelstatus': '已完结 ',
 'noveltype': '异世大陆',
 'novelurl': 'http://www.zntxt.com/txt/73976.html',
 'simplyintroduce': '从艾泽拉斯到外域，从德拉诺到阿古斯。一个充满了谎言的真实降临在这里好吧，说点真实感想。说好的军团炸天呢？莫名其妙的就被换了家，搞得基尔加丹都死了还要每天定时定点上班，整天给大领主的小号们送福利。对了，还有伊利丹大...',
 'txtdownload': 'http://xiazai.xqishu.com/txt/圣光并不会保佑你.txt',
 'zipdownload': 'http://xiazai.xqishu.com/rar/圣光并不会保佑你.rar'}
data3={'author': '白眼镜猫',
 'downloadNum': '0',
 'imgurl': 'http://img.xqishu.com/pic/x_201947997.jpg',
 'novelid': '73976',
 'novelname': '圣光并不会保佑你',
 'novelsize': 3208642.56,
 'novelstatus': '已完结 ',
 'noveltype': '异世大陆',
 'novelurl': 'http://www.zntxt.com/txt/73976.html',
 'simplyintroduce': '从艾泽拉斯到外域，从德拉诺到阿古斯。一个充满了谎言的真实降临在这里好吧，说点真实感想。说好的军团炸天呢？莫名其妙的就被换了家，搞得基尔加丹都死了还要每天定时定点上班，整天给大领主的小号们送福利。对了，还有伊利丹大...',
 'txtdownload': 'http://xiazai.xqishu.com/txt/圣光并不会保佑你.txt',
 'zipdownload': 'http://xiazai.xqishu.com/rar/圣光并不会保佑你.rar'}

a.insertData(data)
a.insertData(data1)
a.insertData(data2)
a.insertData(data3)