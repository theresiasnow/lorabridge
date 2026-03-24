## v0.2.0 (2026-03-24)

### Feat

- **tui**: add Textual TUI with BLE/serial sources and multi-sink support
- **source**: implement Meshtastic MQTT source with protobuf decoding

### Fix

- **tui**: use localNode.nodeNum to identify local node for top-right panel
- **ble**: force clean exit; timeout BLE close to prevent hang on quit
- **tui**: show local node in top-right panel; update header on source change

### Refactor

- rename project from lorabridge to meshtop
