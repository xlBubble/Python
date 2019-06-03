# _*_coding:utf-8 _*_
import urllib.request
import json
import time
import logging
import requests

logging.basicConfig(level=logging.DEBUG,
                    filename='accesslog.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )

def gettoken(corpid,corpsecret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    #print(gettoken_url)
    token = json.loads(urllib.request.urlopen(gettoken_url).read().decode())['access_token']
    return token


def senddata(access_token, content):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "touser": "@all",
        "msgtype": "textcard",
        "agentid": "1000002",
        "textcard": {
            "title": "迁移告警通知",
            "description": "<div class=\"normal\">" + time.strftime('%Y-%m-%d %H:%M', time.localtime(
             time.time())) + "</div><div class=\"highlight\">" + "数据库迁移：" + content + "</div>",
            "url": "https://www.aliyun.com",
            "btntxt": "详情"
        },
        "safe": "0"
    }

    '''<font color="info">+ content +</font>'''
    send_data = (bytes(json.dumps(send_values), 'utf-8'))
    try:
        response = urllib.request.urlopen(urllib.request.Request(url=send_url, data=send_data)).read()
        logging.info("已通知")
        return response
    except Exception as e:
        logging.error(e)


def sendfile(access_token, media_id):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "touser": "@all",
        "msgtype": "file",
        "agentid": "1000002",
        "file": {
            'media_id': media_id
        },
        "safe": "0"
    }
    '''<font color="info">+ content +</font>'''
    send_data = (bytes(json.dumps(send_values), 'utf-8'))
    try:
        response = urllib.request.urlopen(urllib.request.Request(url=send_url, data=send_data)).read()
        return response
    except Exception as e:
        logging.error(e)


def get_media_id(access_token, file):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=' + access_token + '&type=file'

    data = {'media': open(file, 'rb')}
    try:
        response = requests.post(url, files=data)
        response_detail = json.loads(response.text)["media_id"]
        return response_detail
    except Exception as e:
        logging.error(e)


def main(value):
    corpid = ''  # CorpID是企业号的标识
    corpsecret = ''  # corpsecretSecret是管理组凭证密钥
    accesstoken = gettoken(corpid, corpsecret)
    senddata(accesstoken, value)
    file = 'accesslog.txt'
    media_id = get_media_id(accesstoken, file)
    #print(media_id)
    sendfile(accesstoken, media_id)
