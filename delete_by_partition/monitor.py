#!/usr/bin/ptyhon
# coding:utf8
import datetime
import urllib2
import json
import sys
def get_index_properties(url,index_name):
    # 获取索引的相关配置 如果获取不到返回空
    prop=None
    context_stream=None
    try:
        context_stream=urllib2.urlopen(url+'/'+index_name)
        tmp=context_stream.read()
        prop=json.loads(tmp).get(index_name)
    except urllib2.HTTPError,e:
        print datetime.datetime.now(),index_name,'索引不存在'
    finally:
        if type(context_stream)!=type(None):
            context_stream.close()
    return prop
def create_index(url,index_name,prop):
    response=None
    try:
        request=urllib2.Request(url+'/'+index_name,json.dumps(prop))
        request.get_method=lambda:'PUT'
        response=urllib2.urlopen(request)
        response.read()
        # 打印相关日志
        print datetime.datetime.now(),'创建',index_name
    except urllib2.HTTPError,e:
        print datetime.datetime.now(),index_name,'创建索引失败'
    finally:
        if type(response)!=type(None):
            response.close()
def index_exists(url,index_name):
    # 获取索引的相关配置 如果获取不到返回空
    prop=False
    context_stream=None
    try:
        context_stream=urllib2.urlopen(url+'/'+index_name)
        prop=True
    except urllib2.HTTPError,e:
        print datetime.datetime.now(),index_name,'索引不存在'
    finally:
        if type(context_stream)!=type(None):
            context_stream.close()
    return prop
def day_monitor(url,types):
    # 获取当前时间
    now_date=datetime.datetime.now()
    # 获取昨天时间
    yesterday=now_date+datetime.timedelta(-1)
    now_str=now_date.strftime('%Y%m%d')
    yester_str=yesterday.strftime('%Y%m%d')
    for ty in types:
        if index_exists(url,ty+'_'+yester_str):
            if not index_exists(url,ty+'_'+now_str):
                prop=get_index_properties(url,ty+'_'+yester_str)
                if prop!=None:
                    create_index(url,ty+'_'+now_str,prop)
            else:
                print datetime.datetime.now(),ty+'_'+now_str,'已经存在'
        else:
            print datetime.datetime.now(),ty+'_'+yester_str+'不存在'
def close_index(url,index_name):
    response=None
    try:
        request=urllib2.Request(url+'/'+index_name+'/_close')
        request.get_method=lambda:'POST'
        response=urllib2.urlopen(request)
        response.read()
        # 打印相关日志
        print datetime.datetime.now(),'关闭',index_name
    except urllib2.HTTPError,e:
        print datetime.datetime.now(),index_name,'关闭索引失败'
    finally:
        if type(response)!=type(None):
            response.close()
# from: http://blog.ipattern.org/archives/417
# input datetime1, and an month offset
# return the result datetime
def datetime_offset_by_month(datetime1, n = 1):
    # create a shortcut object for one day
    one_day = datetime.timedelta(days = 1)
    # first use div and mod to determine year cycle
    q,r = divmod(datetime1.month + n, 12)
    # create a datetime2
    # to be the last day of the target month
    datetime2 = datetime.datetime(
            datetime1.year + q, r + 1, 1) - one_day
    # if input date is the last day of this month
    # then the output date should also be the last
    # day of the target month, although the day
    # may be different.
    # for example:
    # datetime1 = 8.31
    # datetime2 = 9.30
    if datetime1.month != (datetime1 + one_day).month:
        return datetime2
    # if datetime1 day is bigger than last day of
    # target month, then, use datetime2
    # for example:
    # datetime1 = 10.31
    # datetime2 = 11.30
    if datetime1.day >= datetime2.day:
        return datetime2
    # then, here, we just replace datetime2's day
    # with the same of datetime1, that's ok.
    return datetime2.replace(day = datetime1.day)
def month_monitor(url,types):
    datetime1=datetime.datetime.now()
    cur_day=datetime1.strftime("%Y%m")
    create_day=datetime_offset_by_month(datetime1, 1).strftime("%Y%m")
    close_day=datetime_offset_by_month(datetime1, -15).strftime("%Y%m")
    print create_day,close_day
    for ty in types:
        # 判断索引是否存在
        if index_exists(url,ty+'_'+cur_day):
            # 判断是否存在下一个月
            if not index_exists(url,ty+'_'+create_day):
                #创建
                prop=get_index_properties(url,ty+'_'+cur_day)
                create_index(url,ty+'_'+create_day,prop)
            else:
                print datetime.datetime.now(),ty+'_'+create_day,'已经存在'
            # 判断前15个月的那个月的索引是否存在
            if index_exists(url,ty+'_'+close_day) :
                # 关闭
                close_index(url,ty+'_'+close_day)
def help():
    print '''
    monitor.py day_monitor or monitor.py month_monitor
    '''
if __name__=='__main__':
    types=['calls','inters']
    if len(sys.argv)!=2 or not (sys.argv[1]=='day_monitor' or sys.argv[1]=='month_monitor'):
        print help()
    if sys.argv[1] == 'day_monitor':
        url='http://192.168.57.139:9200'
        day_monitor(url,types)
    else:
        url='http://192.168.57.139:9200'
        month_monitor(url,types)
