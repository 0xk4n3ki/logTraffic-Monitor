from celery import shared_task
from kafka import KafkaConsumer
import json, django, os
from .models import LogEvent
from django.utils import timezone

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'logTraffic_monitor.settings'
)
django.setup()

@shared_task
def consumer_kafka_logs():
    consumer = KafkaConsumer(
        'log_events',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id="log-consumer-group"
    )

    for message in consumer:
        log_data = message.value
        print(log_data)

        if "timestamp" not in log_data or not log_data["timestamp"]:
            log_data["timestamp"] = timezone.now()

        LogEvent.objects.create(**log_data)



# sudo docker exec -it reverent_aryabhata  /opt/kafka/bin/kafka-topics.sh --create --topic log_events --bootstrap-server localhost:9092
# sudo docker exec -it reverent_aryabhata  /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
# sudo docker exec -it reverent_aryabhata  /opt/kafka/bin/kafka-topics.sh --delete --topic log_event --bootstrap-server localhost:9092
