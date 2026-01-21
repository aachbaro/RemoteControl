from django.test import TestCase
from rest_framework.test import APIClient


class PingTests(TestCase):
    def test_ping(self):
        client = APIClient()
        r = client.get("/api/ping/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "ok")