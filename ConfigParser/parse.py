#!/usr/bin/env python
# -*- coding: utf-8 -*-  

# Author: huntinux@gmail.com
# Create Date: 2014-06-03 
# Description: 读取ini文件



import ConfigParser
config = ConfigParser.SafeConfigParser()

config.read("config.ini")
#sections = config.sections()
#print sections
#
#options = config.options("main")
#print options
#
#items = config.items("main")
#print items
#
#value = config.get("main","version")
#print value

value = config.get("machines", "product_machines")
print value.strip().split("\n")

value = config.get("machines", "beta_machines")
print value.strip().split("\n")

config.set('main', 'version', '2014-09-23')

fp = open(r'config.ini','w')
config.write(fp)
fp.close()

# 参考：http://my.oschina.net/mutour/blog/32530 
