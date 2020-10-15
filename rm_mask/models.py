from django.db import models
import os
import datetime


def destination(instance, filename):
    now = datetime.datetime.now()
    now_str = now.strftime('%Y%m%d_%H%M%S')
    extension = os.path.splitext(filename)[-1]
    return 'upload/' + now_str + '/input' + extension


class Photo(models.Model):
    image = models.ImageField(upload_to=destination)
