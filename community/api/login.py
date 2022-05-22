from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
import json
from django.core import serializers
import os
import platform
from community.models import User
from community.serailize import UserSerializer


# 用户登录
@require_http_methods(["POST"])
def login(request):
    response = {}
    try:
        userJson = json.loads(request.body)
        user = User()
        user.__dict__ = userJson
        dbUser = User.objects.get(account=user.account)
        if dbUser.password != user.password:
            response['data'] = ''
            response['msg'] = 'account or password error'
            response['code'] = 2
        else:
            serializer = UserSerializer(dbUser)
            request.session[str(dbUser.id)] = serializer.data
            response['data'] = serializer.data
            response['token'] = str(dbUser.id)
            response['msg'] = 'success'
            response['code'] = 0
    except User.DoesNotExist as et:
        response['data'] = ''
        response['msg'] = 'account does not exists'
        response['code'] = 2
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)


# 用户登出
@require_http_methods(["POST"])
def logout(request):
    response = {}
    sessionKey = request.session.session_key
    if sessionKey:
        request.session.delete(sessionKey)

    response['data'] = ''
    response['msg'] = ''
    response['code'] = 0
    return JsonResponse(response)


# 用户注册
@require_http_methods(["POST"])
def register(request):
    response = {}
    try:
        userJson = json.loads(request.body)
        user = User()
        user.__dict__ = userJson
        dbUser = User.objects.get(account=user.account)
        if dbUser:
            response['data'] = ''
            response['msg'] = 'account has repeat'
            response['code'] = 2
    except User.DoesNotExist as et:
        User.objects.create(
            name=user.name,
            account=user.account,
            password=user.password,
            phone=user.phone,
            sex=user.sex,
            role=user.role,
            create_time=user.create_time,
            birth=user.birth
        )
        response['data'] = ''
        response['msg'] = 'register success'
        response['code'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)
