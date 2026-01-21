from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.utils import timezone

from actions.repositories import recording_repo


@dataclass
class RecordingState:
    is_recording: bool
    started_at: Optional[datetime]


def start() -> RecordingState:
    rec = recording_repo.get_singleton()
    if not rec.is_recording:
        rec.is_recording = True
        rec.started_at = timezone.now()
        recording_repo.save(rec, update_fields=["is_recording", "started_at", "updated_at"])
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)


def stop() -> RecordingState:
    rec = recording_repo.get_singleton()
    rec.is_recording = False
    rec.started_at = None
    recording_repo.save(rec, update_fields=["is_recording", "started_at", "updated_at"])
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)


def status() -> RecordingState:
    rec = recording_repo.get_singleton()
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)
