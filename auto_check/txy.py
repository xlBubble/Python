# -*- coding: utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.yunjing.v20180228 import models as yunjing_models
from tencentcloud.yunjing.v20180228 import yunjing_client
import json
import txy_show_endtime_info

#get yunjing info
def DescribeOverviewStatistics(yj_client):
    req = yunjing_models.DescribeOverviewStatisticsRequest()
    resp = yj_client.DescribeOverviewStatistics(req)
    return json.loads(resp.to_json_string())


def get_main(item):
    id = item["id"]
    key = item["key"]
    region = ""
    cred = credential.Credential(id, key)
    yj_client = yunjing_client.YunjingClient(cred, region)
    #get yunjing info
    safe_info = DescribeOverviewStatistics(yj_client)
    #get endtime info
    count = txy_show_endtime_info.show_endtime_info(item)
    monitor_info = {'NonlocalLoginNum': safe_info['NonlocalLoginNum'], 'BruteAttackSuccessNum': safe_info['BruteAttackSuccessNum'],
                    'VulNum': safe_info['VulNum'], 'BaseLineNum': safe_info['BaseLineNum'], 'MalwareNum': safe_info['MalwareNum'],
                    'dead_in_7d': count}
    return monitor_info
