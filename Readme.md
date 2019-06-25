# novel网站
| 网站        | 代码地址         | 其他  |
| ------------- |:-------------:| -----:|
|[爱去小说网](https://www.27xs.cc/)  |[下载代码](https://github.com/JimyFengqi/Novels/tree/master/aiqu/aiqu/aiqu)  | 
|[书本网](https://www.bookben.net/txt.html)	|[下载代码](https://github.com/JimyFengqi/Novels/tree/master/bookben/bookben/bookben)| 
|[落吧书屋](http://www.txt81.com/shu/)	|[下载代码](https://github.com/JimyFengqi/Novels/tree/master/luoba/luoba/luoba)  | 
|[书丫丫](https://www.shuyaya.cc/quanben/)	|[下载代码](https://github.com/JimyFengqi/Novels/tree/master/shuyaya/shuyaya/shuyaya)   |  
|[八零电子书](https://www.80txt.com/sort/4500.html)		|	[下载代码](https://github.com/JimyFengqi/Novels/tree/master/txt80/txt80)  |  
|[无限小说](http://www.555x.org/shuku.html)		|	[下载代码](https://github.com/JimyFengqi/Novels/tree/master/wuxian/wuxian/wuxian)  |  
|[炫书网书库](https://www.xuanquge.com/shuku.html)			|[下载代码](https://github.com/JimyFengqi/Novels/tree/master/xuanshuwang/xuanshuwang/xuanshuwang)  |  
|[选书网](https://www.xuanshu.com/soft/sort01/index_303.html)			|[下载代码](https://github.com/JimyFengqi/Novels/tree/master/xuanshuwang/xuanshuwang)  |  
|[爪机网](https://www.zhuaji.org/shuku/)			|[下载代码](https://github.com/JimyFengqi/Novels/tree/master/zhuajishuwu/zhuajishuwu/zhuajishuwu)  |  
|[奇书网](http://www.qishu.cc/yanqing/list10_1.html) |[下载代码](https://github.com/JimyFengqi/Novels/tree/master/qishuwang/qishuwang/qishuwang)  |  
|[宅男小说网](http://www.zntxt.com/shuku/)  |[下载代码](https://github.com/JimyFengqi/Novels/tree/master/zhainan/zhainan/zhainan)  |  
|[棉花糖](https://www.mianhuatang2.com/lx/9/11.htm)  |[下载代码](https://github.com/JimyFengqi/Novels/tree/master/mianhuatang/mianhuatang/mianhuatang)  |  
|[福利小说网](http://www.fltxt.com/xuanhuan/)  |[下载代码](https://github.com/JimyFengqi/Novels/tree/master/fulitxt/fulitxt/fulitxt)  |  
|[Txt小说下载网](https://www.xsjtxt.com/soft/1/Soft_001_1.html)  |[下载代码](https://github.com/JimyFengqi/Novels/tree/master/sjtxt/sjtxt/sjtxt)  |  

|[当书网](https://www.downbook.net/TXT/list4_1.html) |[下载代码](https://github.com/JimyFengqi/Novels/tree/master/dangshuwang/dangshuwang/dangshuwang)  |   

[飘柔文学](https://www.prwx.com/)  
[乐文小说](https://www.365xs.la/type/)  
[良久小说](https://www.txt909.com/full/1.html)  

[我爱读](https://www.woaidu.org/)  
[下书网](https://www.xiashutxt.com/type/nan_0_2_allvisit_1.html)  
[言情小说书库](http://www.fmxxs.com/)  
[请看小说网](https://www.qk6.org/shuku/0_0_0_0_2_0_0_0_1.html)  
[时光电子书](https://www.60book.com/)  
 





## 插入数据避免重复
用insert语句插入数据，为避免重复插入又不打断数据处理。 

首先要避免重复插入，就必须在插入时引发冲突。在表中设置了id字段，该字段为UNIQUE属性，当插入的id已存在时引发冲突。 

引发冲突后insert会做一些处理，处理方式由OR字句定义。包含如下： 
ROLLBACK当发生约束冲突，立即ROLLBACK，即结束当前事务处理，命令中止并返回SQLITE_CONSTRAINT代码。若当前无活动事务(除了每一条命令创建的默认事务以外)，则该算法与ABORT相同。 
ABORT当发生约束冲突，命令收回已经引起的改变并中止返回SQLITE_CONSTRAINT。但由于不执行ROLLBACK，所以前面的命令产生的改变将予以保留。缺省采用这一行为。 
FAIL当发生约束冲突，命令中止返回SQLITE_CONSTRAINT。但遇到冲突之前的所有改变将被保留。例如，若一条UPDATE语句在100行遇到冲突100th，前99行的改变将被保留，而对100行或以后的改变将不会发生。 
IGNORE当发生约束冲突，发生冲突的行将不会被插入或改变。但命令将照常执行。在冲突行之前或之后的行将被正常的插入和改变，且不返回错误信息。 
REPLACE当发生UNIQUE约束冲突，先存在的，导致冲突的行在更改或插入发生冲突的行之前被删除。这样，更改和插入总是被执行。命令照常执行且不返回错误信息。当发生NOT NULL约束冲突，导致冲突的NULL值会被字段缺省值取代。若字段无缺省值，执行ABORT算法 

为避免操作打断，我选择了IGNORE。最后完整的用法如下： 
INSERT OR IGNORE INTO troopstypes (id)values(2); 

## 常用的一些方法
* 选择特定的内容
   比如下面list内容， 只选择 class = b 的内容， xpath('class["b"]'); 
   筛选含有class 的项目                         xpath('a[(@title)]/@id') #筛选出来含有title属性的，然后取其id
```html
  <div id="post-405" class="post-405 post type-post status">inner text</div>
  <div id="post-105" class="b">inner text</div>
  <div id="post-5" class="post-5 post type-post status">inner text</div>
```    
