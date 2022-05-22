"""community URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from community.api.login import login, register, logout
from community.api.user import user_info, user_edit, user_list, user_delete, user_add
from community.api.topic import topic_info, topic_delete, topic_update, publish_list, publish
from community.api.record import record_remark, record_info, record_list, record_edit, record_delete
from community.api.upload import uploads
from community.api.device import device_delete, device_info, device_edit, device_list, device_add
from community.api.device_receive import receive_list, receive_info, receive_record
from community.api.report import report_info, report_edit, report_delete, report_list, report_add
from community.api.review import review_list, review_edit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login),
    path('register', register),
    path('logout', logout),
    path(r'user/info/', user_info),
    path('user/edit', user_edit),
    path('user/delete', user_delete),
    path('user/add', user_add),
    path('user/list', user_list),
    path('topic/info', topic_info),
    path('topic/edit', topic_update),
    path('topic/list', publish_list),
    path('topic/publish', publish),
    path('topic/delete', topic_delete),
    path('record/info', record_info),
    path('record/edit', record_edit),
    path('record/delete', record_delete),
    path('record/list', record_list),
    path('record/remark', record_remark),
    path('device/delete', device_delete),
    path('device/info', device_info),
    path('device/edit', device_edit),
    path('device/list', device_list),
    path('device/add', device_add),
    path('receive/list', receive_list),
    path('receive/info', receive_info),
    path('receive/record', receive_record),
    path('report/list', report_list),
    path('report/info', report_info),
    path('report/add', report_add),
    path('report/edit', report_edit),
    path('report/delete', report_delete),
    path('upload', uploads),

    path('review/list', review_list),
    path('review/edit', review_edit)
]
