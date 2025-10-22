import json
from typing import Dict

from pydantic import AnyHttpUrl, BaseSettings, Field, SecretStr


class Config(BaseSettings):
    otlp_metrics_api: AnyHttpUrl = Field(env="OTLP_METRICS_URL")
    otlp_logs_api: AnyHttpUrl = Field(env="OTLP_LOGS_URL")
    otlp_token: SecretStr = Field(env="DT_API_TOKEN")
    otlp_meter_provider_name: str = Field("my-meter", env="OTLP_METER_PROVIDER_NAME")
    otlp_meter_provider_version: str = Field("0.1.0", env="OTLP_METER_PROVIDER_VERSION")
    team_name: str = Field(env="DT_COSTCENTER")
    metric_prefix: str = Field("poc", env="DT_METRIC_PREFIX")
    product: str = Field(env="DT_PRODUCT")

    def as_serialized_dict(self) -> Dict[str, str]:
        return json.loads(self.json())


config = Config()
