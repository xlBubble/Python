# -*- coding: utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.vpc.v20170312 import vpc_client
from tencentcloud.vpc.v20170312 import models
from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
import json
import time

# import json data
with open('params.json', 'r') as f:
    params = json.load(f)
id = params["secret_id"]
key = params["secret_key"]
region = params["region"]

#
cred = credential.Credential(id, key)
vpc_client = vpc_client.VpcClient(cred, region)
cvm_client = cvm_client.CvmClient(cred, region)

# create vpc
'''
"vpc":{
		"vpc_name":"api_test",
		"vpc_cidr":"192.168.0.0/16"
	}
'''

def create_vpc():
    try:
        vpc_name = params["vpc"]["vpc_name"]
        vpc_cidr = params["vpc"]["vpc_cidr"]

        req = models.CreateVpcRequest()
        temp = {"VpcName": vpc_name, "CidrBlock": vpc_cidr}
        vpc_params = json.dumps(temp)
        req.from_json_string(vpc_params)

        resp = vpc_client.CreateVpc(req)
        return json.loads(resp.to_json_string())["Vpc"]["VpcId"]
    except TencentCloudSDKException as err:
        print (err)
        exit(1)

#create sudnet
'''
	"subnet":{
		"subnet_name": "test1",
		"zone": "ap-shanghai-1",
		"subnet_cidr": "192.168.1.0/24"
	},
'''
def create_subnet(vpc_id):
    '''
    :param vpc_id:
    :return:
    '''
    try:
        subnet_name = params["subnet"]["subnet_name"]
        zone = params["subnet"]["zone"]
        subnet_cidr = params["subnet"]["subnet_cidr"]

        req = models.CreateSubnetRequest()
        temp = {"VpcId": vpc_id, "SubnetName": subnet_name, "CidrBlock": subnet_cidr, "Zone": zone}
        subnet_params = json.dumps(temp)
        req.from_json_string(subnet_params)

        resp = vpc_client.CreateSubnet(req)
        return json.loads(resp.to_json_string())["Subnet"]["SubnetId"]
    except TencentCloudSDKException as err:
        print (err)
        exit(1)


#create security group
def create_sg():
    try:
        sg_name = params["security_group"]["sg_name"]
        sg_des = params["security_group"]["sg_des"]

        req = models.CreateSecurityGroupRequest()
        temp = {"GroupName": sg_name, "GroupDescription": sg_des}
        subnet_params = json.dumps(temp)
        req.from_json_string(subnet_params)

        resp = vpc_client.CreateSecurityGroup(req)
        return json.loads(resp.to_json_string())["SecurityGroup"]
    except TencentCloudSDKException as err:
        print (err)
        exit(1)

#config group policy
def config_in_policy(sg_id):
    '''
    :param sg_id:
    :return:
    '''
    try:
        Protocol = params["sg_in"]["Protocol"]
        Port = params["sg_in"]["Port"]
        CidrBlock = params["sg_in"]["CidrBlock"]
        Action = params["sg_in"]["Action"]
        Des = params["sg_in"]["Des"]
        req = models.CreateSecurityGroupPoliciesRequest()
        in_policy = {"Protocol": Protocol,
                     "Port": Port,
                     "CidrBlock": CidrBlock,
                     "Action": Action,
                     "PolicyDescription": Des
                     }
        temp = {"SecurityGroupId": sg_id, "SecurityGroupPolicySet": {"Ingress": [in_policy]}}

        policy_params = json.dumps(temp)
        req.from_json_string(policy_params)

        resp = vpc_client.CreateSecurityGroupPolicies(req)
        return resp.to_json_string()
    except TencentCloudSDKException as err:
        print (err)
        exit(1)

def config_out_policy(sg_id):
    '''
    :param sg_id:
    :return:
    '''
    try:
        Port = params["sg_out"]["Port"]
        CidrBlock = params["sg_out"]["CidrBlock"]
        Action = params["sg_out"]["Action"]
        Protocol = params["sg_out"]["Protocol"]
        Des = params["sg_out"]["Des"]

        req = models.CreateSecurityGroupPoliciesRequest()
        out_policy = {
                     "Protocol": Protocol,
                     "Port": Port,
                     "CidrBlock": CidrBlock,
                     "Action": Action,
                     "PolicyDescription": Des
                     }
        temp = {"SecurityGroupId": sg_id, "SecurityGroupPolicySet": {"Egress": [out_policy]}}

        policy_params = json.dumps(temp)
        req.from_json_string(policy_params)

        resp = vpc_client.CreateSecurityGroupPolicies(req)
        return resp.to_json_string()
    except TencentCloudSDKException as err:
        print (err)
        exit(1)

#Describe Project id
def des_pro_id():
    return 0

#create ssh key
# CANCEL.....

