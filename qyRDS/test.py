# _*_coding:utf-8 _*_
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815.DescribeDatabasesRequest import DescribeDatabasesRequest
import json
import logging

with open('accesslog.txt','w') as f:
    f.truncate()