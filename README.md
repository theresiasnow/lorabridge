# lorabridge

GPS bridge for Meshtastic devices — reads position, telemetry and messages via Bluetooth (BLE), USB serial or LoRa/MQTT and forwards to pi-star, APRS-IS, gpsd, and rigtop.

## Connecting via Bluetooth (BLE)

Before connecting from lorabridge, two things must be true:

1. **Disable Bluetooth PIN on the device.**
   In the Meshtastic app: *Radio Config → Bluetooth → Pairing Mode → No PIN* (or Fixed with PIN disabled).
   With PIN enabled, Windows pairing fails silently and the app cannot connect.

2. **Disconnect any other app first.**
   Meshtastic devices only allow one BLE connection at a time. Close the Meshtastic mobile app (or turn off Bluetooth on the phone) before running `ble on` in lorabridge.

## Connecting via USB serial

Enable Serial Console on the device:
*Radio Config → Module Config → Serial → Enabled: ON*

Without this the device does not speak the Meshtastic protocol over USB and the connection will time out.

## Usage

```
uv run lorabridge                        # start with TUI (reads lorabridge.toml)
uv run lorabridge --source ble           # connect via Bluetooth on startup
uv run lorabridge --source serial --port COM4
uv run lorabridge --no-tui --debug       # plain console output with debug logging
```

### TUI commands

| Command | Description |
|---|---|
| `ble on` | Scan for nearby Meshtastic devices and connect via BLE |
| `ble off` | Disconnect BLE |
| `serial on` | Pick a serial port and connect |
| `serial off` | Disconnect serial |
| `beacon on/off` | Enable or disable APRS beacon |
| `msg <NODE_ID> <text>` | Send a Meshtastic text message |
| `pos` | Show current position |
| `help` | List all commands |
