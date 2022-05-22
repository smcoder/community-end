#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from community.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'account', 'password', 'phone', 'sex', 'birth', 'role', 'create_time')


class TopicSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'title', 'content', 'picture', 'user_id', 'create_time')


class RecordSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    modify_user_id = UserSerializer(read_only=True)

    class Meta:
        model = Record
        fields = ('id', 'user_id', 'content', 'remark', 'modify_user_id', 'modify_time', 'create_time')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'picture', 'total_num', 'remain_num', 'use_content', 'attention_content', 'create_time')


class ReportSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ('id', 'picture', 'remark', 'user_id', 'create_time')


class ReportReviewSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    report_id = ReportSerializer(read_only=True)

    class Meta:
        model = ReportReview
        fields = ('id', 'review_remark', 'create_time', 'user_id', 'report_id', 'status')