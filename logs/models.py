from django.db import models

class LogEvent(models.Model):
    service_name = models.CharField(max_length=100)
    log_level = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)