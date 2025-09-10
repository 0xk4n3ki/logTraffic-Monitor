from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
import json
from django.conf import settings
from logs.utils import process_log_message

class Command(BaseCommand):
    help = "Consume log messages from Kafka and save to DB"

    def handle(self, *args, **options):
        consumer = KafkaConsumer(
            'log_events',
            bootstrap_servers=settings.KAFKA_BROKER_URL,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="log-consumer-group",
        )

        self.stdout.write(self.style.SUCCESS('Kafka consumer started...'))

        for message in consumer:
            log_data = message.value
            self.stdout.write(f"consumed log: {log_data}")

            try:
                process_log_message(log_data)
            except Exception as e:
                self.stderr.write(f"error processing log: {e}")