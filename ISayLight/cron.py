import datetime

from ISayLight import models


def device_offline():
    for d in models.Device.objects.filter():
        if datetime.datetime.now() - datetime.timedelta(minutes=5) > d.update_time:
            d.sta = 0
            d.save()