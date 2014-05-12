#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 
# Description: extract VALIDITY module
#

import re
import time
import datetime
from datetime import date
from collections import defaultdict

MONTH = {
'JAN':'01',
'FEB':'02',
'MAR':'03',
'APR':'04',
'MAY':'05',
'JUN':'06',
'JUL':'07',
'AUG':'08',
'SEP':'09',
'OCT':'10',
'NOV':'11',
'DEC':'12'
}

###########################################################################
#### get the year before
### param: dt is type of date
###########################################################################
def getYearBefore(dt):
    year = dt.year - 1
    month = dt.month
    day = dt.day
    if  month == 2 and day == 29 and not isLeapyear(year):
        day = 28
    return date(year,month,day)


def isLeapyear(year):
    if year%400 == 0:
        return True
    elif year%4 == 0 and year%100 != 0:
        return True
    return False

###########################################################################
#### extract querytime to the format "20120601"
###########################################################################
def extractQuerytime(data):
    if data.isdigit():
        return data
    t = data
    if len(t) == 7:
        # 形如 4OCT12
        d = t[:2]
        m = MONTH[t[2:5]]
        y = str(2000 + int(t[5:]))
    if len(t) == 6:
        # 形如 04OCT12
        d = t[:1]
        m = MONTH[t[1:4]]
        y = str(2000 + int(t[4:]))
    elif len(t) == 9:
        # 形如 04OCT2012
        d = t[:2]
        m = MONTH[t[2:5]]
        y = t[5:]
    elif len(t) == 5:
        # 形如 04OCT
        d = t[:2]
        m = MONTH[t[2:]]
        y = str(time.localtime(time.time()).tm_year )
    elif len(t) == 4:
        # 形如 4OCT
        d = '0'+t[:1]
        m = MONTH[t[1:]]
        y = str(time.localtime(time.time()).tm_year )

    querytime = y + m + d 
    return querytime

def extractStamptime(data):
    if data.strip() != '':
        return data.strip().split()[0] 
    return ''

###########################################################################
#### get crawler time or extract time 
###########################################################################
def getQueryAndCrawlerTime(result):
    querytime =''
    if 'querytime' in result and result['querytime'].strip() != '':
        querytime= result['querytime']
    elif 'timestamp'in result and result['timestamp'].strip() != '':
        querytime = result['timestamp']
    return querytime

###########################################################################
#### get crawler time or extract time or current time
###########################################################################
def getDefaulttime(result):
    querytime =''
    if 'querytime' in result and result['querytime'].strip() != '':
        return result['querytime']
    elif 'timestamp'in result and result['timestamp'].strip() != '':
        return result['timestamp']
    else:
        t = time.localtime(time.time())
        y, m, d = str(t.tm_year), str(t.tm_mon), str(t.tm_mday)
        if len(m) == 1: m = '0' + m
        if len(d) == 1: d = '0' + d
        return y + m + d 

def getNOW(querytime):
    now = date(int(querytime[:4]),int(querytime[4:6]),int(querytime[6:]))
    now365 = now + datetime.timedelta(days=365)
    infinity = now + datetime.timedelta(days=365*2)
    NOW = str(now).replace('-','')
    NOW365 = str(now365).replace('-','')
    INFINITY = str(infinity).replace('-','')
    defaultMap = {'NOW':NOW,'NOW365':NOW365,'INFINITY':INFINITY}
    return defaultMap

###########################################################################
#### the below is about 05 function module
###########################################################################
def getADVP(string):
    if string == '':
        return 0
    segments = string.split('|')
    res = []
    for seg in segments:
        if seg == '':continue
        res.append(dealSegment(seg))
    return min(res)

def dealSegment(segment):
    items = sorted(segment.split('/'))
    res = [[],[],[]]
    for item in items:
        if item.strip() == '':continue
        key, value = item.split('-')
        res[int(key)-1].append(int(value))
    for item in res:
        if len(item) != 0:
            return min(item)


##############################################################################
####  the below is about time function module, such 03 11 and 14
##############################################################################



##############################################################
### @param: type is list
### @return: map {'OUTBOUND': '', 'INBOUND': ''}
##############################################################
def combineTimes(datalist, default = 'OUTBOUND'):
    res = defaultdict(list)
    for data in datalist:
        data = data.strip().split()
        if 1 == len(data):
            res[default].append(data[0])
        elif 2 == len(data):
            res[data[0]].append(data[1])

    for key, value in res.items():
        res[key] = '/'.join(sorted(list(set(value))))
    return res



##############################################################
### @param:字符串 format：T-T direction 
### @return: [T-T]
##############################################################
def getTimes(default, string):
    direction, content = findDirec(string)

    #replace month in string with digit
    for month in MONTH.keys():
        content = content.replace(month,MONTH[month])

    #get complete time info, including day,month,year
    old = direction + ' ' + content
    res = toTimes(default, content)
    return direction + ' ' + res

