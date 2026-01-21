from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.utils import timezone

from actions.models import Recording


@dataclass
class RecordingState:
    is_recording: bool
    started_at: Optional[datetime]


def _get_singleton() -> Recording:
    """
    Retourne l'unique ligne Recording.
    Si elle n'existe pas, on la crée.
    """
    obj, _created = Recording.objects.get_or_create(
        id=1,
        defaults={"is_recording": False, "started_at": None},
    )
    return obj


def start() -> RecordingState:
    rec = _get_singleton()
    if not rec.is_recording:
        rec.is_recording = True
        rec.started_at = timezone.now()
        rec.save(update_fields=["is_recording", "started_at", "updated_at"])
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)


def stop() -> RecordingState:
    rec = _get_singleton()
    rec.is_recording = False
    rec.started_at = None
    rec.save(update_fields=["is_recording", "started_at", "updated_at"])
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)


def status() -> RecordingState:
    rec = _get_singleton()
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)