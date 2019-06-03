import json
from data.views import api_test
from django.contrib import auth
from django.shortcuts import render, render_to_response,redirect,HttpResponse
from data import models
import time,datetime

def check_start(request):
    return HttpResponse(json.dumps({"code": 1, "msg": "loading"}))