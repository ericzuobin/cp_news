#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/13 下午3:17
# @Author  : Sahinn
# @File    : cp_news.py
import re
import urllib2


def url_get(url, timeout=30):
    i_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                 "Referer": 'http://www.baidu.com'}
    req = urllib2.Request(url, headers=i_headers)
    result = urllib2.urlopen(req, timeout=timeout)
    content = result.read()
    return content


def zhcw_zygg_parser():
    base_url = 'http://www.zhcw.com'
    url = 'http://www.zhcw.com/xinwen/zhongyaogonggao/'
    ul_reg = u'<ul class="Nlistul">[\s\S]*?<\/ul>'
    li_reg = u'<li><span class="Nlink">.*?href="(.*?)".*?>(.*?)<\/a>[\s\S]*?Ntime">(.*?)</span><\/li>'
    content = url_get(url)
    ul_group = re.findall(ul_reg, content, re.S | re.M)
    li_group = re.findall(li_reg, ul_group[0], re.S | re.M)
    for li_line in li_group:
        print unicode(base_url + li_line[0], 'utf-8'), unicode(li_line[1], 'utf-8'), unicode(li_line[2], 'utf-8')
        check_save()


def check_save():
    pass


def send_mail():
    pass


def main():
    zhcw_zygg_parser()
    send_mail()


if __name__ == "__main__":
    main()

