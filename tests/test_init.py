"""Test initialization and migration in ha_illuminance."""

from unittest.mock import AsyncMock, MagicMock

import homeassistant.helpers.device_registry as dr
import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.ha_illuminance import (
    async_setup,
    async_setup_entry,
    async_unload_entry,
)
from custom_components.ha_illuminance.const import DOMAIN, OLD_DOMAIN


@pytest.mark.asyncio
async def test_async_setup_clean_and_legacy_devices():
    """Test async_setup removes legacy devices for both DOMAIN and OLD_DOMAIN."""
    hass = HomeAssistant()

    # Pre-populate device registry with legacy devices
    dev_reg = dr.async_get(hass)
    mock_dev_old = MagicMock(id="dev_old")
    mock_dev_new = MagicMock(id="dev_new")
    dev_reg.devices[(OLD_DOMAIN, OLD_DOMAIN)] = mock_dev_old
    dev_reg.devices[(DOMAIN, DOMAIN)] = mock_dev_new

    result = await async_setup(hass, {})
    assert result is True

    # Legacy devices should be removed
    assert (OLD_DOMAIN, OLD_DOMAIN) not in dev_reg.devices
    assert (DOMAIN, DOMAIN) not in dev_reg.devices


@pytest.mark.asyncio
async def test_async_setup_legacy_migration():
    """Test async_setup migrates legacy entries from illuminance to ha_illuminance."""
    hass = HomeAssistant()
    created_tasks = []
    hass.async_create_task = lambda coro: created_tasks.append(coro)

    old_entry = ConfigEntry(
        entry_id="old_entry_1",
        title="Old Sun Sensor",
        unique_id="unique_sun_1",
        options={"mode": "normal", "scan_interval": 5.0},
        data={},
    )

    def mock_async_entries(domain):
        if domain == OLD_DOMAIN:
            return [old_entry]
        return []

    hass.config_entries.async_entries = mock_async_entries

    result = await async_setup(hass, {})
    assert result is True
    # Tasks were created for migration and removal
    assert len(created_tasks) >= 2


@pytest.mark.asyncio
async def test_setup_and_unload_entry():
    """Test setup and unload of a config entry."""
    hass = HomeAssistant()
    hass.config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
    hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)

    entry = ConfigEntry()

    assert await async_setup_entry(hass, entry) is True
    assert hass.config_entries.async_forward_entry_setups.called

    assert await async_unload_entry(hass, entry) is True
    assert hass.config_entries.async_unload_platforms.called
