from django.urls import path
from actions.api.views import record_start, record_stop, record_status, ping

urlpatterns = [
    path("ping/", ping),
    path("record/start/", record_start),
    path("record/stop/", record_stop),
    path("record/status/", record_status),
]