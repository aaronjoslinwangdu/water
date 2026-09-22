import binascii
import json
import time

import machine

from lib.umqtt import simple

env: dict[str, str] = {}
with open(".env", "r") as file:
    for line in file:
        if not line or "=" not in line:
            continue
        key, val = line.split("=", 1)
        env[key] = val.strip()

id = binascii.hexlify(machine.unique_id())
base_topic = env.get("MQTT_TOPIC", "water")
state_topic = f"{base_topic}/state".encode()
cmd_topic = f"{base_topic}/{id.decode()}/cmd".encode()


def handle_message(topic_encoded: bytes, msg_encoded: bytes) -> None:
    topic = topic_encoded.decode()
    msg = json.loads(msg_encoded.decode())
    print(f"{time.time()} - Consumed on '{topic}': {msg}")


client = simple.MQTTClient(
    client_id=id,
    server=env.get("MQTT_HOST"),
    port=int(env.get("MQTT_PORT", "1883")),
)

client.set_last_will(
    topic=state_topic, msg=json.dumps({"type": "dead", "client_id": id.decode()})
)
client.set_callback(handle_message)
client.connect()
client.subscribe(cmd_topic)
client.publish(topic=state_topic, msg=json.dumps({"type": "alive", "client_id": id.decode()}))

while True:
    client.wait_msg()
