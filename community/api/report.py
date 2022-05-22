import datetime

from django.core.serializers import serialize

from community.models import Report, User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.core.paginator import Paginator


# 上报详情
from community.serailize import ReportSerializer


@require_http_methods(['POST'])
def report_info(request):
    response = {}
    db_report = Report.objects.get(id=json.loads(request.body)['id'])
    response['data'] = json.dumps(db_report)
    response['code'] = 0
    response['msg'] = 'deal success'
    return JsonResponse(response)


# 新增上报记录
@require_http_methods(["POST"])
def report_add(request):
    response = {}
    try:
        report_json = json.loads(request.body)
        report = Report()
        report.__dict__ = report_json
        Report.objects.create(
            picture=report.picture,
            remark=report.remark,
            user_id=report.user_id,
            create_time=datetime.datetime.now()
        )
        response['code'] = 0
        response['msg'] = 'success'
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)


# 上报修改
@require_http_methods(['POST'])
def report_edit(request):
    response = {}
    json_str = json.loads(request.body)
    report = Report()
    report.__dict__ = json_str
    Report.objects.filter(id=report.id).update(
        picture=report.picture,
        remark=report.remark
    )
    response['msg'] = 'deal success'
    response['code'] = 0
    return JsonResponse(response)


# 上报记录删除
@require_http_methods(['POST'])
def report_delete(request):
    response = {}
    Report.objects.get(id=json.loads(request.body)['id']).delete()
    response['code'] = 0
    response['msg'] = 'delete success'
    return JsonResponse(response)


# 上报列表
@require_http_methods(['POST'])
def report_list(request):
    param = json.loads(request.body)
    page_no = param['page_no']
    page_size = param['page_size']
    response = {}
    db_list = Report.objects.all()
    # 创建分页对象
    page = Paginator(db_list, page_size)
    count = page.count
    data = page.page(page_no)

    json_data = serialize('json', list(data))  # str
    json_data = json.loads(json_data)  # 序列化成json对象
    json_list = []
    for obj in json_data:
        user = ReportSerializer(obj['fields'])
        value = user.data
        value['id'] = obj['pk']
        value['createName'] = User.objects.get(id=obj['fields']['user']).name
        json_list.append(value)
    response['data'] = json_list
    response['count'] = count
    response['code'] = 0
    response['msg'] = 'success'
    return JsonResponse(response)