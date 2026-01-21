from django.test import TestCase
from actions.services import recording_service


class RecordingServiceTests(TestCase):
    def test_start_stop(self):
        s1 = recording_service.status()
        self.assertFalse(s1.is_recording)

        s2 = recording_service.start()
        self.assertTrue(s2.is_recording)
        self.assertIsNotNone(s2.started_at)

        s3 = recording_service.stop()
        self.assertFalse(s3.is_recording)
        self.assertIsNone(s3.started_at)
