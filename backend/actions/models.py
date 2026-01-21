from django.db import models

# Create your models here.

class Recording(models.Model):
    is_recording = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recording(is_recording={self.is_recording}, started_at={self.started_at})"
