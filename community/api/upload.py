from django.http import JsonResponse
import uuid
import os

from django.views.decorators.http import require_http_methods

# 设置图片保存文件夹
from community.settings import BASE_DIR

UPLOAD_FOLDER = 'static'

# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']


# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS


# 上传图片
@require_http_methods(["POST"])
def uploads(request):
    response = {}
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        file_name = str(uuid.uuid4()) + '.png'
        f = open(os.path.join(BASE_DIR, 'community', 'static', file_name), 'wb')
        print(file_obj, type(file_obj))
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        response['data'] = file_name
        response['code'] = 0
        response['msg'] = 'success'
    return JsonResponse(response)
