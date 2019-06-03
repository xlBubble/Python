import json
from data.views import api_test
from django.contrib import auth
from django.shortcuts import render, render_to_response,redirect,HttpResponse
from data import models
import time, datetime


user_name = ""
msg = ""
code = ""

# 页面跳转
def manage(request):
    global user_name
    try:
        if request.session["is_login"]:
            user_name = request.session["name"]
            return render(request, 'manage.html',{"name":user_name})
        else:
            return render(request, '403.html')
    except Exception:
        return render(request, '403.html')

# 获取用户id
def get_user_id():
    user_id = ""
    user_info = models.user.objects.filter(name=user_name)
    for i in user_info:
        user_id = int(i.id)
    return user_id


# 客户查询
def show_cli(request):
    user_id = get_user_id()
    try:
        info = models.client.objects.filter(user_id=user_id).values()
        cli_info = []
        for i in info:
            cli_info.append(i)
            print(i)
        return HttpResponse(json.dumps({"code": '0', "msg": cli_info}))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({"code": '1'}))


# 仅查询客户名称
def show_cli_name(request):
    print("in show_cli_name()")
    user_id = get_user_id()
    try:
        info = models.client.objects.filter(user_id=user_id).values("name")
        cli_name_info = []
        for i in info:
            cli_name_info.append(i)
        print(cli_name_info)
        return HttpResponse(json.dumps({"code": '0', "msg": cli_name_info}))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({"code": '1'}))


#仅查询账号
def show_cli_account(request):
    cli_name = request.POST.get("cli_name")
    try:
        info = models.client.objects.filter(name=cli_name).values("account")
        cli_account_info = []
        for i in info:
            cli_account_info.append(i)
            print(i)
        return HttpResponse(json.dumps({"code": '0', "msg": cli_account_info}))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({"code": '1'}))

# 退出
def logout(request):
    auth.logout(request)
    return redirect("index.html")


# api 验证
def api_confirm(request):
    msg = ""
    if request.method == "POST":
        cloud = request.POST.get("cloud")
        api_id = request.POST.get("api_id")
        api_key = request.POST.get("api_key")
        api_dict = {"cloud": cloud, "api_id": api_id, "api_key": api_key}
        print(api_dict)
        for i in api_dict.values():
            if len(i) == 0:
                msg = "信息不能为空"
                return HttpResponse(json.dumps([{"code": '1', "msg": msg}]))
        test_result = api_test.test(cloud, api_id, api_key)
        return HttpResponse(json.dumps([{"code": '0', "msg": test_result}]))


# 客户新增
def cli_add(request):
    global code, msg
    user_id = get_user_id()
    if request.method == "POST":
        cli_name = request.POST.get("cli_name")
        sub_account = request.POST.get("sub_account")
        cloud = request.POST.get("cloud")
        api_id = request.POST.get("api_id")
        api_key = request.POST.get("api_key")
        cli_dict = {"name": cli_name, "account": sub_account, "cloud": cloud, "api_id": api_id, "api_key": api_key}
        print(cli_dict)
        for i in cli_dict.values():
            if len(i) == 0:
                msg = "信息不能为空"
                code = '1'
                return HttpResponse(json.dumps([{"code": code, "msg": msg}]))

        try:
            cli_count = models.client.objects.filter(api_id=api_id).count()
            if cli_count == 0:
                cli_dict.update({"user_id": user_id})
                models.client.objects.create(**cli_dict)
                msg = "添加成功"
                code = '0'
            else:
                msg = "API ID重复提交"
                code = '1'
        except Exception as e:
            print(e)
            msg = "添加失败"
        return HttpResponse(json.dumps([{"code": code, "msg": msg}]))


# get_cli_id(cli_name)
def get_cli_id(cli_name, cli_account):
    try:
        cli_info = models.client.objects.filter(name=cli_name, account=cli_account).values()
        for item in cli_info:
            cli_id = item['id']
        return cli_id
    except Exception as e:
        print(e)
        return -1


# 事件新增
def add_event(request):
    global msg
    if request.method == "POST":
        cli_name = request.POST.get("add_name")
        cli_account = request.POST.get("add_account")
        product = request.POST.get("add_product")
        type = request.POST.get("add_type")
        detail = request.POST.get("add_detail")
        status = request.POST.get("add_status")
        manager = request.POST.get("add_manager")
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        event_dict = {"date": date, "method": "1", "product": product, "type": type, "detail": detail, "status": status,
                      "manager": manager}
        for i in event_dict.values():
            if len(i) == 0:
                msg = "信息不能为空"
                return HttpResponse(json.dumps([{"code": "1", "msg": msg}]))
        try:
            cli_id = get_cli_id(cli_name, cli_account)
            if cli_id != -1:
                event_dict.update({"cli_id": cli_id})
                models.check.objects.create(**event_dict)
                msg = "添加成功"
                return HttpResponse(json.dumps([{"code": "0", "msg": msg}]))
        except Exception as e:
            print(e)
            msg = "添加失败"
            return HttpResponse(json.dumps([{"code": "1", "msg": msg}]))


# 查询事件
def show_event_info(request):
    cli_id = ''
    cli_name = request.POST.get("cli_name")
    cli_account = request.POST.get("cli_account")
    period = request.POST.get("period")
    try:
        cli_id_info = models.client.objects.filter(name=cli_name, account=cli_account).values()
        for i in cli_id_info:
            cli_id = i['id']
        info = models.check.objects.filter(cli_id=cli_id).values('date', 'method', 'type', 'detail', 'status',
                                                                        'product', 'manager')
        if info.count() == 0:
            code = '1'
            msg = "该客户无事件记录"
        else:
            code = '0'
            msg = []
            for i in info:
                i['date'] = str(i['date'])
                msg.append(i)
                print(i)
        return HttpResponse(json.dumps({"code": code, "msg": msg}))
    except Exception as e:
        print(e)
        code = '1'
        msg = '获取客户失败'
        return HttpResponse(json.dumps({"code": code, "msg": msg}))