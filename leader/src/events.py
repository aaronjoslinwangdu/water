from typing import Annotated, Literal

from pydantic import BaseModel, Field, PositiveInt


class WaterEvent(BaseModel):
    type: Literal["water"] = "water"
    client_id: str
    duration_ms: PositiveInt


class PhotoEvent(BaseModel):
    type: Literal["photo"] = "photo"
    client_id: str
    flush: bool

class StateEvent(BaseModel):
    type: Literal["alive"] | Literal["dead"]
    client_id: str


Event = Annotated[WaterEvent | PhotoEvent, Field(discriminator="type")]
