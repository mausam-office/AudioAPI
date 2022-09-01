from http.client import HTTPResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Audio
from .serializers import AudioSerializer



class AudioView(APIView):
    def post(self, request):
        serializer = AudioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Acknowledge":"Successfully done."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        data = None
        try:
            device_name = request.get_full_path().split('?')[1].split('=')[1]
         
        # getting device name
        except:
            device_name = dict(request.data)['device_name'][0]

        # filtering data from the database
        record = Audio.objects.filter(device_name=device_name, is_sent=False).order_by('id')#[:1]

        try:
            serializer = AudioSerializer(record, many=True) 
            # print(serializer.data)
            # extracting base64 format of audio only 
            idx = serializer.data[0]['id']
            audio_str = serializer.data[0]['audio_base64']
            # print(idx, audio_str)

            # formating the data into dictionary
            data = {'audio_base64': audio_str}
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
            return Response(status=status.HTTP_200_OK)
        return Response(data)
        # return Response(serializer.data)
        
# def index(request):
#     return HTTPResponse("<h1>API site</h1>")
