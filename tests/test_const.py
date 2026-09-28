"""Test constants for ha_illuminance."""

from datetime import timedelta

from custom_components.ha_illuminance.const import (
    CONF_FALLBACK,
    DEFAULT_FALLBACK,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL_MIN,
    DOMAIN,
    LUX_PER_WPSM,
    MIN_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL_MIN,
    OLD_DOMAIN,
)


def test_constants():
    """Test constant values."""
    assert DOMAIN == "ha_illuminance"
    assert OLD_DOMAIN == "illuminance"
    assert DEFAULT_NAME == "Illuminance"
    assert MIN_SCAN_INTERVAL_MIN == 0.5
    assert MIN_SCAN_INTERVAL == timedelta(minutes=0.5)
    assert DEFAULT_SCAN_INTERVAL_MIN == 5
    assert DEFAULT_SCAN_INTERVAL == timedelta(minutes=5)
    assert DEFAULT_FALLBACK == 10
    assert LUX_PER_WPSM == 120
    assert CONF_FALLBACK == "fallback"
