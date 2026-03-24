"""Send packets to the Meshtastic mesh.

Prefers the already-running BLE/serial interface (iface parameter) to avoid
opening a second connection. Falls back to TCP (device_host) or a fresh serial
connection when no live interface is available.
"""

from __future__ import annotations

from typing import Any

from meshtop.config import LoraSourceConfig


def _fallback_iface(cfg: LoraSourceConfig, serial_port: str):
    """Context-manager that yields a fresh send interface (TCP or serial)."""
    if cfg.device_host:
        from meshtastic.tcp_interface import TCPInterface
        return TCPInterface(cfg.device_host)
    if serial_port:
        from meshtastic.serial_interface import SerialInterface
        return SerialInterface(serial_port)
    raise ValueError(
        "No send interface — set source.lora.device_host (TCP) "
        "or use --port (serial) in meshtop.toml"
    )


def send_text(
    cfg: LoraSourceConfig,
    serial_port: str,
    dest: str,
    text: str,
    iface: Any = None,
) -> str:
    """Send a Meshtastic text message. Returns a status string."""
    if iface is not None:
        iface.sendText(text, destinationId=dest)
        return f"Sent to {dest}"
    with _fallback_iface(cfg, serial_port) as i:
        i.sendText(text, destinationId=dest)
    return f"Sent to {dest} via {'TCP' if cfg.device_host else 'serial'}"


def send_position(iface: Any, lat: float, lon: float, alt: float = 0) -> None:
    """Broadcast a position packet to the mesh."""
    iface.sendPosition(lat, lon, int(alt))


def send_traceroute(iface: Any, dest: str) -> None:
    """Send a traceroute request to dest (node ID like '!7a78e5e3')."""
    iface.sendTraceRoute(dest, hopLimit=7)
