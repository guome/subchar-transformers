#! -*- coding:utf-8 -*-
import copy
import json
import multiprocessing
import os
import random
from urllib.parse import unquote, urlparse, urlunparse  # 用来对URL进行解码  # 对长的URL进行拆分

import requests as rq
import re
import time
import datetime
from multiprocessing.dummy import Pool
# from multiprocessing import Pool
import pymongo  # 使用数据库负责存取
from html.parser import HTMLParser
import html
from bs4 import BeautifulSoup, NavigableString, Tag
from pyquery import PyQuery as pq

unescape = html.unescape  # 用来实现对HTML字符的转移

db = pymongo.MongoClient("mongodb://127.0.0.1:27017/")["wiki8"]
print(db)


tasks = db["tasks"]  # 将队列存于数据库中
# tasks_crawled = db["tasks_crawled"]  # 爬取了的url存在这里
items = db["items"]  # 存放结果
print(tasks)
# print(tasks_crawled)
print(items)

# items.delete_many({})

tasks.create_index([('url', 'hashed')])  # 建立索引，保证查询速度
# tasks_crawled.create_index([('url', 'hashed')])  # 建立索引，保证查询速度
items.create_index([('url', 'hashed')])

count = items.count_documents(filter={})  # 已爬取页面总数
print(count)
if tasks.count_documents(filter={}) == 0:  # 如果队列为空，就把该页面作为初始页面，这个页面要尽可能多超链接
    tasks.insert_many(
        [
            {'url': 'https://www.wiki8.com/tangniaobing_22286/', "processor_id": 0},
            {'url': 'https://www.wiki8.com/suanzhongdu_37047/', "processor_id": 0},
            {'url': 'https://www.wiki8.com/shuiyangsuan_24419/', "processor_id": 0},
            {'url': 'https://www.wiki8.com/jingziranqiangdaoneijingshoushu_48604/', "processor_id": 0},
            {'url': 'https://www.wiki8.com/shoushudianjichanpinzhucejishushenchazhidaoyuanze_124047/', "processor_id": 0},
        ]
    )
print(tasks.count_documents(filter={}))

DEFAULT_REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
				   'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}


url_split_re = re.compile('&|\+')


def clean_url(url):
    url = urlparse(url)
    return url_split_re.split(urlunparse((url.scheme, url.netloc, url.path, '', '', '')))[0]


def process_para(para):
    # 提取一个 "para" 中的文字
    text = ""
    for content in para.contents:

        string = content.string
        if string:
            text += string.strip()

    text = re.sub("\[[1-9]{1,3}\]", "", text)
    # print("para text: ", text)
    return text


tmp_tasks_global = {}
tmp_tasks_global_list = []
for task_ in tasks.find({}):
    # tmp_tasks_global[task_["url"]] = 1
    tmp_tasks_global[task_["url"]] = task_["processor_id"]
    # tmp_tasks_global_list.append(task_)
print("tmp_tasks_global: ", len(tmp_tasks_global))


def main(proc_idx):
    global count
    global tmp_tasks_global

    time.sleep(0.2)

    time_string = str(time.time())
    jsonl_dir = "data_preprocess/wiki8_crawl/data/%s.jsonl" % (time_string)

    with open(jsonl_dir, "w", encoding="utf-8") as f:
        while True:

            url_task = None
            try:
                url_task = tasks.find_one_and_delete({})
            except Exception as e:
                print("exception: ", e)

            if not url_task:
                break

            url = url_task["url"]

            t0 = time.time()

            if items.find_one({'url': url}):
                tasks.delete_many({"url": url})
                continue

            t1 = time.time()
            print("verifying url cost: ", t1 - t0)

            # print(url)
            t0 = time.time()
            sess = rq.get(url, headers=DEFAULT_REQUEST_HEADERS)
            web = sess.content.decode('utf-8', 'ignore')

            t1 = time.time()
            print("requesting url cost: ", t1 - t0)

            if "您所访问的页面不存在" in web:
                continue

            t0 = time.time()
            urls = re.findall(u'title=".*?" href="(/.*?/)" rel="summary"', web)  # 查找所有站内链接

            urls_new = []
            for u in urls:
                try:
                    u = unquote(str(u)).decode('utf-8')
                except:
                    pass

                u = 'https://www.wiki8.com' + u
                u = clean_url(u)
                # print(u)

                urls_new.append(u)

            urls_new = list(set(urls_new))
            if url in urls_new:
                urls_new.pop(urls_new.index(url))
            # urls_new = [{"url": url} for url in urls_new]
            # tasks.update_many({'url': u1}, {'$set': {'url': u1}}, upsert=True)
            print("new urls: ", len(urls_new))

            if len(urls_new) > 0:
                # print("new urls: ", len(urls_new))
                url_tasks = []
                for u in urls_new:

                    if u in tmp_tasks_global:
                        continue

                    processor_asigned = random.choice(list(range(8)))
                    u_task = {
                        "url": u,
                        "processor_id": processor_asigned,
                    }
                    url_tasks.append(
                        u_task
                    )
                    tmp_tasks_global[u] = processor_asigned
                    # tmp_tasks_global_list.append(u_task)

                    tasks.update(
                        {'url': u},
                        {
                            '$set': u_task
                        },
                        upsert=True
                    )

                # tasks.insert_many(url_tasks)

            t1 = time.time()
            print("updating tasks queue costs: ", t1 - t0)

            if not re.search("这是一个.*?多义词.*?，请在下列.*?义项.*?上选择浏览", web):

                doc = pq(web.replace('xmlns="http://www.w3.org/1999/xhtml"', ''))
                title = doc("#main h1").text()
                content = doc("#content").html()
                print("title: ", title)

                if title and content:
                    items.update(
                        {'url': url},
                        {
                            '$set': {
                                'url': url
                            }
                        },
                        upsert=True
                    )

                    samp = {
                        'url': url,
                        'title': title,
                        'content': content
                    }
                    f.write(json.dumps(samp, ensure_ascii=False) + "\n")

                    count += 1
                    print('%s, 爬取《%s》，URL: %s, 已经爬取%s' % (datetime.datetime.now(), title, url, count))

                else:
                    print("blank page: ", url)


if __name__ == "__main__":
    # main(0)

    num_processes = 8
    jobs = []
    for i in range(num_processes):
        # job = multiprocessing.Process(target=main, args=())
        job = multiprocessing.Process(target=main, args=(i, ))
        jobs.append(job)
        job.start()
    # for job in jobs:
    #     job.join()
