#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/13 下午3:17
# @Author  : Sahinn
# @File    : cp_news.py
# use cp_news
# db.createCollection("news",{size:4096,max:4096})
import re
import urllib
import urllib2
import traceback
import hashlib
import json

import pymongo
from pymongo import MongoClient

mail_url = 'http://172.16.3.145:82/LeheQ'
client = MongoClient('172.16.22.251', 27017)
mail_reciever = 'zuobin@qq.com'
db = client.cp_news
collection = db['news']
trace = []


def url_get(url, timeout=30, encoding="utf8"):
    i_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                 "Referer": 'http://www.baidu.com'}
    req = urllib2.Request(url, headers=i_headers)
    result = urllib2.urlopen(req, timeout=timeout)
    content = result.read()
    if encoding != "utf8":
        content = unicode(content, encoding).encode("utf8")
    return content


def log_record():
    trace.append(traceback.format_exc())


# 中彩网
def zhcw_zygg_parser():
    try:
        base_url = 'http://www.zhcw.com'
        url = 'http://www.zhcw.com/xinwen/zhongyaogonggao/'
        ul_reg = u'<ul class="Nlistul">[\s\S]*?<\/ul>'
        li_reg = u'<li><span class="Nlink">.*?href="(.*?)".*?>(.*?)<\/a>[\s\S]*?Ntime">(.*?)</span><\/li>'
        content = url_get(url)
        ul_group = re.findall(ul_reg, content, re.S | re.M)
        li_group = re.findall(li_reg, ul_group[0], re.S | re.M)
        pre_map = {}
        for li_line in li_group:
            pre_save(pre_map, unicode(base_url + li_line[0], 'utf-8'), unicode(li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'))
        filter_news(pre_map)
        news_save(pre_map)
    except :
        log_record()


# 中国体彩网
def zhtc_zzgg_parser():
    try:
        base_url = 'http://www.lottery.gov.cn'
        url = 'http://www.lottery.gov.cn/tzgg/index.html'
        ul_reg = u'<div class="main_l">[\s\S]*?<\/div>'
        li_reg = u'<li><span>\((.*?)\)<\/span><a.*?<\/a><a.*?href="(.*?)">(.*?)<\/a><\/li>'
        content = url_get(url)
        ul_group = re.findall(ul_reg, content, re.S | re.M)
        li_group = re.findall(li_reg, ul_group[0], re.S | re.M)
        pre_map = {}
        for li_line in li_group:
            pre_save(pre_map, unicode(base_url + li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), unicode(li_line[0], 'utf-8'))
        filter_news(pre_map)
        news_save(pre_map)
    except :
        log_record()


# 山东体彩网
def sdtc_tcgz_parser():
    try:
        base_url = 'http://www.sdticai.com/'
        url = 'http://www.sdticai.com/news.asp?dlei=4'
        td_reg = u'<td.*?class="dbk".*?href="(.*?)".*?<span.*?">(.*?)<\/span>.*?<\/td>[\s\S]*?<td.*?class="dbk".*?">\[(.*?)\]<\/span><\/td>'
        content = url_get(url, encoding='gb2312')
        td_group = re.findall(td_reg, content, re.S | re.M)
        pre_map = {}
        for li_line in td_group:
            pre_save(pre_map, unicode(base_url + li_line[0], 'utf-8'), unicode(li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'))
        filter_news(pre_map)
        news_save(pre_map)
    except :
        log_record()


# 广东体彩网
def gdlottery_parser():
    try:
        base_url = 'http://www.gdlottery.cn'
        url = 'http://www.gdlottery.cn/html/gonggao/index.html'
        td_reg = u'<span.*?class=\"r\">\((.*?)\s.*?\)<\/span>[\s\S]*?<a.*?href=\"(.*?)\".*?>(.*?)<\/a>'
        content = url_get(url)
        td_group = re.findall(td_reg, content, re.S | re.M)
        pre_map = {}
        for li_line in td_group:
            date = unicode(li_line[0], 'utf-8').replace(u"年", u"-").replace(u"月", u"-").replace(u"日", u"")
            pre_save(pre_map, unicode(base_url + li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), date)
        filter_news(pre_map)
        news_save(pre_map)
    except :
        log_record()


def pre_save(pre_map, url, title, date):
    md5 = hashlib.md5()
    key = url + title + date
    md5.update(key.encode('utf-8'))
    md5_digest = md5.hexdigest()
    pre_map[md5_digest] = {'key': md5_digest, 'url': url, 'title': title, 'date': date, 'is_warning': False}


def filter_news(pre_map):
    keys = []
    for key in pre_map:
        keys.append(key)
    db_news = collection.find({"key": {"$in": keys}}, projection={'key': True, '_id': False})
    for doc in db_news:
        if doc['key'] in pre_map:
            del pre_map[doc['key']]


def news_save(news_map):
    if not news_map:
        return
    docu = []
    for key in news_map:
        docu.append(news_map[key])
    collection.insert_many(docu)


def send_mail():
    db_news = collection.find({"is_warning": False}, projection={'_id': False}).sort('date', pymongo.DESCENDING)
    content = u''
    update_key = []

    for doc in db_news:
        update_key.append(doc['key'])
        content += (u"<li><a href=\"%s\">(%s)%s</a></li>" % (doc['url'], doc['date'], doc['title']))
    trace_m = u''
    if trace:
        for m in trace:
            trace_m += m
    if not content:
        content = u'今日无最新新闻'
    html = u'''<html><head><meta http-equiv=Content-Type content=text/html; charset=utf-8></head><body>
    <h2>彩票新闻推送</h2>
    <ul>''' + content + u'''</ul>
    trace : ''' + trace_m + '''</body></html>'''
    import datetime
    message = {"content": html, "encoding": "", "fromAddress": "qa@lecai.com", "fromDisplay": "", "htmlStyle": True, "mailType": "",
     "mailto": mail_reciever, "subject": datetime.datetime.now().strftime('%Y-%m-%d') + u"彩票新闻推送"}
    request = urllib2.Request(mail_url)
    message = json.dumps(message)
    data = {"q": "mailqueue", "p": "10001", "data": message, "datatype": 'json', "callback": ""}
    urllib2.urlopen(request, urllib.urlencode(data))
    if update_key:
        collection.update_many({"key": {"$in": update_key}}, {"$set": {"is_warning": True}})


def main():
    zhcw_zygg_parser()
    zhtc_zzgg_parser()
    sdtc_tcgz_parser()
    gdlottery_parser()
    send_mail()

if __name__ == "__main__":
    main()

