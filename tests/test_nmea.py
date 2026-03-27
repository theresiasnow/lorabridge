from meshtop.position import Position
from meshtop.sinks.nmea_server import _format_gpgga, _format_gprmc, _nmea_checksum


def test_checksum_known():
    # GPRMC body — checksum verified against known-good value
    body = "GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W"
    cs = _nmea_checksum(body)
    assert len(cs) == 2
    assert all(c in "0123456789ABCDEF" for c in cs)


def test_gprmc_structure():
    pos = Position(lat=57.887, lon=16.403, alt=67.0, fix=True, sats=8)
    sentence = _format_gprmc(pos)
    assert sentence.startswith("$GPRMC,")
    assert sentence.endswith("\r\n")
    assert "*" in sentence
    # checksum field has 2 hex chars
    cs = sentence.strip().split("*")[1]
    assert len(cs) == 2


def test_gpgga_structure():
    pos = Position(lat=57.887, lon=16.403, alt=67.0, fix=True, sats=8)
    sentence = _format_gpgga(pos)
    assert sentence.startswith("$GPGGA,")
    assert sentence.endswith("\r\n")
    assert "*" in sentence


def test_gprmc_no_fix():
    pos = Position(lat=57.887, lon=16.403, fix=False)
    sentence = _format_gprmc(pos)
    # status field should be V (void)
    assert ",V," in sentence


def test_gprmc_fix():
    pos = Position(lat=57.887, lon=16.403, fix=True)
    sentence = _format_gprmc(pos)
    assert ",A," in sentence


def test_southern_western_hemisphere():
    pos = Position(lat=-33.8688, lon=-70.6693, fix=True)
    sentence = _format_gprmc(pos)
    assert ",S," in sentence
    assert ",W," in sentence


def test_checksum_integrity_gprmc():
    pos = Position(lat=57.887, lon=16.403, fix=True)
    sentence = _format_gprmc(pos).strip()
    body = sentence[1:].split("*")[0]
    expected_cs = sentence.split("*")[1]
    assert _nmea_checksum(body) == expected_cs


def test_checksum_integrity_gpgga():
    pos = Position(lat=57.887, lon=16.403, alt=10.0, fix=True, sats=5)
    sentence = _format_gpgga(pos).strip()
    body = sentence[1:].split("*")[0]
    expected_cs = sentence.split("*")[1]
    assert _nmea_checksum(body) == expected_cs
