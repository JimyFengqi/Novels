from __future__ import unicode_literals 

from django.db.models import Q 
from django.http import HttpResponse 
from . import models 
from django.shortcuts import render 

#定义主函数，即首页展示 
def home(request): 
	return render(request,'home.html') 

#定义ID查询入口函数，即ID入口页面 
def ID_search(request): 
	return render(request,'ID_search.html') 

#定义ID查询结果函数 
def ID_result(request): 
	novelid = request.GET['kw']
	if str(novelid) == "0": 
		return render(request, 'ID_search.html',{'error': 'novelid[%s]  error,请重新输入!'% (novelid)}) 
	try: 
		novel = models.Wuxiandjango.objects.filter(Q(novelid=novelid))
		#novel = models.Wuxiandjango.objects.get(novelid = novelid) #只查询一个返回一个
		return render(request,'ID_result.html',{'novels':novel}) 
	except Exception as e: 
		s = "编号%s不在数据库中" % novelid 
		return render(request,'ID_search.html', {'error': 'novelid[%s] 不存在，请修正后查询! %s '% (novelid,e)})

	'''
	if request.method == 'POST':
		novelid= request.POST.get('search_text','')
		if str(novelid) == "0": 
			return render(request, 'ID_search.html',{'error': 'novelid[%s]  error,请重新输入!'% (novelid)}) 
		try: 
			novel = models.Wuxiandjango.objects.get(novelid = novelid) 
			return render(request,'ID_result.html',{'novel':novel}) 
		except Exception as e: 
			s = "编号%s不在数据库中" % novelid 
			return render(request,'ID_search.html', {'error': 'novelid[%s] 不存在，请修正后查询! %s '% (novelid,e)})
	'''
#定义根据电影名查询入口函数，即电影名查询入口页面 
def NAME_search(request): 
	novelinfo = models.Wuxiandjango.objects.all()[0:20]
	return render(request,'NAME_search.html',{'novelinfo':novelinfo})

#根据电影名查询结果展示 
def NAME_result(request): 
	kw = request.GET['kw']
	novelinfos = models.Wuxiandjango.objects.filter(Q(novelname=kw))
	#novelinfo = models.Wuxiandjango.objects.get(novelname=kw)  #只查询一个返回一个
	return render(request,'NAME_result.html',{'novelinfos':novelinfos, 'kw':kw})
