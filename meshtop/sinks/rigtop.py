"""TCP NMEA server for rigtop (gps2ip source, default port 10111).

Identical wire format to nmea_server but on a separate port so rigtop
and pi-star can both connect simultaneously.
"""

from meshtop.config import RigtopConfig
from meshtop.position import Position
from meshtop.sinks.nmea_server import NmeaServer, NmeaServerConfig


class RigtopSink:
    """Thin wrapper around NmeaServer using RigtopConfig port."""

    def __init__(self, cfg: RigtopConfig) -> None:
        self._server = NmeaServer(NmeaServerConfig(enabled=cfg.enabled, port=cfg.port))

    def start(self) -> None:
        self._server.start()

    def stop(self) -> None:
        self._server.stop()

    def send(self, pos: Position) -> None:
        self._server.send(pos)
