from django.test import TestCase
from rest_framework.test import APIClient


class RecordingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_status_default_is_false(self):
        r = self.client.get("/api/record/status/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["is_recording"], False)
        self.assertIsNone(r.json()["started_at"])

    def test_start_sets_is_recording_true(self):
        r = self.client.post("/api/record/start/", format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["is_recording"], True)
        self.assertIsNotNone(r.json()["started_at"])

    def test_stop_sets_is_recording_false(self):
        self.client.post("/api/record/start/", format="json")
        r = self.client.post("/api/record/stop/", format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["is_recording"], False)
        self.assertIsNone(r.json()["started_at"])
