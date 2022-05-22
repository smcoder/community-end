from django.core.serializers import serialize

from community.models import Topic, User, ReportReview, Report
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
import json
import datetime
from django.core.paginator import Paginator
from community.serailize import TopicSerializer, ReportReviewSerializer, ReportSerializer


@require_http_methods(["POST"])
def review_edit(request):
    response = {}
    try:
        json_str = json.loads(request.body)
        review = ReportReview()
        review.__dict__ = json_str
        ReportReview.objects.filter(id=review.id).update(
            review_remark=review.review_remark,
            status=1,
            create_time=datetime.datetime.now()
        )
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 1
    return JsonResponse(response)

# 查询公共
@require_http_methods(["POST"])
def review_list(request):
    param = json.loads(request.body)
    page_no = param['page_no']
    page_size = param['page_size']
    response = {}
    db_list = ReportReview.objects.all()
    # 创建分页对象
    page = Paginator(db_list, page_size)
    count = page.count
    data = page.page(page_no)

    json_data = serialize('json', list(data))  # str
    json_data = json.loads(json_data)  # 序列化成json对象
    json_list = []
    for obj in json_data:
        report = ReportReviewSerializer(obj['fields'])
        value = report.data
        value['id'] = obj['pk']
        value['picture'] = Report.objects.get(id=obj['fields']['report']).picture
        value['remark'] = Report.objects.get(id=obj['fields']['report']).remark
        value['use_name'] = Report.objects.get(id=obj['fields']['report']).user.name
        json_list.append(value)
    response['data'] = json_list
    response['count'] = count
    response['code'] = 0
    response['msg'] = 'success'
    return JsonResponse(response)

