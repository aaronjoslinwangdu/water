import binascii

import machine

from lib.umqtt import simple

env: dict[str, str] = {}
with open(".env", "r") as file:
    for line in file:
        if not line or "=" not in line:
            continue
        key, val = line.split("=", 1)
        env[key] = val.strip()


def handle_message(topic_encoded: bytes, msg_encoded: bytes) -> None:
    topic = topic_encoded.decode()
    msg = msg_encoded.decode()
    print(f"topic: {topic}, msg: {msg}")


client = simple.MQTTClient(
    client_id=binascii.hexlify(machine.unique_id()),
    server=env.get("MQTT_HOST"),
    port=int(env.get("MQTT_PORT", "1833")),
)

client.set_callback(handle_message)
client.connect()
client.subscribe(env.get("MQTT_TOPIC", "water").encode())

while True:
    client.wait_msg()
