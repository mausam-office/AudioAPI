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

'''Aternative way to filter the serialized data'''
# class FilterAudioSerializer(serializers.ListSerializer):
#     filter_kwargs = {}

#     def to_representation(self, data):
#         if not self.filter_kwargs or not isinstance(self.filter_kwargs, dict):
#             raise TypeError(_('Invalid Attribute Type: `filter_kwargs` must be a of type `dict`.'))
#         data = data.filter(**self.filter_kwargs)
#         return super().to_representation(data)

# class AudioLogSerializer(FilterAudioSerializer):
#     filter_kwargs = {'is_sent':True}

class FilteredAudiosLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id','device_name', 'last_updated']
        # list_serializer_class = AudioLogSerializer


