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
client = MongoClient('172.16.3.251', 27017)
mail_reciever = 'sahinn@163.com'
db = client.cp_news
collection = db['news']
trace = []
func_count = {}


def url_get(url, timeout=30, encoding="utf8"):
    i_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                 "Referer": 'http://www.baidu.com'}
    req = urllib2.Request(url, headers=i_headers)
    result = urllib2.urlopen(req, timeout=timeout)
    content = result.read()
    if encoding != "utf8":
        content = unicode(content, encoding).encode("utf8")
    return content


def log_record(base_name, func):
    if base_name in func_count:
        func_count[base_name] += 1
    else:
        func_count[base_name] = 1
    if func_count[base_name] <= 3:
        func()
    else:
        trace.append(base_name + u": 请求失败超过3次</br>")
        trace.append(traceback.format_exc())
        func_count[base_name] = 0


# 中彩网
def zhcw_parser(url, fun):
    try:
        base_name = u'中彩网'
        base_url = 'http://www.zhcw.com'
        ul_reg = u'<ul class="Nlistul">[\s\S]*?<\/ul>'
        li_reg = u'<li><span class="Nlink">.*?href="(.*?)".*?>(.*?)<\/a>[\s\S]*?Ntime">(.*?)</span><\/li>'
        content = url_get(url)
        ul_group = re.findall(ul_reg, content, re.S | re.M)
        li_group = re.findall(li_reg, ul_group[0], re.S | re.M)
        if not li_group:
            trace.append(url + ":不匹配")
        pre_map = {}
        for li_line in li_group:
            pre_save(pre_map, unicode(base_url + li_line[0], 'utf-8'), unicode(li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=fun)


def zhcw_zygg_parser():
    url = 'http://www.zhcw.com/xinwen/zhongyaogonggao/'
    zhcw_parser(url, zhcw_zygg_parser)


def zhcw_dsfc_parser():
    url = 'http://www.zhcw.com/xinwen/dishifengcai/'
    zhcw_parser(url, zhcw_dsfc_parser)


# 中福在线
def cwl_parser():
    try:
        base_name = u'中福在线'
        base_url = 'http://www.cwl.gov.cn'
        url = 'http://www.cwl.gov.cn/fczx/tzgg/'
        td_reg = u'<li>.*?class="fr">(.*?)\s.*?<\/span><a.*?href=\"..\/..(.*?)\">(.*?)<\/a><\/li>'
        content = url_get(url)
        td_group = re.findall(td_reg, content, re.S | re.M)
        pre_map = {}
        if not td_group:
            trace.append(url + ":不匹配")
        for li_line in td_group:
            pre_save(pre_map, unicode(base_url + li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), unicode(li_line[0], 'utf-8'), base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=cwl_parser)


# 中福在线各省动态
def cwl_scdt_parser():
    try:
        base_name = u'中福在线'
        base_url = 'http://www.cwl.gov.cn'
        url = 'http://www.cwl.gov.cn/fczx/scdt/'
        td_reg = u'<li>.*?class="fr">(.*?)\s.*?<\/span><a.*?href=\"..\/..(.*?)\">(.*?)<\/a><\/li>'
        content = url_get(url)
        td_group = re.findall(td_reg, content, re.S | re.M)
        if not td_group:
            trace.append(url + ":不匹配")
        pre_map = {}
        for li_line in td_group:
            pre_save(pre_map, unicode(base_url + li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), unicode(li_line[0], 'utf-8'), base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=cwl_scdt_parser)


# 中福在线福彩要闻
def cwl_fcyw_parser():
    try:
        base_name = u'中福在线'
        base_url = 'http://www.cwl.gov.cn'
        url = 'http://www.cwl.gov.cn/fczx/fcyw/'
        td_reg = u'<li>.*?class="fr">(.*?)\s.*?<\/span><a.*?href=\"..\/..(.*?)\">(.*?)<\/a><\/li>'
        content = url_get(url)
        td_group = re.findall(td_reg, content, re.S | re.M)
        if not td_group:
            trace.append(url + ":不匹配")
        pre_map = {}
        for li_line in td_group:
            pre_save(pre_map, unicode(base_url + li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), unicode(li_line[0], 'utf-8'), base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=cwl_fcyw_parser)


# 中国体彩网
def zhtc_parser(url, fun):
    try:
        base_name = u'中国体彩'
        base_url = 'http://www.lottery.gov.cn'
        ul_reg = u'<div class="main_l">[\s\S]*?<\/div>'
        li_reg = u'<li><span>\((.*?)\)<\/span><a.*?<\/a><a.*?href="(.*?)">(.*?)<\/a><\/li>'
        content = url_get(url)
        ul_group = re.findall(ul_reg, content, re.S | re.M)
        li_group = re.findall(li_reg, ul_group[0], re.S | re.M)
        if not li_group:
            trace.append(url + ":不匹配")
        pre_map = {}
        for li_line in li_group:
            pre_save(pre_map, unicode(base_url + li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), unicode(li_line[0], 'utf-8'), base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=fun)


# 中国体彩网
def zhtc_zzgg_parser():
    url = 'http://www.lottery.gov.cn/tzgg/index.html'
    zhtc_parser(url, zhtc_zzgg_parser)


# 中国体彩网
def zhtc_gp_parser(url, fun):
    try:
        base_name = u'中国体彩'
        base_url = 'http://www.lottery.gov.cn'
        ul_reg = u'<div class="main_l">[\s\S]*?<\/div>'
        li_reg = u'<h4><a.*?href="(.*?)".*?>(.*?)<\/a><\/h4>\s*<p>[\s\S]*?<\/p>\s*<span>\((.*?)\)<\/span>'
        content = url_get(url)
        ul_group = re.findall(ul_reg, content, re.S | re.M)
        li_group = re.findall(li_reg, ul_group[0], re.S | re.M)
        if not li_group:
            trace.append(url + ":不匹配")
        pre_map = {}
        for li_line in li_group:
            pre_save(pre_map, unicode(base_url + li_line[0], 'utf-8'), unicode(li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=fun)


# 中国体彩网
def zhtc_gpdfdt_parser():
    url = 'http://www.lottery.gov.cn/gpgddt/index.html'
    zhtc_gp_parser(url, zhtc_gpdfdt_parser)


# 中国体彩网
def zhtc_gpgg_parser():
    url = 'http://www.lottery.gov.cn/gptzgg/index.html'
    zhtc_gp_parser(url, zhtc_gpgg_parser)


# 山东体彩网
def sdtc_tcgz_parser():
    try:
        base_name = u'山东体彩'
        base_url = 'http://www.sdticai.com/'
        url = 'http://www.sdticai.com/news.asp?dlei=4'
        td_reg = u'<td.*?class="dbk".*?href="(.*?)".*?<span.*?">(.*?)<\/span>.*?<\/td>[\s\S]*?<td.*?class="dbk".*?">\[(.*?)\]<\/span><\/td>'
        content = url_get(url, encoding='gb2312')
        td_group = re.findall(td_reg, content, re.S | re.M)
        if not td_group:
            trace.append(url + ":不匹配")
        pre_map = {}
        for li_line in td_group:
            pre_save(pre_map, unicode(base_url + li_line[0], 'utf-8'), unicode(li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=sdtc_tcgz_parser)


# 广东体彩网
def gdlottery(url, gd_func):
    try:
        base_name = u'广东体彩'
        base_url = 'http://www.gdlottery.cn'
        td_reg = u'<span.*?class=\"r\">\((.*?)\s.*?\)<\/span>[\s\S]*?<a.*?href=\"(.*?)\".*?>(.*?)<\/a>'
        content = url_get(url)
        td_group = re.findall(td_reg, content, re.S | re.M)
        if not td_group:
            trace.append(url + ":不匹配")
        pre_map = {}
        for li_line in td_group:
            date = unicode(li_line[0], 'utf-8').replace(u"年", u"-").replace(u"月", u"-").replace(u"日", u"")
            pre_save(pre_map, unicode(base_url + li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), date, base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=gd_func)


def gdlottery_gg_parser():
    gd_gg = 'http://www.gdlottery.cn/html/gonggao/index.html'
    gdlottery(gd_gg, gdlottery_gg_parser)


def gdlottery_xw_parser():
    gd_xw = 'http://www.gdlottery.cn/html/ticaidongtai/'
    gdlottery(gd_xw, gdlottery_xw_parser)


# 广西体彩网
def gxlottery_parser():
    try:
        base_name = u'广西体彩'
        base_url = 'http://www.lottery.gx.cn'
        url = 'http://www.lottery.gx.cn/gonggao/guanfang/'
        td_reg = u'<div class=\"dl\">.*?href="(.*?)\".*?<b>(.*?)<\/b>.*?<\/div>[\s\S]*?<span class=\"dr\">(.*?)<\/span><\/li>'
        content = url_get(url)
        td_group = re.findall(td_reg, content, re.S | re.M)
        if not td_group:
            trace.append(url + ":不匹配")
        pre_map = {}
        for li_line in td_group:
            date = unicode(li_line[2], 'utf-8').replace(u"年", u"-").replace(u"月", u"-").replace(u"日", u"")
            pre_save(pre_map, unicode(base_url + li_line[0], 'utf-8'), unicode(li_line[1], 'utf-8'), date, base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=gxlottery_parser)


# 山东福彩网
def sdcp_parser():
    try:
        base_name = u'山东福彩'
        base_url = 'http://www.sdcp.cn/fbgg/'
        reg = u'<li.*?\"clearFix\">[\s\S]*?<h3.*?href=\"\.\/(.*?)\".*?_blank\">(.*?)<\/a>[\s\S]*?<span>(.*?)<\/span>[\s\S]*?<\/li>'
        content = url_get(base_url)
        group = re.findall(reg, content, re.S | re.M)
        if not group:
            trace.append(base_url + ":不匹配")
        pre_map = {}
        for line in group:
            pre_save(pre_map, unicode(base_url + line[0], 'utf-8'), unicode(line[1], 'utf-8'), unicode(line[2], 'utf-8'), base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=sdcp_parser)


# 江西福彩网
def jxfc_parser():
    try:
        base_name = u'江西福彩'
        base_url = 'http://www.jxfczx.cn'
        url = 'http://www.jxfczx.cn/news/NewsListLower.aspx?TypeId=31'
        reg = u'<td.*?newslist_title_table[\s\S]*?<a.*?href=\'\.\.(.*?)\'.*?>[\s]*(.*?)<\/a>[\s\S]*?<\/td>[\s\S]*?<span.*?newslist_timeto_text.*?<\/span>.*?<span.*?>\s*(.*?)<\/span>'
        content = url_get(url)
        group = re.findall(reg, content, re.S | re.M)
        if not group:
            trace.append(url + ":不匹配")
        pre_map = {}
        for line in group:
            pre_save(pre_map, unicode(base_url + line[0], 'utf-8'), unicode(line[1], 'utf-8'), unicode(line[2], 'utf-8'), base_name)
        filter_news(pre_map, base_name)
        news_save(pre_map)
    except :
        log_record(base_name=base_name, func=jxfc_parser)


def pre_save(pre_map, url, title, date, regional):
    md5 = hashlib.md5()
    key = url + title + date
    md5.update(key.encode('utf-8'))
    md5_digest = md5.hexdigest()
    pre_map[md5_digest] = {'key': md5_digest, 'url': url, 'title': title, 'date': date, 'is_warning': False, 'regional': regional}


def filter_news(pre_map, site_name):
    if not pre_map:
        trace.append(site_name + u':未获取到数据,请查看脚本代码\n')
        return
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
    if db_news.count() == 0 and not trace:
        return
    for doc in db_news:
        update_key.append(doc['key'])
        content += (u"<li>[%s]<a href=\"%s\">%s</a>(%s)</li>" % (doc['regional'], doc['url'], doc['title'], doc['date']))
    trace_m = u''
    if trace:
        for m in trace:
            trace_m += m
    if not content:
        content = u'所有最新新闻都已推送,请查看之前的邮件'
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
    try:
        urllib2.urlopen(request, urllib.urlencode(data))
    except:
        return
    if update_key:
        collection.update_many({"key": {"$in": update_key}}, {"$set": {"is_warning": True}})


def parser():
    zhcw_zygg_parser()
    zhcw_dsfc_parser()
    zhtc_zzgg_parser()
    sdtc_tcgz_parser()
    gdlottery_gg_parser()
    zhtc_gpgg_parser()
    gdlottery_xw_parser()
    gxlottery_parser()
    zhtc_gpdfdt_parser()
    cwl_parser()
    cwl_scdt_parser()
    cwl_fcyw_parser()
    sdcp_parser()
    jxfc_parser()


def main():
    parser()
    send_mail()

if __name__ == "__main__":
    main()

