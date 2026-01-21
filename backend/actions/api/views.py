from rest_framework.decorators import api_view
from rest_framework.response import Response

from actions.api.serializers import RecordingStateSerializer
from actions.services import recording_service


@api_view(["POST"])
def record_start(request):
    state = recording_service.start()
    return Response(RecordingStateSerializer(state).data)


@api_view(["POST"])
def record_stop(request):
    state = recording_service.stop()
    return Response(RecordingStateSerializer(state).data)


@api_view(["GET"])
def record_status(request):
    state = recording_service.status()
    return Response(RecordingStateSerializer(state).data)