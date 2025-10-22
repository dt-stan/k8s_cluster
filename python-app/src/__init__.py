from otel import setupOTelObjects
from models.config import config


def main():
    meter, logger = setupOTelObjects()
    counter = meter.create_counter(name=f"{config.metric_prefix}.{config.team_name}.{config.product}", description="The number of requests we received")
    counter.add(1, {"foo": config.team_name})
    logger.info("FOOOBARR")


if __name__ == "__main__":
    main()
