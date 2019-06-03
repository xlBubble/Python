#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/16 17:06
# @Author  : xule
# @File    : huikan.py

import os
import time
import requests
from bs4 import BeautifulSoup
from baidupcsapi import PCS

def fetch_journal(pages,dir_path):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    url_pattern = 'https://tieba.baidu.com/p/4383495009?see_lz=1&pn={}'
    header = {
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    proxy = []
    fp = open('herfs.txt', 'a+', encoding='utf-8')
    num = 0
    print('开始爬取...')
    for page in range(1, pages+1):
        url = url_pattern.format(page)
        response = requests.get(url=url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        conts = soup.find_all('div', 'l_post l_post_bright j_l_post clearfix')
        for cont in conts:
            herfs = cont.find_all('a', 'j-no-opener-url')
            for herf in herfs:
                herf = herf.string
                fp.write("{}\n".format(herf))
            covers = cont.find_all('img', 'BDE_Image')
            for cover in covers:
                cover_herf = cover.get('src')
                cover_resp = requests.get(cover_herf, header).content
                with (open('{}/{}'.format(dir_path, 'img'+str(num)+'.jpg'), 'wb')) as f:
                    f.write(cover_resp)
                num += 1
        print('共有{}页，已爬{}页'.format(pages, page))
    fp.close()




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    dir_path = os.getcwd() + '/' + 'journal'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    start = time.time()
    fetch_journal(5, dir_path)
    end = time.time()
    time_diff = end - start
    print('总耗时: {}s'.format(time_diff))