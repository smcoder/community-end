from django.core.serializers import serialize

from community.models import ReceiveRecord
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.core.paginator import Paginator


# 设备领取详情
@require_http_methods(['POST'])
def receive_info(request):
    response = {}
    db_receive = ReceiveRecord.objects.get(id=json.loads(request.body)['id'])
    response['data'] = json.dumps(db_receive)
    response['code'] = 0
    response['msg'] = 'deal success'
    return JsonResponse(response)


# 消防设备领取、归还
@require_http_methods(['POST'])
def receive_record(request):
    response = {}
    json_str = json.load(request.body)
    receive = ReceiveRecord()
    receive.__dict__ = json_str
    ReceiveRecord.objects.filter(id=receive.id).update(
        receive_num=receive.receive_num
    )
    return JsonResponse(response)


# 设备列表
@require_http_methods(['POST'])
def receive_list(request):
    page_no = int(request.POST.get('page_no'))
    page_size = int(request.POST.get('page_size'))
    response = {}
    db_list = ReceiveRecord.objects.all()
    # 创建分页对象
    page = Paginator(db_list, page_size)
    count = page.count
    data = page.page(page_no)
    json_data = serialize('json', list(data))  # str
    json_data = json.loads(json_data)  # 序列化成json对象
    json_list = []
    for obj in json_data:
        json_list.append(json.dumps(obj['fields'], ensure_ascii=False))
    response['data'] = json_list
    response['count'] = count
    response['code'] = 0
    response['msg'] = 'success'
    return JsonResponse(response)