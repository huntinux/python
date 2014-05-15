#!/bin/bash

#
# Description: 从两个url中得到两个json，然后比较不同
# Author: hongjin.cao@qunar.com
# Date: 2014-5-15
#

NEWHOST="http://l-lp3.f.dev.cn6.qunar.com:8001"
OLDHOST="http://ws.qunar.com"
NEWJSON="newjson.json"
OLDJSON="oldjson.json"

# 参数检查
if [ $# != 1  ];then
	echo "Usage: $0 uri"
	exit 1
fi

# 根据uri和HOST生成url
uri=$1
newurl="$NEWHOST$uri"
oldurl="$OLDHOST$uri"

# 根据url获取json，并重定向到文件
python ./pretty_print_json.py "$newurl">$NEWJSON
python ./pretty_print_json.py "$oldurl">$OLDJSON

# 比较不同
colordiff -u $NEWJSON $OLDJSON | more
