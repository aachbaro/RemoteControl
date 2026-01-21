from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import recording

@api_view(['GET'])
def ping(request):
    return Response({"status": "ok"})

@api_view(['POST'])
def record_start(request):
    state = recording.start()
    return Response(
        {
            "is_recording": state.is_recording,
            "started_at": state.started_at.isoformat() if state.started_at else None,
        }
    )

@api_view(['POST'])
def record_stop(request):
    state = recording.stop()
    return Response(
        {
            "is_recording": state.is_recording,
            "started_at": None,
        }
    )

@api_view(['GET'])
def record_status(request):
    state = recording.status()
    return Response(
        {
            "is_recording": state.is_recording,
            "started_at": state.started_at.isoformat() if state.started_at else None,
        }
    )