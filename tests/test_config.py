import pytest

from meshtop.config import Config, SourceConfig, expand_psk, load_config


def test_default_config():
    cfg = Config()
    assert cfg.source.type == "none"
    assert cfg.nmea_server.enabled is True
    assert cfg.gpsd.enabled is True
    assert cfg.aprs.enabled is False


def test_expand_psk_default():
    key = expand_psk("AQ==")
    assert len(key) == 16


def test_expand_psk_aes128():
    import base64
    raw = bytes(range(16))
    key = expand_psk(base64.b64encode(raw).decode())
    assert key == raw


def test_expand_psk_aes256():
    import base64
    raw = bytes(range(32))
    key = expand_psk(base64.b64encode(raw).decode())
    assert key == raw


def test_expand_psk_empty():
    assert expand_psk("") == b""


def test_expand_psk_invalid_length():
    import base64
    with pytest.raises(ValueError):
        expand_psk(base64.b64encode(bytes(5)).decode())


def test_source_config_tcp_defaults():
    cfg = SourceConfig(type="tcp")
    assert cfg.tcp.port == 4403


def test_load_config_missing_file(tmp_path):
    cfg = load_config(tmp_path / "nonexistent.toml")
    assert isinstance(cfg, Config)


def test_load_config_from_toml(tmp_path):
    toml = tmp_path / "test.toml"
    toml.write_text('[source]\ntype = "tcp"\n\n[source.tcp]\nhost = "10.0.0.1"\n')
    cfg = load_config(toml)
    assert cfg.source.type == "tcp"
    assert cfg.source.tcp.host == "10.0.0.1"
