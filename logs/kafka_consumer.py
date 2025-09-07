import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logTraffic_monitor.settings')
django.setup()


from kafka import KafkaConsumer
import json
from logs.models import LogEvent

consumer = KafkaConsumer('log_events', bootstrap_servers='localhost:9092',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:
    log_data = message.value
    print(log_data)
    LogEvent.objects.create(**log_data)



# sudo docker exec -it reverent_aryabhata  /opt/kafka/bin/kafka-topics.sh --create --topic log_events --bootstrap-server localhost:9092
# sudo docker exec -it reverent_aryabhata  /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
# sudo docker exec -it reverent_aryabhata  /opt/kafka/bin/kafka-topics.sh --delete --topic log_event --bootstrap-server localhost:9092

