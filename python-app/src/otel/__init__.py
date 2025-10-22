import logging, sys
from logging import Logger
from models.config import config

# OpenTelemetry Imports
from opentelemetry.sdk.resources import Resource

# Metric imports
from opentelemetry import metrics as metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import set_meter_provider, get_meter_provider, MeterProvider
from opentelemetry.sdk.metrics import (
    Counter,
    Histogram,
    MeterProvider,
    ObservableCounter,
    ObservableUpDownCounter,
    UpDownCounter,
)
from opentelemetry.sdk.metrics.export import AggregationTemporality, PeriodicExportingMetricReader

# Log Imports
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider


def setupMetricResources(resource: Resource) -> MeterProvider:
    exporter = OTLPMetricExporter(
        endpoint=f"{config.otlp_metrics_api}",
        headers={"Authorization": f"Api-Token {config.otlp_token.get_secret_value()}"},
        preferred_temporality={
            Counter: AggregationTemporality.DELTA,
            UpDownCounter: AggregationTemporality.CUMULATIVE,
            Histogram: AggregationTemporality.DELTA,
            ObservableCounter: AggregationTemporality.DELTA,
            ObservableUpDownCounter: AggregationTemporality.CUMULATIVE,
        },
    )

    reader = PeriodicExportingMetricReader(exporter)
    provider = MeterProvider(metric_readers=[reader], resource=resource)
    set_meter_provider(provider)
    return get_meter_provider().get_meter(config.otlp_meter_provider_name, config.otlp_meter_provider_version)

def setupLoggingResources(resource: Resource) -> Logger:
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter(
            endpoint = config.otlp_logs_api,
            headers = {"Authorization": f"Api-Token {config.otlp_token.get_secret_value()}"}
        ))
    )
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

    # Attach OTLP handler to root logger
    logger = logging.getLogger(config.otlp_logger_provider_name)
    # logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger

def setupOTelObjects(service_name: str = "Python-App", service_version: str = "0.1.0") -> tuple[MeterProvider, Logger]:
    resource = Resource.create({
        "service.name": service_name,
        "service.version": service_version
    })

    return (setupMetricResources(resource), setupLoggingResources(resource))
