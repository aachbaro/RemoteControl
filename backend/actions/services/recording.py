from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class RecordingState:
    is_recording: bool = False
    started_at: Optional[datetime] = None


_state = RecordingState()


def start() -> RecordingState:
    if not _state.is_recording:
        _state.is_recording = True
        _state.started_at = datetime.utcnow()
    return _state


def stop() -> RecordingState:
    _state.is_recording = False
    _state.started_at = None
    return _state


def status() -> RecordingState:
    return _state