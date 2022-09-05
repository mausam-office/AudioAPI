from rest_framework import serializers
from .models import Audio, ClientDevices

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = "__all__"

class ClientDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDevices
        fields = '__all__'