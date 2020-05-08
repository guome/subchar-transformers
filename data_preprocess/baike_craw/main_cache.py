#! -*- coding:utf-8 -*-
import copy
import json
import multiprocessing
import os
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

unescape = html.unescape  # 用来实现对HTML字符的转移

db = pymongo.MongoClient("mongodb://127.0.0.1:27017/")["baidu_baike"]
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
    tasks.insert_one({'url': 'https://baike.baidu.com/item/%E7%A7%91%E5%AD%A6?force=1'})
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
    # print("para.contents: ", para.contents)
    for content in para.contents:
        # print(content)
        # if content.find("sup"):
        #     continue
        # if content.find("div"):
        #     continue
        # if content.find("img"):
        #     continue
        # if content.find("a"):
        #     continue

        # print(content)
        # print(content.string)
        string = content.string
        # print(string)
        if string:
            text += string.strip()

    text = re.sub("\[[1-9]{1,3}\]", "", text)
    # print("para text: ", text)
    return text





def main():
    global count
    global tmp_items_global
    global tmp_tasks_global
    global tmp_tasks_global_list

    tmp_items_global = {}
    for item in items.find({}):
        tmp_items_global[item["url"]] = 1
    print("tmp_items_global: ", len(tmp_items_global))


    tmp_tasks_global = {}
    for task in tasks.find({}):
        tmp_tasks_global[task["url"]] = 1
    print("tmp_tasks_global: ", len(tmp_tasks_global))
    tmp_tasks_global_list = list(tmp_tasks_global.keys())
    # time.sleep(0.3)

    time_string = str(time.time())
    jsonl_dir = "data_preprocess/baike_craw/data/%s.jsonl" % (time_string)



    items_tmp = {}

    with open(jsonl_dir, "w", encoding="utf-8") as f:
        while len(tmp_tasks_global_list) > 0:

            print("tmp_tasks_global_list: ", len(tmp_tasks_global_list))
            print("items_tmp: ", len(items_tmp))

            url = tmp_tasks_global_list.pop(0)  # 取出一个url，并且在队列中删除掉
            # print(url)

            t0 = time.time()
            # if items.find_one({'url': url}):
            #     continue

            # print(url)
            if url in items_tmp:
                continue
            if url in tmp_items_global:
                continue

            t1 = time.time()
            print("verifying url cost: ", t1 - t0)

            # print(url)
            t0 = time.time()
            sess = rq.get(url, headers=DEFAULT_REQUEST_HEADERS)
            web = sess.content.decode('utf-8', 'ignore')

            t1 = time.time()
            print("requesting url cost: ", t1 - t0)

            # print(web)
            print("页面不存在: ", "您所访问的页面不存在" in web)

            if "您所访问的页面不存在" in web:
                continue

            t0 = time.time()
            urls = re.findall(u'target=.*? href="(/item/.*?)"', web)  # 查找所有站内链接
            # print(urls)
            # print(len(urls))
            urls_new = []
            for u in urls:
                try:
                    u = unquote(str(u)).decode('utf-8')
                except:
                    pass

                u = 'https://baike.baidu.com' + u
                u = clean_url(u)
                # print(u)
                # if items.count_documents({'url': u}) == 0:  # 把还没有队列过的链接加入队列
                    # tasks.update_one({'url': u}, {'$set': {'url': u}}, upsert=True)

                if u not in tmp_tasks_global:
                    urls_new.append(u)
                    tmp_tasks_global[u] = 1
                    tmp_tasks_global_list.append(u)

                # item name
                u_0 = u.replace("https://baike.baidu.com/item/", "")
                if "/" in u_0:
                    item_name = u_0.split("/")[0]
                    u1 = 'https://baike.baidu.com/item/%s?force=1' % item_name
                    # print("u1: ", u1)
                    # if not items.count_documents({'url': u1}) == 0:  # 把还没有队列过的链接加入队列
                        # tasks.update({'url': u1}, {'$set': {'url': u1}}, upsert=True)

                    if u1 not in tmp_tasks_global:
                        urls_new.append(u1)
                        tmp_tasks_global[u1] = 1
                        tmp_tasks_global_list.append(u1)

            urls_new = list(set(urls_new))
            if url in urls_new:
                urls_new.pop(urls_new.index(url))
            # urls_new = [{"url": url} for url in urls_new]
            # tasks.update_many({'url': u1}, {'$set': {'url': u1}}, upsert=True)
            if len(urls_new) > 0:
                urls_new = [{"url": url} for url in urls_new]
                tasks.insert_many(urls_new)

            t1 = time.time()
            print("updating tasks queue costs: ", t1 - t0)

            if not re.search("这是一个.*?多义词.*?，请在下列.*?义项.*?上选择浏览", web):

                # 类名为xxx而且文本内容为hahaha的div
                soup = BeautifulSoup(web, "html.parser")

                # "main-content"
                content_tree = []
                main_content = soup.find("div", class_="main-content")

                # title
                # title = main_content.find("dl", class_="lemmaWgt-lemmaTitle lemmaWgt-lemmaTitle-")
                # title = title.find("dd", class_="lemmaWgt-lemmaTitle-title")
                # title = title.find("h1")
                # print(title)
                title = re.findall(u'<title>(.*?)_百度百科</title>', web)[0]
                # print(title)

                # summary
                summary_texts = []
                # if soup.find("div", class_="lemmaWgt-lemmaSummary lemmaWgt-lemmaSummary-light"):
                #     summary_light = soup.find("div", class_="lemmaWgt-lemmaSummary lemmaWgt-lemmaSummary-light")
                #     print(summary_light)
                # else:
                summary = soup.find("div", class_="lemma-summary")
                if summary:
                    # print(summary.text)
                    # summary_texts = []
                    for para in summary.find_all("div", class_="para"):
                        # continue
                        # # print(para.contents)
                        # # print(type(para.contents[0]))
                        para_text = process_para(para)
                        # # print(para_text)
                        summary_texts.append(para_text)

                # 正文内容
                texts = []
                for content in main_content.find_all("div"):
                    # if isinstance(content, NavigableString):
                    # print("content type: ", type(content))
                    # print("content: ", content)
                    if isinstance(content, Tag):
                        class_ = content.attrs.get("class")
                        # print("content class_: ", class_)

                        if class_:
                            # print(class_)
                            if "para" in class_ or "para-title" in class_:
                                # 1) para-title
                                if "para-title" in class_ and 'level-2' in class_:
                                    title_ = None
                                    content_ = content.find("h2", class_="title-text")
                                    if not content_:
                                        content_ = content.find("span")
                                        # print(content_.string)
                                        title_ = content_.string
                                    if content_:
                                        for con in content_.contents:
                                            if con.find("span"):
                                                continue
                                            # print(con.string)
                                            # texts.append(content_.string)
                                            title_ = con.string

                                    if title_:
                                        texts.append(title_)

                                elif "para-title" in class_ and 'level-3' in class_:
                                    title_ = None
                                    content_ = content.find("h3", class_="title-text")
                                    if not content_:
                                        content_ = content.find("span")
                                        # print(content_.string)
                                        title_ = content_.string
                                    if content_:
                                        for con in content_.contents:
                                            if con.find("span"):
                                                continue
                                            # print(con.string)
                                            # texts.append(content_.string)
                                            title_ = con.string

                                    if title_:
                                        # print("para title_: ", title_)
                                        texts.append(title_)
                                elif "para" in class_:
                                    # print("content: ", content.contents)
                                    # para = content.find("div", class_="para")
                                    para_text = process_para(content)
                                    # print("para_text: ", para_text)
                                    if para_text:
                                        texts.append(para_text)

                texts_copy = texts.copy()
                texts = []
                for sent in summary_texts:
                    if sent not in texts:
                        texts.append(sent)
                for sent in texts_copy:
                    if sent not in texts:
                        texts.append(sent)

                if len(texts) > 0:
                    # items.update(
                    #     {'url': url},
                    #     {
                    #         '$set': {
                    #             'url': url
                    #         }
                    #     },
                    #     upsert=True
                    # )
                    items_tmp.update(
                        {url: 1}
                    )
                    tmp_items_global.update(
                        {url: 1}
                    )

                    samp = {
                        'url': url,
                        'title': title,
                        'summary_texts': summary_texts,
                        'text': texts
                    }
                    f.write(json.dumps(samp, ensure_ascii=False) + "\n")

                    count += 1
                    print('%s, 爬取《%s》，URL: %s, 已经爬取%s' % (datetime.datetime.now(), title, url, count))

                else:
                    print("blank page: ", url)

            else:
                print("多义词url: ", url)

            if len(items_tmp) > 45:
                items_tmp_samples = [{"url": url} for url in items_tmp.keys()]
                items.insert_many(items_tmp_samples)
                items_tmp = {}

                print("tmp_items_global: ", len(tmp_items_global))



if __name__ == "__main__":
    # items_global = []
    # for key in tmp_items_global.keys():
    #     task_ = {"url": key}
    #     items_global.append(task_)
    # items.delete_many({})
    # items.insert_many(items_global)

    # tasks_tmp = []
    # if tasks.count_documents(filter={}) > 0:
    #     for i in range(10):
    #         url = tasks.find_one_and_delete({})['url']
    #         tasks_tmp.append(url)
    # # print(tasks_tmp)

    num_processes = 8
    jobs = []
    for i in range(num_processes):
        # job = multiprocessing.Process(target=main, args=())
        job = multiprocessing.Process(target=main, args=())
        jobs.append(job)
        job.start()
    for job in jobs:
        job.join()

    # main()


    # TODO: 区分到底是词条具体信息页面，还是一词多义页面