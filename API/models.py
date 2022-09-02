from django.db import models


class Audio(models.Model):
    device_name = models.CharField(max_length=150)
    audio_base64 = models.CharField(max_length=130000, null=True)
    is_sent = models.BooleanField(default=False)
    audio_base64_text = models.TextField(default='')
    # TODO add a field to for a

# class DeviceApproval(models.Model):
#     device_name = models.CharField(max_length=150)
#     approval_status = models.BooleanField(default=False)
