#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/27 下午1:31
# @Author  : Sahinn
# @File    : get_cpnews.py
import json
import urllib
import urllib2

import pymongo
from pymongo import MongoClient

mail_url = 'http://172.16.3.145:82/LeheQ'
client = MongoClient('172.16.3.251', 27017)
mail_reciever = 'sahinn@163.com'
db = client.cp_news
collection = db['news']


def send_mail():
    db_news = collection.find(projection={'_id': False}).sort('date', pymongo.DESCENDING).limit(20)
    content = u''
    for doc in db_news:
        content += (u"<li>[%s]<a href=\"%s\">%s</a>(%s)</li>" % (doc['regional'], doc['url'], doc['title'], doc['date']))

    html = u'''<html><head><meta http-equiv=Content-Type content=text/html; charset=utf-8></head><body>
    <h2>彩票新闻推送</h2>
    <ul>''' + content + u'''</ul></body></html>'''

    import datetime
    message = {"content": html, "encoding": "", "fromAddress": "qa@lecai.com", "fromDisplay": "", "htmlStyle": True, "mailType": "",
     "mailto": mail_reciever, "subject": datetime.datetime.now().strftime('%Y-%m-%d') + u"彩票新闻推送"}
    request = urllib2.Request(mail_url)
    message = json.dumps(message)
    data = {"q": "mailqueue", "p": "10001", "data": message, "datatype": 'json', "callback": ""}
    urllib2.urlopen(request, urllib.urlencode(data))

send_mail()
