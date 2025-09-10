import logging
from decouple import config
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.kafka import KafkaInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry import trace, metrics

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry import _logs

OTEL_EXPORTER_OTLP_ENDPOINT = config("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")

resource = Resource(attributes={
    SERVICE_NAME: "log-monitor-service"
})

# traces
trace_provider = TracerProvider(resource=resource)
otlp_span_exporter = OTLPSpanExporter(endpoint=f"{OTEL_EXPORTER_OTLP_ENDPOINT}/v1/traces")
trace_provider.add_span_processor(BatchSpanProcessor(otlp_span_exporter))
trace.set_tracer_provider(trace_provider)

# metrics
metric_exporter = OTLPMetricExporter(endpoint=f"{OTEL_EXPORTER_OTLP_ENDPOINT}/v1/metrics")
reader = PeriodicExportingMetricReader(metric_exporter)
provider = MeterProvider(metric_readers=[reader], resource=resource)
metrics.set_meter_provider(provider)

# logs
logger_provider = LoggerProvider(resource=resource)
_logs.set_logger_provider(logger_provider)

log_exporter = OTLPLogExporter(endpoint=f"{OTEL_EXPORTER_OTLP_ENDPOINT}/v1/logs")
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

app_logger = logging.getLogger('app.logs')
app_logger.setLevel(logging.INFO)
otel_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.getLogger().addHandler(otel_handler)

logging.getLogger('opentelemetry').setLevel(logging.ERROR)
logging.getLogger('kafka').setLevel(logging.ERROR)

# instrumentation
DjangoInstrumentor().instrument()
CeleryInstrumentor().instrument()
KafkaInstrumentor().instrument()

logger = logging.getLogger('app.logs')