def findDirec(string):
    datalist = string.strip().split()
    if len(datalist) > 2:
        for data in datalist:
            if '-' in data:
                content = data
            else:
                direction = data
    elif len(datalist) == 2:
        content = datalist[0] if '-' in datalist[0] else datalist[1]
        direction = datalist[1] if '-' in datalist[0] else datalist[0]
    elif len(datalist) == 1:
        content = string
        direction = ''
    return (direction, content)

def toTimes(pre, content):
    #get NOW NOW365 INFINITY
    NNI = getNOW(pre)

    result = []
    data = re.split('-|/',content)
    for i in xrange(len(data)):
        pre, current = dealOne(pre, i, data, NNI)
        result.append(current)

    res = []
    while len(result) != 0:
        res.append(result.pop(0) + '-' + result.pop(0))
    res = timeInter(res)
    return '/'.join(res)


def dealOne(pre, i, data, NNI):
    one = data[i]
    # deal now and infinity
    if one in call_map.keys():
        return call_map[one](pre, i, data, NNI)

    # deal first element in data
    if 0 == i and 4 == len(one):
        return call_map[0](pre, one)

    # deal other cases like len = 4, 6, 8
    if len(one) in call_map.keys():
        return call_map[len(one)](pre, one)


def dealNow(pre, i, data, NNI):
    return NNI['NOW'], NNI['NOW']

def dealInfinity(pre, i, data, NNI): 
    if i+1 < len(data) and 4 == len(data[i+1]):
        data[i+1] = data[i+1] + pre[:4]
    return pre, NNI['INFINITY']

def dealNow365(pre, i, data, NNI): 
    if i+1 < len(data) and 4 == len(data[i+1]):
        data[i+1] = data[i+1] + pre[:4]
    return pre, NNI['NOW365']

def dealFirst(pre, one):
    current =  pre[:4] + getMD(one)
    return current, current

def dealLength6(pre, one):
    current = '20' + one[-2:] + getMD(one[:-2])
    return current, current

def dealLength4(pre, one):
    if int(getMD(one)) < int(pre[4:]):
        current =  str(int(pre[:4]) + 1) + getMD(one)
    elif int(getMD(one)) >= int(pre[4:]):
        current = pre[:4] + getMD(one)
    return current, current

def dealLength8(pre, one):
    current = one[-4:] + one[2:4] + one[:2]
    return current, current

call_map = {
        6: dealLength6,
        4: dealLength4,
        8: dealLength8,
        0: dealFirst,
        'now': dealNow,
        'infinity': dealInfinity,
        'now365':dealNow365
        }

def getMD(string):
    return string[-2:] + string[:2]

##############################################################
### deal with 03 and 14
##############################################################

def timeUnion(times_dict):
    res = []
    for key, value in times_dict.items():
        res += timeInter(value)
    return res

def whichyears(one, res_dict):
    begin = int(str(one[0])[0:4])
    end = int(str(one[1])[0:4])
    if begin == end: 
        res_dict[begin].append('-'.join(one))
    elif end - begin == 1:
        res_dict[begin].append('-'.join([one[0], str(begin) + '1231']))
        res_dict[end].append('-'.join([str(end) + '0101', one[1]]))
    else:
        res_dict[begin].append('-'.join([one[0], str(begin) + '1231']))
        res_dict[end].append('-'.join([str(end) + '0101', one[1]]))
        for mid in xrange(begin+1, end):
            res_dict[mid].append('-'.join([str(mid) + '0101', str(mid) + '1231']))
    pass

def split_time2dict(onelist):
    onelist = [ one.split('-') for one in onelist]
    onedict = defaultdict(list)
    for one in onelist:
        whichyears(one, onedict)

    return onedict



##############################################################
### @param：timeList保存的是时间段
### @return：时间交集
##############################################################

def timeInter(timeList):
    """
    """
    if len(timeList)  == 0: return []
    timeList.sort()
    splited = []
    res = []
    for k in timeList:
        splited.append(k.split('-'))

    item1 = splited[0]
    for k in range(1,len(splited)):
        ret = inter(item1,splited[k])
        if ret==None:
            res.append(item1[0]+"-"+item1[1])
            item1 = splited[k]
        else:
            item1 = ret
    res.append(item1[0]+'-'+item1[1])
    return res


def inter(time1,time2):
    begin = max(time1[0],time2[0])
    end = min(time1[1],time2[1])
    if begin<=end:
        return [begin,end]
    else:
        return None

if __name__ == '__main__':
    #print timeUnion(['20110101-20110110','20110102-20110105','20110104-20110116'])
    #print timeUnion(['20110202-20110202','20110202-20111231'])
    #print timeUnion(['20111231-20111231','20110202-20111231'])
    #print timeInter(['20110202-20110431','20110202-20110431'])
    #getTimes('20120101','01OCT10-now365')
    print extractQuerytime('12JUL13')
