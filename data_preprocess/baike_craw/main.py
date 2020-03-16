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


tasks = db["tasks"]  # 将队列存于数据库中
items = db["items"]  # 存放结果
print(tasks)
print(items)

tasks.create_index([('url', 'hashed')])  # 建立索引，保证查询速度
items.create_index([('url', 'hashed')])

count = items.count_documents(filter={})  # 已爬取页面总数
print(count)
if tasks.count_documents(filter={}) == 0:  # 如果队列为空，就把该页面作为初始页面，这个页面要尽可能多超链接
    tasks.insert_one({'url': 'https://baike.baidu.com/item/%E7%A7%91%E5%AD%A6?force=1'})
print(tasks.count_documents(filter={}))

DEFAULT_REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
				   'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}



url_split_re = re.compile('&|\+')


def clean_url(url):
    url = urlparse(url)
    return url_split_re.split(urlunparse((url.scheme, url.netloc, url.path, '', '', '')))[0]


def main():
    global count
    while tasks.count_documents(filter={}) > 0:
        url = tasks.find_one_and_delete({})['url']  # 取出一个url，并且在队列中删除掉
        print(url)
        sess = rq.get(url, headers=DEFAULT_REQUEST_HEADERS)
        web = sess.content.decode('utf-8', 'ignore')
        # print(web)
        print("页面不存在: ", "您所访问的页面不存在" in web)

        if "您所访问的页面不存在" in web:
            continue

        urls = re.findall(u'target=.*? href="(/item/.*?)"', web)  # 查找所有站内链接
        # print(urls)
        # print(len(urls))
        for u in urls:
            try:
                u = unquote(str(u)).decode('utf-8')
            except:
                pass

            u = 'https://baike.baidu.com' + u
            u = clean_url(u)
            # print(u)
            if not items.find_one({'url': u}):  # 把还没有队列过的链接加入队列
                tasks.update({'url': u}, {'$set': {'url': u}}, upsert=True)

            # item name
            u_0 = u.replace("https://baike.baidu.com/item/", "")
            if "/" in u_0:
                item_name = u_0.split("/")[0]
                u1 = 'https://baike.baidu.com/item/%s?force=1' % item_name
                # print("u1: ", u1)
                if not items.find_one({'url': u1}):  # 把还没有队列过的链接加入队列
                    tasks.update({'url': u1}, {'$set': {'url': u1}}, upsert=True)

        # text = re.findall('<div class="content">([\s\S]*?)<div class="content">', web)
        # 爬取我们所需要的信息，需要正则表达式知识来根据网页源代码而写

        if web:
            # text = ' '.join([re.sub(u'[ \n\r\t\u3000]+', ' ', re.sub(u'<.*?>|\xa0', ' ', unescape(t))).strip() for t in
            #                  text])    # 对爬取的结果做一些简单的处理
            title = re.findall(u'<title>(.*?)_百度百科</title>', web)[0]
            items.update({'url': url}, {'$set': {'url': url, 'title': title, 'web_source_code': web}}, upsert=True)
            count += 1
            print('%s, 爬取《%s》，URL: %s, 已经爬取%s' % (datetime.datetime.now(), title, url, count))


pool = Pool(16, main)  # 多线程爬取，4是线程数
time.sleep(60)
while tasks.count() > 0:
    time.sleep(60)

pool.terminate()

# main()