def create_sshkey():
    try:
        key_name = params["ssh_key"]["key_name"]
        req = cvm_models.CreateKeyPairRequest()
        temp = {"KeyName": key_name,"ProjectId":"0"}
        key_params = json.dumps(temp)
        req.from_json_string(key_params)

        resp = cvm_client.CreateKeyPair(req)
        return json.loads(resp.to_json_string())["KeyPair"]
    except TencentCloudSDKException as err:
        print (err)
        exit(1)

#create cvm
def create_cvm(vpc_id,subnet_id,sg_id,key_id):
    '''

    :param vpc_id: 
    :param subnet_id:
    :param sg_id:
    :param key_id:
    :return:
    '''
    try:
        InstanceChargeType = params["cvm_info"]["InstanceChargeType"]
        Placement = params["cvm_info"]["Placement"]
        InstanceType = params["cvm_info"]["InstanceType"]
        ImageId = params["cvm_info"]["ImageId"]
        SystemDisk = params["cvm_info"]["SystemDisk"]
        DataDisks = params["cvm_info"]["DataDisks.N"]
        InternetAccessible = params["cvm_info"]["InternetAccessible"]
        InstanceCount = params["cvm_info"]["InstanceCount"]
        InstanceName = params["cvm_info"]["InstanceName"]
        HostName = params["cvm_info"]["HostName"]
        VirtualPrivateCloud = {"VpcId": vpc_id,"SubnetId": subnet_id}
        SecurityGroupId = [sg_id]
        LoginId = [key_id]

        temp = {"InstanceChargeType": InstanceChargeType, "Placement": Placement, "InstanceType": InstanceType, 
        "ImageId": ImageId, "SystemDisk": SystemDisk, "DataDisks": DataDisks, "VirtualPrivateCloud":VirtualPrivateCloud,
        "InternetAccessible": InternetAccessible, "InstanceCount": InstanceCount, "InstanceName": InstanceName, 
        "SecurityGroupIds":SecurityGroupId, "LoginSettings": {"KeyIds": LoginId}, "HostName": HostName}
        cvm_params = json.dumps(temp)

        req = cvm_models.RunInstancesRequest()
        req.from_json_string(cvm_params)

        resp = cvm_client.RunInstances(req)
        cvm_id = json.loads(resp.to_json_string())["InstanceIdSet"]
        #cvm_ip = json.loads(resp.to_json_string())["InstanceSet"][0]["PublicIpAddresses"][0]
        return cvm_id
    except TencentCloudSDKException as err:
        print (err)
        exit(1)

def show_cvm_info(cvm_id):
    try:
        #cvm_params = {"InstanceIds.N": [cvm_id]}
        filter_params = {"Filters": [{"Name": "instance-id", "Values": [cvm_id]}]}
        req = cvm_models.DescribeInstancesRequest()
        req.from_json_string(json.dumps(filter_params))

        resp = cvm_client.DescribeInstances(req)
        cvm_ip = json.loads(resp.to_json_string())["InstanceSet"][0]["PublicIpAddresses"]
        return cvm_ip
    except TencentCloudSDKException as err:
        print(err)

#main()
def create_main():
    vpc_id = create_vpc()
    print("INFO:Create vpc ok.           VPC ID: %s" % vpc_id)
    subnet_id = create_subnet(vpc_id)
    print("INFO:Create subnet ok.        SUBNET ID: %s" % subnet_id)
    sg_info = create_sg()
    sg_id = sg_info["SecurityGroupId"]
    sg_name = sg_info["SecurityGroupName"]
    print("INFO:Create security group ok. SG ID: %s" % sg_id)
    config_in_policy(sg_id)
    print("INFO:Config ingress policy ok.")
    config_out_policy(sg_id)
    print("INFO:Config egress policy ok.")

    #pro_id = des_pro_id()

    key_info = create_sshkey()
    key_id = key_info["KeyId"]
    key_name = key_info["KeyName"]
    private_key = key_info["PrivateKey"]

    print("INFO:Create ssh key ok.  KEY ID: %s" % key_id)


    print("INFO:Create cvm loading......")
    cvm_id = create_cvm(vpc_id, subnet_id, sg_id, key_id)
    cvm_ip = show_cvm_info(cvm_id[0])
    while cvm_ip is None:
        time.sleep(1)
        cvm_ip = show_cvm_info(cvm_id[0])

    print("INFO:Create cvm ok.  CVM ID: %s  CVM ip: %s" % (cvm_id[0],cvm_ip[0]))

    #save private_key in sshKey file
    with open("sshKey", 'w') as f:
            f.write(private_key)

    bak_info = {"InstanceId": cvm_id[0], "KeyInfo": {"KeyPairId": key_id, "KeyName": key_name},
                "VpcId": vpc_id, "SecurityGroupInfo": {"SecurityGroupId": sg_id, "SecurityGroupName": sg_name}}
    return bak_info

#if __name__ == "__main__":
#        create_main()
