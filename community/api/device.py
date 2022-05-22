from django.core.serializers import serialize

from community.models import Device
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
import json
import datetime
from django.core.paginator import Paginator


# 设备详情
from community.serailize import DeviceSerializer


@require_http_methods(['POST'])
def device_info(request):
    response = {}
    db_device = Device.objects.get(id=json.loads(request.body)['id'])
    response['data'] = json.dumps(db_device)
    response['code'] = 0
    response['msg'] = 'deal success'
    return JsonResponse(response)


# 设备修改
@require_http_methods(['POST'])
def device_edit(request):
    response = {}
    try:
        json_str = json.loads(request.body)
        device = Device()
        device.__dict__ = json_str
        Device.objects.filter(id=device.id).update(
            name=device.name,
            picture=device.picture,
            total_num=device.total_num,
            use_content=device.use_content,
            attention_content=device.attention_content,
            create_time=datetime.datetime.now()
        )
        response['msg'] = 'deal success'
        response['code'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)


# 新增消防设备
@require_http_methods(["POST"])
def device_add(request):
    response = {}
    try:
        device_json = json.loads(request.body)
        device = Device()
        device.__dict__ = device_json
        db_device = Device.objects.filter(name=device.name)
        if len(db_device) > 0:
            response['code'] = 2
            response['msg'] = '设备名重复，请重新输入！'
        else:
            Device.objects.create(
                name=device.name,
                picture=device.picture,
                total_num=device.total_num,
                remain_num=0,
                use_content=device.use_content,
                attention_content=device.attention_content,
                create_time=datetime.datetime.now()
            )
            response['code'] = 0
            response['msg'] = 'success'
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)


# 消防设备领取
@require_http_methods(['POST'])
def device_receive(request):
    response = {}
    json_str = json.load(request.body)
    device = Device()
    device.__dict__ = json_str
    Device.objects.filter(id=device.id).update(
        remain_num=device.remain_num,
        modify_time=datetime.datetime.now()
    )
    return JsonResponse(response)


# 消防设备删除
@require_http_methods(['POST'])
def device_delete(request):
    response = {}
    Device.objects.get(id=json.loads(request.body)['id']).delete()
    response['code'] = 0
    response['msg'] = 'delete success'
    return JsonResponse(response)


# 设备列表
@require_http_methods(['POST'])
def device_list(request):
    param = json.loads(request.body)
    page_no = param['page_no']
    page_size = param['page_size']
    response = {}
    db_list = Device.objects.all()
    # 创建分页对象
    page = Paginator(db_list, page_size)
    count = page.count
    data = page.page(page_no)

    json_data = serialize('json', list(data))  # str
    json_data = json.loads(json_data)  # 序列化成json对象
    json_list = []
    for obj in json_data:
        device = DeviceSerializer(obj['fields'])
        value = device.data
        value['id'] = obj['pk']
        json_list.append(value)
    response['data'] = json_list
    response['count'] = count
    response['code'] = 0
    response['msg'] = 'success'
    return JsonResponse(response)