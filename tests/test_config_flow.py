"""Test config flow for ha_illuminance."""

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import (
    CONF_ENTITY_ID,
    CONF_MODE,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
    CONF_UNIQUE_ID,
)

from custom_components.ha_illuminance.config_flow import (
    IlluminanceConfigFlow,
    IlluminanceOptionsFlow,
)
from custom_components.ha_illuminance.const import (
    CONF_FALLBACK,
)


@pytest.mark.asyncio
async def test_user_flow():
    """Test standard user flow from name to options to creation."""
    flow = IlluminanceConfigFlow()
    flow.hass = MagicMock()

    # Step user -> shows name form
    result = await flow.async_step_user()
    assert result["type"] == "form"
    assert result["step_id"] == "name"

    # Step name with input -> shows options form
    result = await flow.async_step_name({CONF_NAME: "My Illuminance Sensor"})
    assert result["type"] == "form"
    assert result["step_id"] == "options"

    # Step options with input -> creates entry
    options_data = {
        CONF_MODE: "normal",
        CONF_SCAN_INTERVAL: 5.0,
        CONF_ENTITY_ID: "weather.home",
        CONF_FALLBACK: 10,
    }
    result = await flow.async_step_options(options_data)
    assert result["type"] == "create_entry"
    assert result["title"] == "My Illuminance Sensor"
    assert result["options"][CONF_MODE] == "normal"
    assert result["options"][CONF_SCAN_INTERVAL] == 5.0


@pytest.mark.asyncio
async def test_import_flow_with_timedelta():
    """Test importing configuration with scan_interval as timedelta."""
    flow = IlluminanceConfigFlow()
    flow.hass = MagicMock()
    flow.async_set_unique_id = AsyncMock(return_value=None)

    data = {
        CONF_NAME: "Imported Sensor",
        CONF_UNIQUE_ID: "unique_imported",
        CONF_MODE: "simple",
        CONF_SCAN_INTERVAL: timedelta(minutes=10),
        CONF_ENTITY_ID: "weather.forecast",
    }
    result = await flow.async_step_import(data)
    assert result["type"] == "create_entry"
    assert result["title"] == "Imported Sensor"
    assert result["options"][CONF_SCAN_INTERVAL] == 10.0


@pytest.mark.asyncio
async def test_import_flow_with_float():
    """Test importing configuration with scan_interval as float (migration)."""
    flow = IlluminanceConfigFlow()
    flow.hass = MagicMock()
    flow.async_set_unique_id = AsyncMock(return_value=None)

    data = {
        CONF_NAME: "Migrated Sensor",
        CONF_UNIQUE_ID: "unique_migrated",
        CONF_MODE: "normal",
        CONF_SCAN_INTERVAL: 5.0,
    }
    result = await flow.async_step_import(data)
    assert result["type"] == "create_entry"
    assert result["title"] == "Migrated Sensor"
    assert result["options"][CONF_SCAN_INTERVAL] == 5.0


def test_supports_options_flow():
    """Test options flow support check."""
    entry_user = ConfigEntry(source="user")
    assert IlluminanceConfigFlow.async_supports_options_flow(entry_user) is True

    entry_import = ConfigEntry(source=SOURCE_IMPORT)
    assert IlluminanceConfigFlow.async_supports_options_flow(entry_import) is False


@pytest.mark.asyncio
async def test_options_flow():
    """Test options flow updates."""
    entry = ConfigEntry(
        options={
            CONF_MODE: "normal",
            CONF_SCAN_INTERVAL: 5.0,
        }
    )
    flow = IlluminanceOptionsFlow(entry)
    flow.hass = MagicMock()

    result = await flow.async_step_options()
    assert result["type"] == "form"
    assert result["step_id"] == "options"

    result = await flow.async_step_options({CONF_MODE: "simple", CONF_SCAN_INTERVAL: 10.0})
    assert result["type"] == "create_entry"
    assert result["data"][CONF_MODE] == "simple"
