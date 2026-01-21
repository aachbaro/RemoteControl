from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RecordingStateSerializer
from .services import recording

@api_view(['GET'])
def ping(request):
    return Response({"status": "ok"})

@api_view(['POST'])
def record_start(request):
    state = recording.start()
    data = RecordingStateSerializer(state).data
    return Response(data)

@api_view(['POST'])
def record_stop(request):
    state = recording.stop()
    data = RecordingStateSerializer(state).data
    return Response(data)

@api_view(['GET'])
def record_status(request):
    state = recording.status()
    data = RecordingStateSerializer(state).data
    return Response(data)