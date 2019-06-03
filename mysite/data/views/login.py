from django.db.models import QuerySet
from django.shortcuts import render,render_to_response,redirect,HttpResponse
from data import models
import time
# Create your views here.
from data.models import user
import json


def login(request):
    error_msg = ""
    if request.method == "POST":
        name = request.POST.get('login_name')
        pwd = request.POST.get("login_password")
        sf = request.POST.get('login_sf')
        print(name, pwd, sf)
        if len(name) == 0 or len(pwd) == 0:
            error_msg = '用户名或密码为空!'
        else:
            user_info = models.user.objects.filter(name=name)
            print("In Line22:%s" % user_info)
            if user_info.count() == 0:
                error_msg = '用户名不存在!'
            else:
                for item in user_info:
                    print("In Line27:%s,%s,%s" % (item, item.name, item.password))
                    if name == item.name and pwd == item.password:
                        request.session["name"] = name
                        request.session["is_login"] = True
                        return redirect("manage.html")
                    else:
                        error_msg = '用户名或密码错误!'
    return render(request, "index.html", {'error_msg': error_msg})


# Ajax POST 提交注册信息
def ajax_register(request):
    r_error_msg = ""
    name = request.POST.get('ajax_name')
    pwd = request.POST.get("ajax_pwd")
    retry_pwd = request.POST.get("ajax_retry_pwd")
    user_list = [name, pwd, retry_pwd]
    print(user_list)
    if len(name) == 0 or len(pwd) == 0 or len(retry_pwd) == 0 :
        r_error_msg = '用户名或密码为空!'
        print(r_error_msg)
    elif pwd != retry_pwd:
        r_error_msg = '密码不匹配!'
        print(r_error_msg)
    else:
        user_dict = {'name': name, 'password': pwd}
        user_info = models.user.objects.filter(name=name)
        print("In Line58:%s" % user_info)
        if user_info.count() == 0:
            try:
                models.user.objects.create(**user_dict)
                print("注册成功")
            except Exception as e:
                print(e)
            info_list = [{'code_msg': '0', "r_error_msg": r_error_msg}]
            return HttpResponse(json.dumps(info_list))
        else:
            r_error_msg = '该用户已被注册!'
            print(r_error_msg)
    info_list = [{'code_msg': '1', "r_error_msg": r_error_msg}]
    return HttpResponse(json.dumps(info_list))


def homepage(request):
    response = render_to_response('index.html')
    return response
