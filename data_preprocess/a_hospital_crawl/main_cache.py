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

db = pymongo.MongoClient("mongodb://127.0.0.1:27017/")["a_hospital"]
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
            {'url': 'http://www.a-hospital.com/w/%E6%B2%BB%E7%96%97%E8%85%B9%E7%97%9B%E5%92%8C%E8%85%B9%E6%B3%BB%E7%9A%84%E8%8D%AF%E5%93%81%E5%88%97%E8%A1%A8', "processor_id": 0},
        ]
    )
print(tasks.count_documents(filter={}))

DEFAULT_REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
				   'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}

USER_AGENTS = [

    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",

    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",

    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",

    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",

    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",

    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",

    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",

    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"

]

IPS = [
    "218.241.219.84:3128",
]



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

    sleep_time = random.uniform(1, 5)

    time.sleep(sleep_time)

    time_string = str(time.time())
    jsonl_dir = "data_preprocess/a_hospital_crawl/data/%s.jsonl" % (time_string)

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
                print("already crawled url: ", url)
                continue

            t1 = time.time()
            print("verifying url cost: ", t1 - t0)

            # print(url)
            t0 = time.time()

            web = None

            ip = random.choice(IPS)
            proxies = {
                "http": "http://%s" % ip,
            }

            try:
                user_agent = random.choice(USER_AGENTS)
                sess = rq.get(
                    url,
                    headers={'User-Agent':user_agent},
                    proxies=proxies,
                    timeout=5,
                )

                web = sess.content.decode('utf-8', 'ignore')
            except Exception as e:
                print(e)

            if not web:
                continue

            t1 = time.time()
            print("requesting url cost: ", t1 - t0)

            if "页面不存在" in web:
                continue

            t0 = time.time()
            # href="/w/%E8%83%86%E7%BB%8F"
            urls = re.findall(u'href="(/w/.*?)" title=".*?"', web)  # 查找所有站内链接

            urls_new = []
            for u in urls:
                # print(u)
                try:
                    u = unquote(str(u)).decode('utf-8')
                except:
                    pass

                u = 'http://www.a-hospital.com' + u
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

                    tasks.update(
                        {'url': u},
                        {
                            '$set': u_task
                        },
                        upsert=True
                    )

            t1 = time.time()
            print("updating tasks queue costs: ", t1 - t0)

            if not re.search("这是一个.*?多义词.*?，请在下列.*?义项.*?上选择浏览", web):

                doc = pq(web.replace('xmlns="http://www.w3.org/1999/xhtml"', ''))
                title = doc("#content h1").text()
                content = doc("#bodyContent").html()
                print("title: ", title)
                # print("content: ", content)

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
    main(0)

    # num_processes = 8
    # jobs = []
    # for i in range(num_processes):
    #     # job = multiprocessing.Process(target=main, args=())
    #     job = multiprocessing.Process(target=main, args=(i, ))
    #     jobs.append(job)
    #     job.start()
    # # for job in jobs:
    # #     job.join()
