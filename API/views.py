from http.client import HTTPResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Audio, ClientDevices
from .serializers import AudioSerializer, ClientDevicesSerializer
from datetime import datetime


class AudioView(APIView):
    def post(self, request):
        serializer = AudioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Acknowledge":"Successfully done."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # This get should be depriciated.
    def get(self, request):
        data = None
        # getting device name
        try:
            device_name = dict(request.data)['device_name'][0]
            print("first name", device_name)

        except:
            device_name = request.get_full_path().split('?')[1].split('=')[1]
            print("second name", device_name)

        # filtering data from the database
        record = Audio.objects.filter(device_name=device_name, is_sent=False).order_by('id')#[:1]

        try:
            serializer = AudioSerializer(record, many=True)
            # print(serializer.data)
            # extracting base64 format of audio only 
            idx = serializer.data[0]['id']
            audio_str = serializer.data[0]['audio_base64_text']
            # print(idx, audio_str)

            # formating the data into dictionary
            data = {'audio_base64_text': audio_str}
            # print(data)

            ## update
            row = Audio.objects.get(id=idx)
            row.is_sent = True
            row.save()
            print("After Updatae")

            # # deleting the record from the database
            # Audio.objects.get(id=idx).delete()

        except:
            print("Exception")

            # when no record in the database 
            return Response({'audio_base64_text': ''})
        return Response(data)


class DeviceRegistration_AudioExtractionView(APIView):
    def get(self, request):
        # getting device name
        try:
            device_name = dict(request.data)['device_name'][0]
            print("try block")
        except:
            device_name = request.get_full_path().split('?')[1].split('=')[1]
            print("except block")
        print(dict(request.data))

        # To check if the device is registered
        devices = ClientDevices.objects.filter(device_name=device_name)

        # print(devices, len(devices))
        if len(devices) == 0:
            """When the device is not registered"""
            print("registration maa")
            serializer = ClientDevicesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Acknowledge":"Registered."}, status=status.HTTP_201_CREATED)
            return Response({"Acknowledge":"Not Registered."}, status=status.HTTP_400_BAD_REQUEST)

        # To check if the device is registered and approved aswell
        devices = ClientDevices.objects.filter(device_name=device_name, is_approved=True)
        print(devices)
        if len(devices) != 0:
            """Here should be the code to check if there is any data"""
            data = None
            print("audio axtraction maa")

            # filtering data from the database
            record = Audio.objects.filter(device_name=device_name, is_sent=False).order_by('id')[:1]

            try:
                serializer = AudioSerializer(record, many=True)
                # print(serializer.data)
                # extracting base64 format of audio only 
                idx = serializer.data[0]['id']
                audio_str = serializer.data[0]['audio_base64_text']
                time = serializer.data[0]['last_updated']
                # print(idx, audio_str)

                # formating the data into dictionary
                data = {'audio_base64_text': audio_str}
                # print(data)

                ## update
                row = Audio.objects.get(id=idx)
                row.is_sent = True
                # row.time = datetime
                row.save()
                print("After Update")

                # # deleting the record from the database
                # Audio.objects.get(id=idx).delete()

            except:
                print("Exception")

                # when no record in the database 
                return Response({'audio_base64_text': ''})
            return Response(data)
        # when the device is not approved
        return Response({})


class ClientDevicesListView(APIView):
    # TODO also add validation for `is_active`
    def get(self, request):
        # filtering registered devices from the database
        devices = ClientDevices.objects.all()
        serializer = ClientDevicesSerializer(devices, many=True)
        registered_devices = serializer.data

        for data in serializer.data:
            data = dict(data)
            device_name = data['device_name']
            record = Audio.objects.filter(device_name=device_name).order_by('-id')[:1]
            
            print(len(record))

        
        return Response(registered_devices)    # array of all filtered records


class ClientDeviceApprovalView(APIView):
    def get(self, request):
        try:
            device_name = dict(request.data)['device_name'][0]
        except:
            device_name = request.get_full_path().split('?')[1].split('=')[1]

        device = ClientDevices.objects.filter(device_name=device_name)
        serializer = ClientDevicesSerializer(device, many=True)
        idx = serializer.data[0]['id']
        device = ClientDevices.objects.get(id=idx)

        device.is_approved = True
        device.save()

        return Response({'Acknowledge' : 'Approved'})

