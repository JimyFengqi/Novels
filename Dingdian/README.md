# Novel_spider

本文以scrapy 框架来爬取整个顶点小说网的小说


1.scrapy的安装
这个安装教程，网上有很多的例子，这里就不在赘述了

2.关于scrapy
scrapy框架 是一个非常好的东西，能够实现异步爬取，节省时间，其实本文纯粹的按照之前的思维来做，
也不是不可以，但是感觉速度太慢了，毕竟数据量有点大
框架内容也在网上找找例子吧

3.直接说实现吧


使用 命令
scrapy startproject dingdian  
创建项目

然后增加文件，最后代码目录如下：

[python] view plain copy
├── dingdian  
│   ├── __init__.py  
│   ├── items.py  
│   ├── pipelines.py  
│   ├── settings.py  
│   └── spiders  
│       ├── __init__.py  
│       └── mydingdian.py  


主程序是：mydingdian.py
定义的存贮条目内容即 ：items.py
设置相关  settings.py
最终的数据处理以及保存：pipelines.py
