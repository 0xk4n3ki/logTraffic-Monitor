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



# from celery import shared_task
# from kafka import KafkaConsumer
# import json, django, os
# from .models import LogEvent
# from django.utils import timezone
# from elasticsearch import Elasticsearch
# from django.conf import settings
# from functools import lru_cache

# os.environ.setdefault(
#     'DJANGO_SETTINGS_MODULE',
#     'logTraffic_monitor.settings'
# )
# django.setup()


# @lru_cache(maxsize=1)
# def get_es():
#     return Elasticsearch([settings.ELASTICSEARCH_HOST])

# def index_log_to_es(data):
#     get_es().index(index="logs", document=data)

# @lru_cache(maxsize=1)
# def get_consumer():
#     return KafkaConsumer(
#         'log_events',
#         bootstrap_servers=settings.KAFKA_BROKER_URL,
#         value_deserializer=lambda x: json.loads(x.decode('utf-8')),
#         auto_offset_reset='earliest',
#         enable_auto_commit=True,
#         group_id="log-consumer-group"
#     )


# @shared_task
# def consumer_kafka_logs():
#     consumer = get_consumer()
#     for message in consumer:
#         log_data = message.value
#         print(log_data)

#         if "timestamp" not in log_data or not log_data["timestamp"]:
#             log_data["timestamp"] = timezone.now().isoformat()

#         LogEvent.objects.create(**log_data)
#         index_log_to_es(log_data)



# sudo docker exec -it reverent_aryabhata  /opt/kafka/bin/kafka-topics.sh --create --topic log_events --bootstrap-server localhost:9092
# sudo docker exec -it reverent_aryabhata  /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
# sudo docker exec -it reverent_aryabhata  /opt/kafka/bin/kafka-topics.sh --delete --topic log_event --bootstrap-server localhost:9092
