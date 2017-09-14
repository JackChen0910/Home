# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Device(models.Model):
    device_id = models.CharField(max_length=10, unique=True)
    ip = models.CharField(max_length=22)
    place = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    sta = models.CharField(max_length=1)
    description = models.TextField()
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        # 在Python3中使用 def __str__(self):
        return self.type + ":" + self.device_id
