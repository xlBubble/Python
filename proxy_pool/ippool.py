#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/19 13:57
# @Author  : xule
# @File    : ippool.py
# @Usage    : 获取1000个代理ip，并检测有效性
'''
    学习参考：https://mp.weixin.qq.com/s/0foxdcRj0_k5r2GyGQwjsA
'''

import os
from bs4 import BeautifulSoup
# import requests
from urllib import request, response
import random
from fake_useragent import UserAgent
from lxml import etree


def get_url(url):
    '''
    构造网站链接，网站http://www.xicidaili.com/nn/
    :return:
    '''
    url_list = []
    for i in range(1,100):
        url = url + str(1)
        url_list.append(url)
    return url_list


def get_header():
    '''
    自定义header库
    :return:
    '''
    headers =[
        "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
        "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
        "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
        "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
        "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
        "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)",
        "Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv:66.0) Gecko/20100101 Firefox/66.0",
        "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 73.0.3683.103 Safari / 537.36",
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
    ]
    return random.choice(headers)


def get_cont(url):
    '''
    获取网站内容，使用工具urllib
    :return:
    '''
    ua = UserAgent()  # 第三方header库
    header = {
        'host': 'www.xicidaili.com',
        'User-Agent': ua.random
    }
    req = request.Request(url=url, headers=header)
    resp = request.urlopen(req)
    cont = resp.read()
    return cont.decode('utf-8')


def get_ip(cont):
    html = etree.HTML(cont)
    print(html)
    print(type(html))
    result = etree.tostring(html)
    print(result.decode("utf-8"))

get_ip(get_cont('http://www.xicidaili.com/nn/2'))