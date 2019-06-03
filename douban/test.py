#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/15 16:43
# @Author  : xule
# @File    : test.py


import requests
import re
from bs4 import BeautifulSoup
import chardet
import lxml

text = '''
<div class="pl2">
<a class="" href="https://movie.douban.com/subject/1291843/">
                        黑客帝国
                        / <span style="font-size:13px;">廿二世纪杀人网络(港) / 骇客任务(台)</span>
</a>
<span style="font-size: 13px; padding-left: 3px; color: #00A65F;">[可播放]</span>
<p class="pl">1999-03-31(美国) / 基努·里维斯 / 凯瑞-安·莫斯 / 劳伦斯·菲什伯恩 / 雨果·维文 / 格洛丽亚·福斯特 / 乔·潘托里亚诺 / 马库斯·钟 / 朱利安·阿拉汗加 / 马特·多兰 / 比尔·扬 / 罗温·维特 / 童自荣 / 沈晓谦 / 户田惠子 / 阿达·尼科德莫...</p>
<div class="star clearfix">
<span class="allstar45"></span>
<span class="rating_nums">8.9</span>
<span class="pl">(402489人评价)</span>
</div>
</div>
'''
'''
    Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0
'''
import os

def fetch_proxy(num):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    url_pattern = 'https://www.xicidaili.com/nn/{}'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
    }
    fp = open('ip.txt', 'a+', encoding='utf-8')
    for i in range(1, num+1):
        url = url_pattern.format(num)
        response = requests.get(url=url, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
        conts = soup.find_all('tr', 'odd')
        for cont in conts:
            ip = cont.find_all('td')[1].get_text()
            port = cont.find_all('td')[2].get_text()
            fp.write('{}\t{}\n'.format(ip, port))
    fp.close()


def test_proxy():
    N = 1
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    url = 'https://www.baidu.com'
    fp = open('ip.txt', 'r')
    ips = fp.readlines()
    proxys = list()
    for p in ips:
        ip = p.strip('\n').split('\t')
        proxy = 'http://' + ip[0] + ':' + ip[1]
        proxies = {'proxy': proxy}
        proxys.append(proxies)
    for pro in proxys:
        try:
            s = requests.get(url, proxies=pro)
            print('第{}个ip：{} 状态{}'.format(N, pro, s.status_code))
        except Exception as e:
            print(e)
        N += 1


# fetch_proxy(5)
# test_proxy()


def proxypool():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    url = 'https://www.baidu.com'
    fp = open('ip.txt', 'r')
    ips = fp.readlines()
    proxys = list()
    for p in ips:
        ip = p.strip('\n').split('\t')
        proxy = 'http://' + ip[0] + ':' + ip[1]
        proxies = {'proxy': proxy}
        proxys.append(proxies)
    return proxys


# proxypool()

import requests
import json
import time
import simplejson

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0'
}
base_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=38975978198&' \
           'spuId=279689783&sellerId=92889104&order=3&callback=jsonp698'
#在base_url后面添加&currentPage=1就可以访问不同页码的评论

for i in range(2, 98, 1):
    url = base_url + '&currentPage=%s' % str(i)
    #将响应内容的文本取出
    tb_req = requests.get(base_url, headers=headers).text[12:-1]
    print(tb_req)
    print(type(tb_req))
    #将str格式的文本格式化为字典
    tb_dict = json.loads(tb_req)

    #编码： 将字典内容转化为json格式对象
    tb_json = json.dumps(tb_dict, indent=2)   #indent参数为缩紧，这样打印出来是树形json结构，方便直观
    #print(type(tb_json))

    #print(tb_json)
    #解码： 将json格式字符串转化为python对象
    review_j = json.loads(tb_json)
    for p in range(1, 20, 1):
        print(review_j["rateDetail"]["rateList"][p]['rateContent'])
    time.sleep(1)