# -*- coding: utf-8 -*-

from tencentcloud.common import credential
from tencentcloud.vpc.v20170312 import vpc_client
from tencentcloud.vpc.v20170312 import models as vpc_models

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
import json
import time

#import json data
with open('params.json', 'r') as f:
    params = json.load(f)
id = params["secret_id"]
key = params["secret_key"]
region = "ap-shanghai"
sg_name = "api_test1"

cred = credential.Credential(id, key)
vpc_client = vpc_client.VpcClient(cred, region)

def show_sg_info(sg_name):
    try:
        sg_params = {"Filters": [{"Name": "security-group-name", "Values": sg_name}]}
        req = vpc_models.DescribeSecurityGroupsRequest()
        req.from_json_string(json.dumps(sg_params))

        resp = vpc_client.DescribeSecurityGroups(req)
        sg_info = json.loads(resp.to_json_string())["SecurityGroupSet"]
        return sg_info
    except TencentCloudSDKException as err:
        print (err)
        return -1


#key_info = show_sg_info(sg_name)
if "key_info = show_sg_info(sg_name)" is True :
    print ("OK")
else:
    print ("NOT OK")
