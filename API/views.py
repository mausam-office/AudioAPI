from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Audio, ClientDevices
from .serializers import AudioSerializer, ClientDevicesSerializer, FilteredAudiosLogSerializer
# from django.http import QueryDict
# from http.client import HTTPResponse
from datetime import datetime
import pytz

from API import serializers


class AudioView(APIView):
    def post(self, request):
        try:
            data = request.data
            print('Try: ', data)
            """ req_str = request.get_full_path().split('?')[1].split('&')
            data = QueryDict('', mutable=True)
            temp = {}
            for item in req_str:
                item = item.split('=')
                if item[0]=='is_sent':
                    temp['is_sent'] = False
                    continue
                temp[item[0]] = item[1]
            print(temp)
            data.update(temp) """
        except:
            data = request.POST
            print('Except: ', data)

        serializer = AudioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Acknowledge":"Successfully done."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeviceRegistration_AudioExtractionView(APIView):
    def get(self, request):
        # getting device name
        try:
            device_name = request.GET['device_name']
            data = request.GET 
        except:
            device_name = dict(request.data)['device_name'][0]
            data = request.data

        # To check if the device is registered
        devices = ClientDevices.objects.filter(device_name=device_name)

        if len(devices) == 0:
            """When the device is not registered"""
            serializer = ClientDevicesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Acknowledge":"Registered."}, status=status.HTTP_201_CREATED)
            return Response({"Acknowledge":"Not Registered."}, status=status.HTTP_400_BAD_REQUEST)

        # Update Last Request time only if it is approved.
        try:
            device_record = ClientDevices.objects.filter(is_approved=True).get(device_name=device_name)
            print('For updating: ', device_record)
            if device_record:
                device_record.last_req_time =  datetime.now()
                device_record.save()
        except:
            print("Not an approved devices")
            return Response({})

        # To check if the device is registered and approved aswell
        devices = ClientDevices.objects.filter(device_name=device_name, is_approved=True)

        if len(devices) != 0:
            """check if there is any data for corresponding device"""
            data = None
            # filtering data from the database
            record = Audio.objects.filter(device_name=device_name, is_sent=False).order_by('id')[:1]
            try:
                serializer = AudioSerializer(record, many=True)

                # extracting base64 format of audio only 
                idx = serializer.data[0]['id']
                audio_str = serializer.data[0]['audio_base64_text']

                # formating the data into dictionary
                data = {'audio_base64_text': audio_str}

                ## update
                row = Audio.objects.get(id=idx)
                row.is_sent = True
                row.save()

                # # deleting the record from the database
                # Audio.objects.get(id=idx).delete()
                Audio.objects.all()
            except:
                # when no record in the database 
                return Response({'audio_base64_text': ''})
            return Response(data)
        # when the device is not approved
        return Response({})




class ClientDevicesListView(APIView):
    def get(self, request):
        # filtering approved devices from the database
        devices = ClientDevices.objects.filter(is_approved=True)
        serializer = ClientDevicesSerializer(devices, many=True)
        

        format = "%Y-%m-%dT%H:%M:%S"
        format_current = "%Y-%m-%d %H:%M:%S"
        #Updating request time
        try:
            for data in serializer.data:
                data = dict(data)
                device_name = data['device_name']
                # split('.')[0] -> removes millisecond part
                # print('last req time: ',  data['last_req_time'])
                last_req_time = data['last_req_time'].split('.')[0]   # In string of ISO format, convert it into  datetime format.
                last_req_time = datetime.strptime(last_req_time, format)
                
                current = datetime.strptime(datetime.now().strftime(format_current), format_current)
                # print('current: ', current)
                diff = current - last_req_time
                diff_minutes = diff.total_seconds()/60
                # print('diff_minutes',diff_minutes)
                
                device_record = ClientDevices.objects.get(device_name=device_name)
                print(device_record)
                if diff_minutes > 2:
                    device_record.is_active = False
                else:
                    device_record.is_active = True
                device_record.save()
                print(device_name, last_req_time, current, diff_minutes)
        except:
            pass

        devices = ClientDevices.objects.all()
        serializer = ClientDevicesSerializer(devices, many=True)
        return Response(serializer.data)    # array of all filtered records




class ClientDeviceApprovalView(APIView):
    def get(self, request):
        try:
            device_name = request.GET['device_name']
        except:
            device_name = dict(request.data)['device_name'][0]
        print(request.GET, device_name)
        try:
            device = ClientDevices.objects.filter(device_name=device_name)
            serializer = ClientDevicesSerializer(device, many=True)
            idx = serializer.data[0]['id']
            device = ClientDevices.objects.get(id=idx)

            device.is_approved = True
            device.save()

            return Response({'Acknowledge' : 'Approved'})
        except:
            return Response({'Acknowledge' : 'Not Approved'})


class BackupAndDeleteView(APIView):
    def get(self, request):
        
        # Delete the records once the timestamp is 
        audio_records = Audio.objects.filter(is_sent=True)
        serializer = AudioSerializer(audio_records, many=True)

        log_data = {}
        for row in serializer.data:
            device_name = row['device_name']
            if device_name not in log_data:
                log_data[device_name] = []
            log_data[device_name].append(row['last_updated'].replace('T', ' '))
            
            audio_record = Audio.objects.get(id=row['id'])
            # We need to delete the audio records after getting timestamp
            audio_record.delete()
            # Updating is just for testing
            # audio_record.last_updated = datetime.now()
            # audio_record.save()

        return Response(log_data)

        