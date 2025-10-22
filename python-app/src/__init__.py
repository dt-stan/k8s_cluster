from helpers import logger
from time import sleep
from datetime import datetime
from models.config import config
from otel import setupOTelObjects


def main():
    meter = setupOTelObjects()
    counter = meter.create_counter(
        name=f"{config.metric_prefix}.{config.team_name}.{config.product}",
        description="The number of requests we received",
    )
    while True:
        counter.add(1, {"team": config.team_name, "product": config.product})
        logger.info(f"Successfully emitted metric for Team: '{config.team_name}', Product: '{config.product}' at Time: '{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}'")
        sleep(config.sleep_timer)


if __name__ == "__main__":
    main()
