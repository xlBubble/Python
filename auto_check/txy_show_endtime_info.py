from tencentcloud.common import credential
from tencentcloud.vpc.v20170312 import vpc_client, models as vpc_models
from tencentcloud.cbs.v20170312 import cbs_client, models as cbs_models
from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
import json
import datetime
from dateutil.parser import parse

def show_endtime_info(item):
    #
    count = 0
    now = datetime.datetime.now()
    expire_time_list = []
    #
    id = item["id"]
    key = item["key"]
    region = item["region"]
    cred = credential.Credential(id, key)
    client_cvm = cvm_client.CvmClient(cred, region)
    client_cbs = cbs_client.CbsClient(cred, region)
    client_vpc = vpc_client.VpcClient(cred, region)
    #
    cvm_info = cvm(client_cvm)
    for i in cvm_info:
        expiretime = i["ExpiredTime"].split('T')[0]
        expire_time_list.append(parse(expiretime))
    #
    cbs_info = cbs(client_cbs)
    for i in cbs_info:
        expiretime = i["DeadlineTime"]
        expire_time_list.append(parse(expiretime))

    count = show_result(now, count, expire_time_list)
    return count

def cvm(client_cvm):
    try:
        filter_params = {"Filters": [{"Name": "instance-charge-type", "Values": ["PREPAID"]}]}
        req = cvm_models.DescribeInstancesRequest()
        """req.Filters = [{
            "Name": "instance-charge-type",
            "Values": ["PREPAID"]
        }]"""
        req.from_json_string(json.dumps(filter_params))
        resp = client_cvm.DescribeInstances(req)
        cvm_info = json.loads(resp.to_json_string())["InstanceSet"]
        return cvm_info
    except TencentCloudSDKException as err:
        print(err)

def cbs(client_cbs):
    try:
        filter_params = {"Filters": [{"Name": "disk-charge-type", "Values": ["PREPAID"]},
                         {"Name": "disk-usage", "Values": ["DATA_DISK"]}]}
        req = cbs_models.DescribeDisksRequest()
        req.from_json_string(json.dumps(filter_params))
        resp = client_cbs.DescribeDisks(req)
        cbs_info = json.loads(resp.to_json_string())["DiskSet"]
        return cbs_info
    except TencentCloudSDKException as err:
        print(err)


def show_result(now, count, expire_time_list):
    for i in expire_time_list:
        day = (i - now).days
        if day <= 7:
            count += 1
    return count