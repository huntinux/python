#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 从url中读取json
# 比较两个json


import json
import urllib2
import re
import sys



#d1 = json.dumps(json1,sort_keys=True,indent=4)
#d2 = json.dumps(json2,sort_keys=True,indent=4)

#print type(json.load(json1))
#filecomp.diffjson( d1, d2)
#print d1


# 根据url，得到页面内容(json)
def get_json(url):
	furl=urllib2.urlopen(url)
	strjson=furl.read()
	return strjson


# 使用正则，删除无用字符
# 删除开头第一个'{'之前的字符
# 删除结尾最后一个'{'之后的字符
def remove_invalid_char(strjson):
	start=re.compile('^[^{]*')
	strjson=start.sub('',strjson)
	end=re.compile('[^}]*$')
	strjson=end.sub('',strjson)
	return strjson

# 从命令行得到url
# TODO
if __name__ == "__main__":
	
	if len(sys.argv) != 2:
		print "please give the url"
		sys.exit(1)
	
    #url="http://l-lp3.f.dev.cn6.qunar.com:8001/all_lp.jcp?from=%E6%B5%8E%E5%8D%97&to=%E5%93%88%E5%B0%94%E6%BB%A8&goDate=2014-07-27&backDate=2014-07-27&count=90&packto=2014-07-30&packreturn=2014-08-01&packcount=9&output=json&n=0.8512787204556904&callback=SpringHotRoundtrip.parsedata"
	url=sys.argv[1]
	urlcontent = get_json(url)
	realjson = remove_invalid_char(urlcontent)
	#print realjson
	#print type(realjson)
	#print type(eval(realjson))
	#print json.dumps(realjson,sort_keys=True,indent=4)
	#print type(json.dumps(realjson))
	
	jsondict=eval(realjson)
	#print jsondict		
	print json.dumps(jsondict,sort_keys=True,indent=2)
