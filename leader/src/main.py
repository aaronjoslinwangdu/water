from contextlib import asynccontextmanager
from typing import Annotated

import aiomqtt
from fastapi import Depends, FastAPI, Request

from config import Settings, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    async with aiomqtt.Client(
        hostname=settings.MQTT_HOST,
        port=settings.MQTT_PORT,
    ) as client:
        app.state.mqtt = client
        yield


async def get_mqtt(request: Request) -> aiomqtt.Client:
    return request.app.state.mqtt


app = FastAPI(lifespan=lifespan)


@app.post("/water")
async def water(
    client: Annotated[aiomqtt.Client, Depends(get_mqtt)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    print("publishing")
    await client.publish(topic=settings.MQTT_TOPIC, payload="hi")
