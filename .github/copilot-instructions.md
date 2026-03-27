# Copilot Instructions — meshtop

## Project overview

**meshtop** is a Meshtastic GPS bridge and TUI dashboard — a Python 3.12+ terminal application
that receives position and telemetry from Meshtastic mesh-radio nodes (via BLE, serial, or MQTT)
and forwards to external consumers: pi-star NMEA server, APRS-IS, gpsd, and rigtop.

## Architecture

```
meshtop/
  cli.py             — Typer entry point; builds sources/sinks, starts TUI
  tui.py             — Full-screen Textual TUI dashboard (MeshtopApp)
  config.py          — Pydantic models + TOML loader (Config, LoraSourceConfig, ChannelConfig, …)
  position.py        — Position dataclass — shared data contract between sources and sinks
  mesh_sender.py     — Send text/position/traceroute via BLE/serial/TCP iface
  sources/
    meshtastic.py    — MQTT source (MeshtasticSource) — decrypts + decodes ServiceEnvelope
    serial.py        — USB-serial NMEA source (pyserial + pynmea2)
    ble.py           — BLE source (bleak + meshtastic BLEInterface)
    tcp.py           — TCP source (meshtastic TCPInterface)
    _mesh_decode.py  — Shared decoder for BLE/serial dict packets
  sinks/
    nmea_server.py   — TCP NMEA server (pi-star / NMEA consumers, port 10110)
    aprs.py          — APRS-IS beacon (callsign, passcode, interval)
    gpsd.py          — gpsd-compatible JSON server (port 2947)
    rigtop.py        — NMEA TCP server consumed by rigtop as gps2ip source
```

## Key conventions

- **Python 3.12+** — use modern syntax: `X | Y` unions, PEP 695 type aliases where appropriate
- **Pydantic v2** for all config models; use `field_validator` not `validator`
- **loguru** for logging (`logger.info`, `logger.debug`, etc.); never use `print` for log output
- **Textual** (v0.80+) for the TUI; widgets communicate via `Message` subclasses posted to the app
- **uv** for package management; `uv sync` / `uv run`; never `pip install` directly in dev
- **ruff** for linting + formatting (line length 100, target py312)
- All sinks run as background threads; the TUI main thread owns the Textual event loop
- `position.py` is the only shared data contract — no sink imports a source and vice versa
- Config is loaded once in `cli.main()` and passed down; never re-read TOML at runtime
- Thread-safe TUI updates use `app.call_from_thread()` or `app.post_message()`

## Meshtastic / ham radio domain context

- **Meshtastic** — LoRa mesh-radio firmware for ESP32/nRF52 devices; nodes relay packets over RF
- **ServiceEnvelope** — MQTT wrapper protobuf; inner `MeshPacket` is encrypted with AES-CTR
- **PSK** — Pre-Shared Key; `AQ==` (1 byte 0x01) is the Meshtastic shorthand for the default
  128-bit key (`D4F1BB3A20290759F0BCFFABCF4E4DF6`); full 16/32-byte AES keys also accepted
- **Primary channel** (index 0) — no user-assigned name; uses `primary_key` in config
- **Named channels** (index 1+) — e.g. `TSS`, each with its own enable/encrypt/key settings
- **Node ID** — `!XXXXXXXX` (8 hex digits); short name is 4 chars (e.g. `TSSV`)
- **APRS-IS** — internet gateway for APRS position beacons; callsign + passcode required
- **gpsd** — GPS daemon protocol; meshtop serves a compatible JSON stream on port 2947
- **pi-star** — hotspot firmware that consumes NMEA position over TCP (port 10110)

## Code review focus areas

When reviewing PRs, pay attention to:
1. **Thread safety** — TUI widgets must only be updated via `call_from_thread` or `post_message`
2. **AES-CTR decryption** — nonce is `packet.id (8 bytes LE) + packet.from (8 bytes LE)`; wrong
   nonce or key silently produces garbage — log decrypt failures at DEBUG, not ERROR
3. **PSK expansion** — `expand_psk()` in `config.py` handles 0/1/16/32-byte keys; new key fields
   must use `_validate_psk()` as a `field_validator`
4. **Config validation** — new config fields should use pydantic validators, not runtime checks
5. **Socket/serial errors** — sources and sinks must handle `OSError` / `ConnectionError` and
   reconnect gracefully without crashing the TUI
6. **Channel filtering** — the `enabled` flag on `ChannelConfig` must be respected before
   attempting decryption or dispatching callbacks
