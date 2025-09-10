from django.utils import timezone
from .models import LogEvent
from opentelemetry import trace
import logging

logger = logging.getLogger("app.logs")
tracer = trace.get_tracer(__name__)

def process_log_message(log_data):
    if "timestamp" not in log_data or not log_data["timestamp"]:
        log_data["timestamp"] = timezone.now().isoformat()

    with tracer.start_as_current_span("process_log_message"):
        LogEvent.objects.create(**log_data)

        log_record_data = {k: v for k, v in log_data.items() if k != "message"}
        logger.info(log_data.get("message", "log_event"), extra=log_record_data) 
              