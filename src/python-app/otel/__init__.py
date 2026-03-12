import logging
from logging import Logger

from models.config import config

# Metric imports
from opentelemetry import metrics as metrics
from opentelemetry._logs import set_logger_provider

# Log Imports
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import MeterProvider, get_meter_provider, set_meter_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import (
    Counter,
    Histogram,
    MeterProvider,
    ObservableCounter,
    ObservableUpDownCounter,
    UpDownCounter,
)
from opentelemetry.sdk.metrics.export import AggregationTemporality, PeriodicExportingMetricReader

# OpenTelemetry Imports
from opentelemetry.sdk.resources import Resource


def setupMetricResources(resource: Resource) -> MeterProvider:
    otlp_metric_exporter_config = {
        "endpoint": f"{config.otlp_metrics_api}",
        "preferred_temporality": {
            Counter: AggregationTemporality.DELTA,
            UpDownCounter: AggregationTemporality.CUMULATIVE,
            Histogram: AggregationTemporality.DELTA,
            ObservableCounter: AggregationTemporality.DELTA,
            ObservableUpDownCounter: AggregationTemporality.CUMULATIVE,
        },
    }
    if config.otlp_token:
        otlp_metric_exporter_config["headers"] = {"Authorization": f"Api-Token {config.otlp_token.get_secret_value()}"}

    exporter = OTLPMetricExporter(**otlp_metric_exporter_config)

    reader = PeriodicExportingMetricReader(exporter)
    provider = MeterProvider(metric_readers=[reader], resource=resource)
    set_meter_provider(provider)
    return get_meter_provider().get_meter(config.otlp_meter_provider_name, config.otlp_meter_provider_version)


def setupLoggingResources(resource: Resource) -> Logger:
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    otlp_log_exporter_config = {"endpoint": config.otlp_logs_api}

    if config.otlp_token:
        otlp_log_exporter_config["headers"] = {"Authorization": f"Api-Token {config.otlp_token.get_secret_value()}"}

    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter(**otlp_log_exporter_config)))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(handler)


def setupOTelObjects(service_name: str = "Python-App", service_version: str = "0.1.0") -> tuple[MeterProvider]:
    resource = Resource.create({"service.name": service_name, "service.version": service_version})
    setupLoggingResources(resource)

    return setupMetricResources(resource)
