from django.db import models

from community.base import BaseModel


# 用户信息
class User(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    account = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    sex = models.IntegerField()
    birth = models.DateTimeField()
    role = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'sm_user'

    def __unicode__(self):
        return self.account


# 公告
class Topic(BaseModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.CharField(max_length=200, blank=True)
    picture = models.CharField(max_length=2000, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'sm_topic'

    def __unicode__(self):
        return self.id


# 留言记录表
class Record(BaseModel):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='create_user')
    content = models.CharField(max_length=2000, blank=True)
    remark = models.CharField(max_length=100, blank=True)
    modify_user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='modify_user')
    modify_time = models.DateTimeField
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'sm_record'

    def __unicode__(self):
        return self.id


# 消防设施维护
class Device(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    picture = models.CharField(max_length=2000, blank=True)
    total_num = models.IntegerField()
    remain_num = models.IntegerField()
    use_content = models.CharField(max_length=2000, blank=True)
    attention_content = models.CharField(max_length=2000, blank=True)
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'sm_device'

    def __unicode__(self):
        return self.id


# 消防设施领取
class ReceiveRecord(BaseModel):
    id = models.AutoField(primary_key=True)
    receive_num = models.IntegerField()
    device_name = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'sm_receive_record'

    def __unicode__(self):
        return self.id


# 消防上报记录
class Report(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    picture = models.CharField(max_length=2000, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'sm_report'

    def __unicode__(self):
        return self.id


# 上访记录审核
class ReportReview(BaseModel):
    id = models.AutoField(primary_key=True)
    report = models.ForeignKey(Report, on_delete=models.DO_NOTHING)
    review_remark = models.CharField(max_length=2000, blank=True)
    create_time = models.DateTimeField()
    status = models.IntegerField()

    class Meta:
        db_table = 'sm_report_review'

    def __unicode__(self):
        return self.id
