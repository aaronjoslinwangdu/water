from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    MQTT_HOST: str
    MQTT_PORT: int
    MQTT_TOPIC: str


@lru_cache
def get_settings():
    return Settings()
