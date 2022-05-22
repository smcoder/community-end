from django.core.serializers import serialize

from community.api.date_encoding import date_encoding
from community.models import User
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
import json
import datetime
from django.core.paginator import Paginator
from community.serailize import UserSerializer


# 用户详情
@require_http_methods(['GET'])
def user_info(request):
    response = {}
    db_user = User.objects.get(id=request.GET.get('token'))
    user = UserSerializer(db_user)
    response['data'] = user.data
    response['msg'] = 'success'
    response['code'] = 0
    return JsonResponse(response)


# 用户修改
@require_http_methods(["POST"])
def user_edit(request):
    response = {}
    try:
        user_json = json.loads(request.body)
        user = User()
        user.__dict__ = user_json
        db_user = User.objects.filter(account=user.account)
        if len(db_user) > 0:
            response['code'] = 2
            response['msg'] = 'account has been repeat'
        else:
            User.objects.filter(id=user.id).update(
                name=user.name,
                account=user.account,
                password=user.password,
                phone=user.phone,
                sex=user.sex,
                role=user.role,
                birth=user.birth
            )
            response['code'] = 0
            response['msg'] = 'success'
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)


# 新增用户
@require_http_methods(["POST"])
def user_add(request):
    response = {}
    try:
        user_json = json.loads(request.body)
        user = User()
        user.__dict__ = user_json
        db_user = User.objects.filter(account=user.account)
        if len(db_user) > 0:
            response['code'] = 2
            response['msg'] = '账号名重复，请重新输入！'
        else:
            User.objects.create(
                name=user.name,
                account=user.account,
                password=user.password,
                phone=user.phone,
                sex=user.sex,
                role=user.role,
                birth=user.birth,
                create_time=datetime.datetime.now()
            )
            response['code'] = 0
            response['msg'] = 'success'
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)


# 用户删除
@require_http_methods(["POST"])
def user_delete(request):
    response = {}
    User.objects.get(id=json.loads(request.body)['id']).delete()
    response['code'] = 0
    response['data'] = 'delete success'
    return JsonResponse(response)


# 用户列表
@require_http_methods(['POST'])
def user_list(request):
    param = json.loads(request.body)
    page_no = param['page_no']
    page_size = param['page_size']
    response = {}
    db_list = User.objects.all()
    # 创建分页对象
    page = Paginator(db_list, page_size)
    count = page.count
    data = page.page(page_no)

    json_data = serialize('json', list(data))  # str
    json_data = json.loads(json_data)  # 序列化成json对象
    json_list = []
    for obj in json_data:
        user = UserSerializer(obj['fields'])
        value = user.data
        value['id'] = obj['pk']
        json_list.append(value)
    response['data'] = json_list
    response['count'] = count
    response['code'] = 0
    response['msg'] = 'success'
    return JsonResponse(response)
