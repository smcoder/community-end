from django.core.serializers import serialize

from community.models import Topic, User
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
import json
import datetime
from django.core.paginator import Paginator
from community.serailize import TopicSerializer


# 新增公告
@require_http_methods(["POST"])
def publish(request):
    response = {}
    try:
        topic_str = json.loads(request.body)
        topic = Topic()
        topic.__dict__ = topic_str
        Topic.objects.create(
            title=topic.title,
            content=topic.content,
            picture=topic.picture,
            user_id=topic.user_id,
            create_time=datetime.datetime.now()
        )
        response['data'] = ''
        response['msg'] = 'publish success'
        response['code'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)


# 公告详情
@require_http_methods(["POST"])
def topic_info(request):
    response = {}
    try:
        db_topic = Topic.objects.get(id=request.POST.get('id'))
        response['data'] = json.dumps(db_topic)
        response['msg'] = 'success'
        response['code'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)


# 公告删除
def topic_delete(request):
    response = {}
    try:
        Topic.objects.get(id=json.loads(request.body)['id']).delete()
        response['msg'] = 'delete success'
        response['code'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)


# 公告更新
def topic_update(request):
    response = {}
    try:
        model_topic = json.loads(request.body)
        topic = Topic()
        topic.__dict__ = model_topic
        Topic.objects.filter(id=topic.id).update(
            title=topic.title,
            content=topic.content,
            picture=topic.picture,
            user_id=topic.user_id,
            create_time=datetime.datetime.now()
        )
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)


# 查询公共
@require_http_methods(["POST"])
def publish_list(request):
    param = json.loads(request.body)
    page_no = param['page_no']
    page_size = param['page_size']
    response = {}
    db_list = Topic.objects.all()
    # 创建分页对象
    page = Paginator(db_list, page_size)
    count = page.count
    data = page.page(page_no)

    json_data = serialize('json', list(data))  # str
    json_data = json.loads(json_data)  # 序列化成json对象
    json_list = []
    for obj in json_data:
        user = TopicSerializer(obj['fields'])
        value = user.data
        value['id'] = obj['pk']
        value['createName'] = User.objects.get(id=obj['fields']['user']).name
        json_list.append(value)
    response['data'] = json_list
    response['count'] = count
    response['code'] = 0
    response['msg'] = 'success'
    return JsonResponse(response)

