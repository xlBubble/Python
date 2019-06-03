#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/16 17:06
# @Author  : xule
# @File    : test.py
import requests
import re
import os
from bs4 import BeautifulSoup


'''
    https://pan.baidu.com/share/transfer?shareid=421578512&from=1532967721&channel=chunlei&web=1&app_id=250528&
    bdstoken=4fb993821b38c43a524a7ef3aedf2274&logid=MTU1NTU1MjcxODg4MTAuNTAzMzY3NDkxOTMyNzc3Mw==&clienttype=0
'''

# -*- coding:utf-8 -*-
import requests
import json
import time
import re
from selenium import webdriver


class BaiduYunTransfer:
    headers = None
    bdstoken = None

    def __init__(self, bduss, stoken, bdstoken):
        self.bdstoken = bdstoken
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '161',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'BDUSS=%s;STOKEN=%s;' % (bduss, stoken),
            'Host': 'pan.baidu.com',
            'Origin': 'https://pan.baidu.com',
            'Referer': 'https://pan.baidu.com/s/1dFKSuRn?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

    def transfer(self, share_id, uk, filelist_str, path_t_save):
        # 通用参数
        ondup = "newcopy"
        async = "1"
        channel = "chunlei"
        clienttype = "0"
        web = "1"
        app_id = "250528"
        logid = "MTU1NTU3NTMzMzIxMzAuOTA0MDE4OTI2NjMzODAzNg=="

        url_trans = "https://pan.baidu.com/share/transfer?shareid=%s" \
                    "&from=%s" \
                    "&ondup=%s" \
                    "&async=%s" \
                    "&bdstoken=%s" \
                    "&channel=%s" \
                    "&clienttype=%s" \
                    "&web=%s" \
                    "&app_id=%s" \
                    "&logid=%s" % (share_id, uk, ondup, async, self.bdstoken, channel, clienttype, web, app_id, logid)

        form_data = {
            'filelist': filelist_str,
            'path': path_t_save,
        }


        response = requests.post(url_trans, data=form_data, headers=self.headers)
        print(response.content)

        jsob = json.loads(response.content)

        if "errno" in jsob:
            return jsob["errno"]
        else:
            return None

    def get_file_info(self, url):
        print(u"尝试打开")
        driver = webdriver.Chrome()
        print(u"尝试打开")
        driver.get(url)
        time.sleep(1)
        print(u"正式打开链接")
        driver.get(url)
        print(u"成功获取并加载页面")
        script_list = driver.find_elements_by_xpath("//body/script")
        innerHTML = script_list[-1].get_attribute("innerHTML")

        pattern = 'yunData.SHARE_ID = "(.*?)"[\s\S]*yunData.SHARE_UK = "(.*?)"[\s\S]*yunData.FILEINFO = (.*?);[\s\S]*'  # [\s\S]*可以匹配包括换行的所有字符,\s表示空格，\S表示非空格字符
        srch_ob = re.search(pattern, innerHTML)

        share_id = '504165961'
        share_uk = '1532967721'

        file_info_jsls = json.loads(srch_ob.group(3))
        path_list_str = u'['
        for file_info in file_info_jsls:
            path_list_str += u'"' + file_info['path'] + u'",'

        path_list_str = path_list_str[:-1]
        path_list_str += u']'

        return share_id, share_uk, path_list_str

    def transfer_url(self, url_bdy, path_t_save):
        try:
            print(u"发送连接请求...")
            share_id, share_uk, path_list = self.get_file_info(url_bdy)
        except:
            print(u"链接失效了，没有获取到fileinfo...")
        else:
            error_code = self.transfer('504165961', '1532967721', path_list, path_t_save)
            if error_code == 0:
                print(u"转存成功！")
            else:
                print(u"转存失败了，错误代码：" + str(error_code))


bduss = 'UpNTXhCd3k3VXAwcnEyTnJrR0JWd2RYTkQ5TlppOUppNmY5VXZNcFcydWl2TjljRVFBQUFBJCQAAAAAAAAAAAEAAADIuIFVw8jDyN~VtrqxyM' \
        'fHsM0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKIvuFyiL7hcZ'
stoken = '9d92e708f13f3b516b59652d0f54a821ae05d1b956b8da660171f9f82f021245'
bdstoken = "4fb993821b38c43a524a7ef3aedf2274"
bdy_trans = BaiduYunTransfer(bduss, stoken, bdstoken)

url_src = "http://pan.baidu.com/share/link?shareid=504165961&uk=1532967721"
path = u"/会刊"

bdy_trans.transfer_url(url_src, path)

class save():
    pass
