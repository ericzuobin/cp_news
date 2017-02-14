#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/13 下午3:17
# @Author  : Sahinn
# @File    : cp_news.py
# use cp_news
# db.createCollection("news",{size:4096,max:4096})
import re
import urllib2
import traceback
import hashlib
from pymongo import MongoClient

client = MongoClient('172.16.22.251', 27017)
db = client.cp_news
collection = db['news']

log_path = '/Users/sahinn/Documents/workspace_py/cp_news/cp_news.log'


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
    f = open(log_path, 'a')
    traceback.print_exc(file=f)
    f.flush()
    f.close()


def zhcw_zygg_parser():
    try:
        base_url = 'http://www.zhcw.com'
        url = 'http://www.zhcw.com/xinwen/zhongyaogonggao/'
        ul_reg = u'<ul class="Nlistul">[\s\S]*?<\/ul>'
        li_reg = u'<li><span class="Nlink">.*?href="(.*?)".*?>(.*?)<\/a>[\s\S]*?Ntime">(.*?)</span><\/li>'
        content = url_get(url)
        ul_group = re.findall(ul_reg, content, re.S | re.M)
        li_group = re.findall(li_reg, ul_group[0], re.S | re.M)
        for li_line in li_group:
            check_save(unicode(base_url + li_line[0], 'utf-8'), unicode(li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'))
    except :
        log_record()


def zhtc_zzgg_parser():
    try:
        base_url = 'http://www.lottery.gov.cn'
        url = 'http://www.lottery.gov.cn/tzgg/index.html'
        ul_reg = u'<div class="main_l">[\s\S]*?<\/div>'
        li_reg = u'<li><span>\((.*?)\)<\/span><a.*?<\/a><a.*?href="(.*?)">(.*?)<\/a><\/li>'
        content = url_get(url)
        ul_group = re.findall(ul_reg, content, re.S | re.M)
        li_group = re.findall(li_reg, ul_group[0], re.S | re.M)
        for li_line in li_group:
            check_save(unicode(base_url + li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'), unicode(li_line[0], 'utf-8'))
    except :
        log_record()


def sdtc_tcgz_parser():
    try:
        base_url = 'http://www.sdticai.com/'
        url = 'http://www.sdticai.com/news.asp?dlei=4'
        td_reg = u'<td.*?class="dbk".*?href="(.*?)".*?<span.*?">(.*?)<\/span>.*?<\/td>[\s\S]*?<td.*?class="dbk".*?">\[(.*?)\]<\/span><\/td>'
        content = url_get(url, encoding='gb2312')
        td_group = re.findall(td_reg, content, re.S | re.M)
        for li_line in td_group:
            check_save(unicode(base_url + li_line[0], 'utf-8'), unicode(li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8'))
    except :
        log_record()


def check_save(url, title, date):
    md5 = hashlib.md5()
    key = url + title + date
    md5.update(key.encode('utf-8'))
    md5_digest = md5.hexdigest()
    print url, title, date
    print md5_digest


def send_mail():
    pass


def main():
    print collection.find_one()
    # zhcw_zygg_parser()
    # zhtc_zzgg_parser()
    # sdtc_tcgz_parser()
    send_mail()


if __name__ == "__main__":
    main()

