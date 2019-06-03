import json
from django.shortcuts import render, render_to_response,redirect,HttpResponse
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from tencentcloud.cvm.v20170312 import cvm_client, models
from data import models
import time

def DescribeRegions(cloud):
    cred = ("", "")
    req = models.DescribeRegionsRequest()
    clt = cvm_client.CvmClient(cred, cloud)
    try:
        resq = clt.DescribeRegions(req)
        return resq
    except Exception as e:
        print(e)



def show_region(request):
    cloud = request.POST.get("cloud")
    if cloud == "txy":
        DescribeRegions(cloud)
    elif cloud == "aliy":
        pass
    else:
        pass
    return HttpResponse("LOADING")