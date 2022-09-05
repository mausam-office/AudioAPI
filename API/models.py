from datetime import datetime
from django.db import models


class Audio(models.Model):
    device_name = models.CharField(max_length=150)
    audio_base64 = models.CharField(max_length=130000, null=True)
    is_sent = models.BooleanField(default=False)
    audio_base64_text = models.TextField(default='')
    # added a field to determine inactive devices.
    last_updated = models.DateTimeField(auto_now=True)


class ClientDevices(models.Model):
    device_name = models.CharField(max_length=150, blank=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    last_req_time = models.DateTimeField(auto_now=False, null=True)

