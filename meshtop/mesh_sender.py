"""Send Meshtastic text messages via TCP or serial interface."""

from __future__ import annotations

from meshtop.config import LoraSourceConfig


def send_text(cfg: LoraSourceConfig, serial_port: str, dest: str, text: str) -> str:
    """Send a Meshtastic text message. Returns a status string.

    Tries TCP first (device_host), falls back to serial (serial_port).
    dest: node ID like "!7a78e5e3" or "^all" for broadcast.
    """
    if cfg.device_host:
        from meshtastic.tcp_interface import TCPInterface

        with TCPInterface(cfg.device_host) as iface:
            iface.sendText(text, destinationId=dest)
        return f"Sent to {dest} via TCP ({cfg.device_host})"

    if serial_port:
        from meshtastic.serial_interface import SerialInterface

        with SerialInterface(serial_port) as iface:
            iface.sendText(text, destinationId=dest)
        return f"Sent to {dest} via serial ({serial_port})"

    raise ValueError(
        "No send interface — set source.lora.device_host (TCP) "
        "or use --port COM9 (serial) in meshtop.toml"
    )
