def get_env() -> dict[str, str]:
    env: dict[str, str] = {}
    with open(".env", "r") as file:
        for line in file:
            if not line or "=" not in line:
                continue
            key, val = line.split("=", 1)
            env[key] = val.strip()
    return env

def do_connect(env: dict[str, str]):
    import network
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(env.get("SSID"), env.get("PASSWORD"))
        while not wlan.isconnected():
            pass
    ip = wlan.ipconfig("addr4")
    print(f"Network config: {ip}")

do_connect(get_env())
