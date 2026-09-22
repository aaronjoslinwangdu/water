import asyncio
import json
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

import aiomqtt
from fastapi import Depends, FastAPI, Request

from config import Settings, get_settings
from events import Event, StateEvent


async def update_state(client: aiomqtt.Client, connected: set[str]) -> None:
    async for msg in client.messages:
        payload = msg.payload.decode()
        event = StateEvent.model_validate_json(json.loads(payload))
        match event.type:
            case "alive":
                connected.add(event.client_id)
            case "dead":
                connected.discard(event.client_id)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    async with aiomqtt.Client(
        hostname=settings.MQTT_HOST,
        port=settings.MQTT_PORT,
    ) as client:
        await client.subscribe(f"{settings.MQTT_TOPIC}/state")
        app.state.connected = set()
        task = asyncio.create_task(
            update_state(client=client, connected=app.state.connected)
        )
        app.state.mqtt = client
        yield
        try:
            await task
        except asyncio.CancelledError:
            pass


def get_mqtt(request: Request) -> aiomqtt.Client:
    return request.app.state.mqtt


app = FastAPI(lifespan=lifespan)


@app.post("/events")
async def publish(
    client: Annotated[aiomqtt.Client, Depends(get_mqtt)],
    settings: Annotated[Settings, Depends(get_settings)],
    event: Event,
):
    payload = json.dumps(event.model_dump_json())
    topic = f"{settings.MQTT_TOPIC}/{event.client_id}/cmd"
    print(f"{datetime.now()} - Publishing to topic '{topic}': '{payload}'")
    await client.publish(topic=topic, payload=payload)
