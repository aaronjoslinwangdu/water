def do_connect() -> None:
    import network

    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to network")
        env: dict[str, str] = {}
        with open(".env", "r") as file:
            for line in file:
                if not line or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                env[key] = val.strip()

        wlan.connect(env.get("SSID"), env.get("PASSWORD"))
        while not wlan.isconnected():
            pass
    print("Successfully connected")


do_connect()
