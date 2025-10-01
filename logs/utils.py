import json
from django.utils import timezone
from elasticsearch import Elasticsearch
from django.conf import settings
from .models import LogEvent
from time import sleep

def get_es(retries=5, delay=3):
    for i in range(retries):
        try:
            es = Elasticsearch([settings.ELASTICSEARCH_HOST])
            if es.ping():
                return es
        except ConnectionError:
            sleep(delay)
    raise ConnectionError("Elasticsearch is not available after multiple retries")

def index_log_to_es(data):
    get_es().index(index="logs", document=data)

def process_log_message(log_data):
    if "timestamp" not in log_data or not log_data["timestamp"]:
        log_data['timestamp'] = timezone.now().isoformat()
    
    LogEvent.objects.create(**log_data)
    index_log_to_es(log_data)