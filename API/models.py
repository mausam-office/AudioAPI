from django.db import models


class Audio(models.Model):
    device_name = models.CharField(max_length=150)
    audio_base64 = models.CharField(max_length=130000)
    is_sent = models.BooleanField(default=False)