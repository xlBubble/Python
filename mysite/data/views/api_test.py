from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
from tencentcloud.common.credential import Credential
from tencentcloud.cvm.v20170312 import cvm_client
from tencentcloud.cvm.v20170312 import models
import json


def txy_test(id, key):
    cred = Credential(id, key)
    req = models.DescribeRegionsRequest()
    clt = cvm_client.CvmClient(cred, "ap-shanghai")
    try:
        clt.DescribeRegions(req)
        return 0
    except Exception as e:
        print(e)
        return 1


def aliy_test(id, key):
    try:
        clt = AcsClient(id, key, "cn-shanghai")
        req = DescribeRegionsRequest()
        req.set_accept_format('json')
        req.set_version("2014-05-26")
        clt.do_action_with_exception(req)
        return 0
    except Exception as e:
        print(e)
        return 1


def test(cloud, api_id, api_key):
    code = ""
    if cloud == "txy":
        code = txy_test( api_id, api_key)
    elif cloud == "aliy":
        code = aliy_test( api_id, api_key)
    print(code)
    return code