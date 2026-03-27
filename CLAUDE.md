# meshtop — Claude Code instructions

## Project layout

```
meshtop/
  __init__.py
  __main__.py
  cli.py           # entry point, argument parsing, startup/shutdown, rich output
  config.py        # Pydantic models + TOML loader
  position.py      # Position dataclass (lat, lon, alt, speed, course, fix)
  sources/
    __init__.py
    serial.py      # USB-serial (Meshtastic device, pyserial)
    tcp.py         # TCP source (Meshtastic TCPInterface)
    ble.py         # BLE source (bleak + meshtastic BLEInterface)
    lora.py        # LoRa-gateway via MQTT (paho-mqtt)
  sinks/
    __init__.py
    nmea_server.py # TCP NMEA server for pi-star (default port 10110)
    aprs.py        # APRS-IS beacon (callsign, passcode, interval)
    gpsd.py        # gpsd-compatible JSON server (port 2947)
    rigtop.py      # NMEA TCP server consumed by rigtop as gps2ip source
tests/
  test_config.py
  test_nmea.py
```

## Key conventions

- Config is loaded once in `cli.main()` — pass values down, don't re-read TOML at runtime
- Sources produce `Position` objects via callback; sinks consume them
- All sinks run as background threads; main thread owns the source loop
- `position.py` is the shared data contract — no sink/source imports the other

## Running

```
uv run meshtop --help
uv run meshtop --source serial --port COM3
uv run meshtop --source tcp --config meshtop.toml
uv run pytest tests/
uv run ruff check meshtop/
```
