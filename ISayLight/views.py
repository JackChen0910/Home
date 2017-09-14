# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
from django.utils.datastructures import MultiValueDictKeyError
from ISayLight import models


def register_online(request):
    if request.method == "POST":
        try:
            de_id = json.loads(request.body)["id"]
            if de_id is None:
                response = {"message": "缺少参数",
                            "status": 300,
                            }
                return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                for d in models.Device.objects.filter(device_id=de_id):
                    d.sta = 1
                    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                        ip = request.META['HTTP_X_FORWARDED_FOR']
                    else:
                        ip = request.META['REMOTE_ADDR']
                    d.ip = ip
                    d.save()
                    response = {"message": "online",
                                "status": 200,
                                }
                    return HttpResponse(json.dumps(response), content_type="application/json")
                response = {"message": "未找到设备",
                            "status": 400,
                            }
                return HttpResponse(json.dumps(response), content_type="application/json")
        except MultiValueDictKeyError:
            response = {"message": "缺少参数",
                        "status": 300,
                        }
            return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {"message": "只允许POST方法",
                    "status": 500,
                    }
        return HttpResponse(json.dumps(response), content_type="application/json")


def device_offline(res):
    for d in models.Device.objects.filter():
        if datetime.datetime.now() - datetime.timedelta(minutes=30) > d.update_time:
            d.sta = 0
            d.save()
    return HttpResponse("", content_type="application/json")
