from datetime import datetime
from random import randint
from time import sleep

from helpers import logger
from models.config import config
from otel import setupOTelObjects


def main():
    meter = setupOTelObjects()
    counter = meter.create_counter(
        name=f"{config.metric_prefix}.{config.team_name}.{config.product}",
        description="The number of requests we received",
    )
    shared_counter = meter.create_counter(
        name=f"{config.metric_prefix}.{config.shared_metric_name}",
        description="A universal metric to help demonstrate how the metric would be presented differently for each user",
    )
    while True:
        shared_counter.add(randint(1, 10), {"team": config.team_name, "product": config.product})
        counter.add(1, {"team": config.team_name, "product": config.product})
        logger.info(
            f"Successfully emitted metrics for Team: '{config.team_name}', Product: '{config.product}' at Time: '{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}'"
        )
        sleep(config.sleep_timer)


if __name__ == "__main__":
    main()
