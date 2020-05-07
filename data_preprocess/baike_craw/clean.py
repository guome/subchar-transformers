#! -*- coding:utf-8 -*-
import copy
import json
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

tasks.delete_many({})