#_*_ coding: utf-8 _*_
from tencentcloud.common import credential
from tencentcloud.vpc.v20170312 import vpc_client
from tencentcloud.vpc.v20170312 import models as vpc_models
from tencentcloud.cvm.v20170312 import cvm_client,models as cvm_models

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
import json
import time

#import json data
with open('params.json', 'r') as f:
    params = json.load(f)
id = params["secret_id"]
key = params["secret_key"]
region = params["region"]

#
cred = credential.Credential(id, key)
vpc_client = vpc_client.VpcClient(cred, region)
cvm_client = cvm_client.CvmClient(cred, region)

def show_cvm_info(cvm_id):
    try:
        #cvm_params = {"InstanceIds.N": [cvm_id]}
        filter_params = {"Filters": [{"Name": "instance-id", "Values": [cvm_id]}]}
        req = cvm_models.DescribeInstancesRequest()
        req.from_json_string(json.dumps(filter_params))

        resp = cvm_client.DescribeInstances(req)
        cvm_info = json.loads(resp.to_json_string())["InstanceSet"]
        return cvm_info
    except TencentCloudSDKException as err:
        print (err)

def del_cvm(cvm_id):
    try:
        del_params = {"InstanceIds": [cvm_id]}
        req = cvm_models.TerminateInstancesRequest()
        req.from_json_string(json.dumps(del_params))

        resp = cvm_client.TerminateInstances(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as err:
        print (err)

def show_key_info(key_name):
    try:
        key_params = {"Filters": [{"Name": "key-name", "Values": key_name}]}
        req = cvm_models.DescribeKeyPairsRequest()
        req.from_json_string(json.dumps(key_params))

        resp = cvm_client.DescribeKeyPairs(req)
        key_info = json.loads(resp.to_json_string())["KeyPairSet"]
        return key_info
    except TencentCloudSDKException as err:
        print (err)

def del_key(key_id):
    try:
        del_params = {"KeyIds": [key_id]}
        req = cvm_models.DeleteKeyPairsRequest()
        req.from_json_string(json.dumps(del_params))

        resp = cvm_client.DeleteKeyPairs(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as err:
        print (err)

def show_vpc_info(vpc_id):
    try:
        vpc_params = {"Filters": [{"Name": "vpc-id", "Values": [vpc_id]}]}
        req = vpc_models.DescribeVpcsRequest()
        req.from_json_string(json.dumps(vpc_params))

        resp = vpc_client.DescribeVpcs(req)
        vpc_info = json.loads(resp.to_json_string())["VpcSet"]
        return vpc_info
    except TencentCloudSDKException as err:
        print (err)

def del_vpc(vpc_id):
    try:
        del_params = {"VpcId": vpc_id}
        req = vpc_models.DeleteVpcRequest()
        req.from_json_string(json.dumps(del_params))

        resp = vpc_client.DeleteVpc(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as err:
        print (err)

def show_sg_info(sg_name):
    try:
        sg_params = {"Filters": [{"Name": "security-group-name", "Values": sg_name}]}
        req = vpc_models.DescribeSecurityGroupsRequest()
        req.from_json_string(json.dumps(sg_params))

        resp = vpc_client.DescribeSecurityGroups(req)
        sg_info = json.loads(resp.to_json_string())["SecurityGroupSet"]
        return sg_info
    except TencentCloudSDKException as err:
        print(err)

def del_sg(sg_id):
    try:
        del_params = {"SecurityGroupId": sg_id}
        req = vpc_models.DeleteSecurityGroupRequest()
        req.from_json_string(json.dumps(del_params))

        resp = vpc_client.DeleteSecurityGroup(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as err:
        print (err)


#main()
def clean_main(get_info):
    #查询并删除cvm
    cvm_id = get_info["InstanceId"]
    cvm_info = show_cvm_info(cvm_id)
    if len(cvm_info) == 0:
        print ("INFO:NOT FOUND Instance")
    else:
        print("INFO: Deleting cvm, Loading.....")
        if del_cvm(cvm_id) is True:
            print ("INFO: Deleted CVM :%s" % cvm_id)
        while not len(show_cvm_info(cvm_id)) == 0:
            time.sleep(1)

    #查询并删除KeyPair
    key_id = get_info["KeyInfo"]["KeyPairId"]
    key_name = [get_info["KeyInfo"]["KeyName"]]
    key_info = show_key_info(key_name)
    if len(key_info) == 0:
        print("INFO:NOT FOUND KeyPair")
    else:
        if del_key(key_id) is True:
            print ("INFO: Deleted KeyPair :%s" % key_id)

    #查询并删除vpc
    vpc_id = get_info["VpcId"]
    vpc_info = show_vpc_info(vpc_id)
    if len(vpc_info) == 0:
        print("INFO:NOT FOUND VPC")
    else:
        if del_vpc(vpc_id) is True:
            print ("INFO: Deleted VPC :%s" % vpc_id)

    #查询并删除security group
    sg_id = get_info["SecurityGroupInfo"]["SecurityGroupId"]
    sg_name = [get_info["SecurityGroupInfo"]["SecurityGroupName"]]
    sg_info = show_sg_info(sg_name)

    sg_id_list = []
    if len(sg_info) == 0:
        print("INFO:NOT FOUND security group")
    else:
        for i in range(len(sg_info)):
            sg_id_list.append(sg_info[i]["SecurityGroupId"])

        if sg_id in sg_id_list:
            if del_sg(sg_id) is True:
                print("INFO: Deleted Security Group :%s" % sg_id)
        else:
            print("INFO:NOT FOUND security group")

    return 0

