from django.db import models
from django.contrib.auth.models import User
import secrets

class LogEvent(models.Model):
    service_name = models.CharField(max_length=100)
    log_level = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=False)

class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys")
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    @staticmethod
    def generate():
        return secrets.token_hex(32)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate()
        super().save(*args, **kwargs)