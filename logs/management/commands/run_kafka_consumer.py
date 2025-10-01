from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
import json
from django.conf import settings
from logs.utils import process_log_message
from prometheus_client import start_http_server, Counter, Histogram

messages_consumed = Counter("log_messages_total", 
                            "Total log messages consumed")
consume_latency = Histogram("log_consume_latency_seconds",
                            "Log processing time")

class Command(BaseCommand):
    help = "Run kafka consumer to process log_events"

    def handle(self, *args, **options):
        consumer = KafkaConsumer(
            "log_events",
            bootstrap_servers=settings.KAFKA_BROKER_URL,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="log-consumer-group",
        )

        self.stdout.write(self.style.SUCCESS("Kafka consumer started..."))

        start_http_server(8001)

        for message in consumer:
            log_data = message.value
            self.stdout.write(self.style.WARNING(f"Received: {log_data}"))
            process_log_message(log_data)