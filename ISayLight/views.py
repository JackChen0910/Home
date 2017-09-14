# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
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


def light(request):
    if request.method == "POST":
        try:
            operation = json.loads(request.body)["operation"]
            de_id = json.loads(request.body)["id"]
            if operation is None or de_id is None:
                response = {"message": "缺少参数",
                            "status": 300,
                            }
                return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                for d in models.Device.objects.filter(device_id=de_id):
                    if d.sta == "1" and read_nodemcu(d.ip, operation) == 200:
                        response = {"message": "ok",
                                    "status": 200,
                                    }
                        return HttpResponse(json.dumps(response), content_type="application/json")
                    else:
                        response = {"message": "设备不在线",
                                    "status": 401,
                                    }
                        return HttpResponse(json.dumps(response), content_type="application/json")
                        # data = {'operation': operation}
                        # headers = {'content-type': 'application/json'}
                        # requests.post("http://" + d.ip + ":80", data=json.dumps(data), headers=headers)
                        # if json.load(r.text)["code"] is not None:
                        #     response = {"message": "ok",
                        #                 "status": 200,
                        #                 }
                        #     return HttpResponse(json.dumps(response), content_type="application/json")
                        # else:
                        #     response = {"message": "failed",
                        #                 "status": 401,
                        #                 }
                        #     return HttpResponse(json.dumps(response), content_type="application/json")
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


def read_nodemcu(ip, operation):
    data = {'operation': operation}
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 80
    s.connect((ip, port))
    s.send(json.dumps(data))
    return json.loads(s.recv(1024))["code"]
