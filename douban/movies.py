#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 9:37
# @Author  : xule
# @File    : movies.py

#/html/body/div[3]/div[1]/div/div[1]/div/div/div[1]/div[3]/a[99]/p/span[2]
# https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=%E7%A7%91%E5%B9%BB

import requests
import re
from bs4 import BeautifulSoup
import csv
import os
import time
import random


def get_movie(tag,pages,proxy_ips):
    '''
    :param tag:
    :param pages:
    :return:
    '''
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    url_pattern = 'https://movie.douban.com/tag/{}?start={}'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
    }
    csvfile = open('{}.csv'.format(tag), 'a+', newline='\n', encoding='utf-8')
    writer = csv.writer(csvfile)
    writer.writerow(('name', 'nation', 'score', 'peoples', 'date'))
    for page in range(0, pages*20, 20):
        url = url_pattern.format(tag, page)
        try:
            response = requests.get(url=url, headers=header, proxies=random.choice(proxy_ips))
            while response.status_code != 200:
                response = requests.get(url=url, headers=header, proxies=random.choice(proxy_ips))
            soup = BeautifulSoup(response.text, 'lxml')
            movies = soup.find_all('div', 'pl2')
            # print(movies)
            for movie in movies:
                movie = BeautifulSoup(str(movie), 'lxml')
                # 影片名
                # mov_name = movie.find(name='a')
                mov_name = movie.find(name='a').contents[0].split('\n')[1].strip()
                # print(mov_name)
                # 上映时间
                mov_date = movie.find(name='p').string.split(' ')[0][0:10]
                # 国家
                mov_nation = movie.find(name='p').string.split(' ')[0][11:-1]
                # 评分
                mov_star = movie.find(name='div', attrs='star clearfix')
                mov_score = mov_star.find(name='span', attrs='rating_nums').string
                # 评分人数
                temp = mov_star.find(name='span', attrs='pl').get_text()
                mov_peopels = re.search(r'\d+', temp).group()
                writer.writerow((mov_name, mov_nation, mov_score, mov_peopels,mov_date))
        except:
            pass
        print('共有{}页，已爬{}页'.format(pages, int(page/20)+1))
    csvfile.close()


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


def proxypool():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    fp = open('ip.txt', 'r')
    ips = fp.readlines()
    proxys = list()
    for p in ips:
        ip = p.strip('\n').split('\t')
        proxy = 'http://' + ip[0] + ':' + ip[1]
        proxies = {'proxy': proxy}
        proxys.append(proxies)
    fp.close()
    return proxys


if __name__ == "__main__":
    start = time.time()
    fetch_proxy(5)
    proxy_ips = proxypool()
    get_movie('悬疑', 20, proxy_ips)
    end = time.time()
    time_diff = end-start
    print('总耗时: {}s'.format(time_diff))