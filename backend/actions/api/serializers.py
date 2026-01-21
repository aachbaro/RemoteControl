from rest_framework import serializers


class RecordingStateSerializer(serializers.Serializer):
    is_recording = serializers.BooleanField()
    started_at = serializers.DateTimeField(allow_null=True)