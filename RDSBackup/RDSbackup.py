#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 14:32
# @Author  : xule
# @File    : RDSbackup.py

from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815.DescribeLogBackupFilesRequest import DescribeLogBackupFilesRequest
import json
import logging
from datetime import datetime, timedelta
import os,sys
# import subprocess


def get_time():
    tmp_time = (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%dT")
    stime = tmp_time + '00:00Z'
    tmp_time = datetime.now().strftime("%Y-%m-%dT")
    etime = tmp_time + '00:00Z'
    return stime, etime


def get_url():
    logging.info('获取备份URL')
    request = DescribeLogBackupFilesRequest()
    request.set_accept_format('json')
    request.set_version('2014-08-15')
    request.set_DBInstanceId(rdsid)
    request.set_StartTime(stime)
    request.set_EndTime(etime)
    try:
        response = clt.do_action_with_exception(request)
        url_info = json.loads(response.decode('utf-8'))['Items']['BinLogFile'][0]
        if 'IntranetDownloadLink' in url_info:
            internal_url = url_info['IntranetDownloadLink']
            logging.info("备份URL:{}".format(internal_url))
            return internal_url
        else:
            logging.error('未获取到备份URL')
            exit()
    except Exception as e:
        logging.error(e)


def upload_bak():
    logging.info("开始下载并上传文件")
    param = './upload.sh '+filepath+' '+"'"+url+"'"
    os.system(param)


if __name__ == '__main__':
    filepath = '/data/rdsbak'
    sys.path.insert(0, filepath)
    os.chdir(filepath)
    time = datetime.now().strftime("%Y%m%d")
    logging.basicConfig(level=logging.DEBUG,
                    filename= 'logs/baklog_' + str(time),
                    filemode='a',
                    format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s'
                    )
    sid = ''
    skey = ''
    region = 'cn-shanghai'
    rdsid = ''
    clt = client.AcsClient(sid, skey, region)
    stime, etime = get_time()
    url = get_url()
    upload_bak()