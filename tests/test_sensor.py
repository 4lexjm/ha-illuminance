"""Test sensor calculations and mappings for ha_illuminance."""

import math

from custom_components.ha_illuminance.sensor import (
    MAPPING,
    EntityStatus,
    Mode,
    _illumiance,
)


def test_modes():
    """Test supported modes."""
    assert Mode.normal.name == "normal"
    assert Mode.simple.name == "simple"
    assert Mode.irradiance.name == "irradiance"


def test_illumiance_calculation():
    """Test mathematical calculation of illuminance from solar elevation."""
    # Sun directly overhead (90 degrees elevation)
    overhead = _illumiance(90)
    assert 100000 < overhead < 150000

    # Sun at 45 degrees
    midday = _illumiance(45)
    assert 50000 < midday < overhead

    # Sun at horizon (0 degrees)
    horizon = _illumiance(0)
    assert 0 <= horizon < midday

    # At negative elevation (night), returns a valid finite number
    night = _illumiance(-10)
    assert math.isfinite(night)


def test_condition_mappings():
    """Test that default weather conditions mapping covers expected conditions."""
    all_conditions = set()
    for divisor, conditions in MAPPING:
        assert divisor in (10, 5, 2, 1)
        for cond in conditions:
            all_conditions.add(cond)

    assert "cloudy" in all_conditions
    assert "rainy" in all_conditions
    assert "sunny" in all_conditions


def test_entity_status_enum():
    """Test EntityStatus enum states."""
    assert EntityStatus.OK_CONDITION != EntityStatus.OK_CLOUD
    assert EntityStatus.NO_ATTRIBUTION != EntityStatus.NOT_SEEN
