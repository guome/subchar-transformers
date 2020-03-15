#! -*- coding:utf-8 -*-
from urllib.parse import unquote, urlparse, urlunparse  # 用来对URL进行解码  # 对长的URL进行拆分

import requests as rq
import re
import time
import datetime
from multiprocessing.dummy import Pool
import pymongo  # 使用数据库负责存取
from html.parser import HTMLParser
import html

unescape = html.unescape  # 用来实现对HTML字符的转移

db = pymongo.MongoClient("mongodb://127.0.0.1:27017/")["baidu_baike"]
print(db)


# tasks = db["tasks"]  # 将队列存于数据库中
# items = db["items"]  # 存放结果
#
# tasks.create_index([('url', 'hashed')])  # 建立索引，保证查询速度
# items.create_index([('url', 'hashed')])
#
# count = items.count()  # 已爬取页面总数
# if tasks.count() == 0:  # 如果队列为空，就把该页面作为初始页面，这个页面要尽可能多超链接
#     tasks.insert({'url': u'http://baike.baidu.com/item/科学'})
#
# url_split_re = re.compile('&|\+')
#
#
# def clean_url(url):
#     url = urlparse(url)
#     return url_split_re.split(urlunparse((url.scheme, url.netloc, url.path, '', '', '')))[0]
#
#
# def main():
#     global count
#     while True:
#         url = tasks.find_one_and_delete({})['url']  # 取出一个url，并且在队列中删除掉
#         sess = rq.get(url)
#         web = sess.content.decode('utf-8', 'ignore')
#         urls = re.findall(u'href="(/item/.*?)"', web)  # 查找所有站内链接
#         for u in urls:
#             try:
#                 u = unquote(str(u)).decode('utf-8')
#             except:
#                 pass
#             u = 'http://baike.baidu.com' + u
#             u = clean_url(u)
#             if not items.find_one({'url': u}):  # 把还没有队列过的链接加入队列
#                 tasks.update({'url': u}, {'$set': {'url': u}}, upsert=True)
#
#         text = re.findall('<div class="content">([\s\S]*?)<div class="content">', web)
#         # 爬取我们所需要的信息，需要正则表达式知识来根据网页源代码而写
#
#         if text:
#             text = ' '.join([re.sub(u'[ \n\r\t\u3000]+', ' ', re.sub(u'<.*?>|\xa0', ' ', unescape(t))).strip() for t in
#                              text])    # 对爬取的结果做一些简单的处理
#             title = re.findall(u'<title>(.*?)_百度百科</title>', web)[0]
#             items.update({'url': url}, {'$set': {'url': url, 'title': title, 'text': text}}, upsert=True)
#             count += 1
#             print('%s, 爬取《%s》，URL: %s, 已经爬取%s' % (datetime.datetime.now(), title, url, count))
#
#
# pool = Pool(4, main)  # 多线程爬取，4是线程数
# time.sleep(60)
# while tasks.count() > 0:
#     time.sleep(60)
#
# pool.terminate()
