"""Mock Home Assistant modules and fixtures for testing ha_illuminance."""

from __future__ import annotations

import asyncio
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from types import ModuleType
from typing import Any
from unittest.mock import MagicMock

from astral.location import Location


def _setup_homeassistant_mock():
    """Install lightweight mock homeassistant packages into sys.modules."""
    if "homeassistant" in sys.modules:
        return

    ha = ModuleType("homeassistant")
    ha_core = ModuleType("homeassistant.core")
    ha_const = ModuleType("homeassistant.const")
    ha_config_entries = ModuleType("homeassistant.config_entries")
    ha_helpers = ModuleType("homeassistant.helpers")
    ha_helpers_cv = ModuleType("homeassistant.helpers.config_validation")
    ha_helpers_device = ModuleType("homeassistant.helpers.device_registry")
    ha_helpers_reload = ModuleType("homeassistant.helpers.reload")
    ha_helpers_service = ModuleType("homeassistant.helpers.service")
    ha_helpers_sun = ModuleType("homeassistant.helpers.sun")
    ha_helpers_typing = ModuleType("homeassistant.helpers.typing")
    ha_helpers_selector = ModuleType("homeassistant.helpers.selector")
    ha_helpers_entity_platform = ModuleType("homeassistant.helpers.entity_platform")
    ha_helpers_event = ModuleType("homeassistant.helpers.event")
    ha_components = ModuleType("homeassistant.components")
    ha_components_sensor = ModuleType("homeassistant.components.sensor")
    ha_components_weather = ModuleType("homeassistant.components.weather")
    ha_util = ModuleType("homeassistant.util")
    ha_util_dt = ModuleType("homeassistant.util.dt")
    ha_util_hass_dict = ModuleType("homeassistant.util.hass_dict")

    # core
    def callback(fn):
        return fn

    class Event:
        def __init__(self, data=None):
            self.data = data or {}

    class EventStateChangedData(dict):
        pass

    class State:
        def __init__(self, entity_id, state, attributes=None):
            self.entity_id = entity_id
            self.state = state
            self.attributes = attributes or {}

    class ServiceCall:
        def __init__(self, domain, service, data=None):
            self.domain = domain
            self.service = service
            self.data = data or {}

    class HomeAssistant:
        def __init__(self):
            self.data = {}
            self.loop = asyncio.get_event_loop()
            self.services = MagicMock()
            self.config_entries = MagicMock()
            self.config_entries.async_entries = MagicMock(return_value=[])
            self.config_entries.flow = MagicMock()
            self.config_entries.async_reload = MagicMock()
            self.bus = MagicMock()

        async def async_add_executor_job(self, target, *args, **kwargs):
            return target(*args, **kwargs)

        def async_create_task(self, coro):
            return asyncio.create_task(coro)

    ha_core.HomeAssistant = HomeAssistant
    ha_core.callback = callback
    ha_core.Event = Event
    ha_core.EventStateChangedData = EventStateChangedData
    ha_core.State = State
    ha_core.ServiceCall = ServiceCall

    # const
    class Platform(str, Enum):
        SENSOR = "sensor"

    class UnitOfIrradiance:
        WATTS_PER_SQUARE_METER = "W/m²"

    ha_const.Platform = Platform
    ha_const.UnitOfIrradiance = UnitOfIrradiance
    ha_const.CONF_NAME = "name"
    ha_const.CONF_UNIQUE_ID = "unique_id"
    ha_const.CONF_ENTITY_ID = "entity_id"
    ha_const.CONF_MODE = "mode"
    ha_const.CONF_SCAN_INTERVAL = "scan_interval"
    ha_const.EVENT_CORE_CONFIG_UPDATE = "core_config_updated"
    ha_const.SERVICE_RELOAD = "reload"
    ha_const.LIGHT_LUX = "lx"
    ha_const.STATE_UNAVAILABLE = "unavailable"
    ha_const.STATE_UNKNOWN = "unknown"
    ha_const.ATTR_ATTRIBUTION = "attribution"

    # config_entries
    class ConfigEntryState:
        recoverable = True

    class ConfigEntry:
        def __init__(
            self,
            entry_id="test_entry",
            data=None,
            options=None,
            title="Illuminance",
            unique_id="unique_123",
            source="user",
        ):
            self.entry_id = entry_id
            self.data = data or {}
            self.options = options or {}
            self.title = title
            self.unique_id = unique_id
            self.source = source
            self.state = ConfigEntryState()
            self._unloaders = []

        def async_on_unload(self, unloader):
            self._unloaders.append(unloader)

        def add_update_listener(self, listener):
            return lambda: None

    class ConfigEntryBaseFlow:
        pass

    class ConfigFlow:
        def __init_subclass__(cls, domain=None, **kwargs):
            super().__init_subclass__(**kwargs)

        def add_suggested_values_to_schema(self, schema, suggested_values):
            return schema

        async def async_set_unique_id(self, uid):
            return None

        def async_show_form(self, step_id, data_schema, last_step=True, errors=None):
            return {
                "type": "form",
                "step_id": step_id,
                "data_schema": data_schema,
                "errors": errors or {},
            }

        def async_create_entry(self, title, data, options=None):
            return {
                "type": "create_entry",
                "title": title,
                "data": data,
                "options": options or {},
            }

        def async_abort(self, reason):
            return {"type": "abort", "reason": reason}

    class OptionsFlowWithConfigEntry:
        def __init__(self, config_entry):
            self.config_entry = config_entry
            self._options = dict(config_entry.options) if config_entry else {}

        @property
        def options(self):
            return self._options

        def add_suggested_values_to_schema(self, schema, suggested_values):
            return schema

        def async_show_form(self, step_id, data_schema, last_step=True, errors=None):
            return {"type": "form", "step_id": step_id, "data_schema": data_schema}

        def async_create_entry(self, title="", data=None):
            return {"type": "create_entry", "data": data}

    ConfigFlowResult = dict[str, Any]

    ha_config_entries.SOURCE_IMPORT = "import"
    ha_config_entries.ConfigEntry = ConfigEntry
    ha_config_entries.ConfigEntryBaseFlow = ConfigEntryBaseFlow
    ha_config_entries.ConfigFlow = ConfigFlow
    ha_config_entries.ConfigFlowResult = ConfigFlowResult
    ha_config_entries.OptionsFlowWithConfigEntry = OptionsFlowWithConfigEntry

    # config_validation
    def string(val):
        return str(val)

    def ensure_list(val):
        if isinstance(val, list):
            return val
        return [val]

    def time_period(val):
        return val

    def entity_id(val):
        return str(val)

    def boolean(val):
        return bool(val)

    ha_helpers_cv.string = string
    ha_helpers_cv.ensure_list = ensure_list
    ha_helpers_cv.time_period = time_period
    ha_helpers_cv.entity_id = entity_id
    ha_helpers_cv.boolean = boolean

    # device_registry
    class DeviceRegistry:
        def __init__(self):
            self.devices = {}

        def async_get_device(self, identifiers):
            return self.devices.get(next(iter(identifiers), None))

        def async_remove_device(self, device_id):
            to_del = [
                k
                for k, v in self.devices.items()
                if getattr(v, "id", None) == device_id or k == device_id
            ]
            for k in to_del:
                del self.devices[k]

    _dev_reg = DeviceRegistry()

    def async_get_device_reg(hass):
        return _dev_reg

    ha_helpers_device.async_get = async_get_device_reg

    # reload
    async def async_integration_yaml_config(hass, domain):
        return {domain: []}

    ha_helpers_reload.async_integration_yaml_config = async_integration_yaml_config

    # service
    def async_register_admin_service(hass, domain, service, handler):
        pass

    ha_helpers_service.async_register_admin_service = async_register_admin_service

    # sun
    def get_astral_location(hass):
        from astral.location import LocationInfo

        info = LocationInfo("London", "England", "Europe/London", 51.5, -0.1)
        loc = Location(info)
        return loc, 25

    ha_helpers_sun.get_astral_location = get_astral_location

    # typing
    ha_helpers_typing.ConfigType = dict

    # selector
    class NumberSelectorMode:
        BOX = "box"

    def SelectSelector(config):
        return config

    def SelectSelectorConfig(options, translation_key=None):
        return {"options": options, "translation_key": translation_key}

    def NumberSelector(config):
        return config

    def NumberSelectorConfig(min=None, max=None, step=None, mode=None):
        return {"min": min, "max": max, "step": step, "mode": mode}

    def EntitySelector(config):
        return config

    def EntitySelectorConfig(domain=None):
        return {"domain": domain}

    def TextSelector():
        return {}

    ha_helpers_selector.NumberSelectorMode = NumberSelectorMode
    ha_helpers_selector.SelectSelector = SelectSelector
    ha_helpers_selector.SelectSelectorConfig = SelectSelectorConfig
    ha_helpers_selector.NumberSelector = NumberSelector
    ha_helpers_selector.NumberSelectorConfig = NumberSelectorConfig
    ha_helpers_selector.EntitySelector = EntitySelector
    ha_helpers_selector.EntitySelectorConfig = EntitySelectorConfig
    ha_helpers_selector.TextSelector = TextSelector

    # entity_platform
    AddEntitiesCallback = Any
    EntityPlatform = Any
    ha_helpers_entity_platform.AddEntitiesCallback = AddEntitiesCallback
    ha_helpers_entity_platform.EntityPlatform = EntityPlatform

    # event
    def async_track_state_change_event(hass, entity_ids, action):
        return lambda: None

    ha_helpers_event.async_track_state_change_event = async_track_state_change_event

    # components.sensor
    class SensorDeviceClass(str, Enum):
        ILLUMINANCE = "illuminance"
        IRRADIANCE = "irradiance"

    class SensorStateClass(str, Enum):
        MEASUREMENT = "measurement"

    class SensorEntity:
        def __init__(self):
            self.hass = None
            self.entity_description = None
            self._attr_native_value = None

        @property
        def native_value(self):
            return self._attr_native_value

        def async_write_ha_state(self):
            pass

    @dataclass(kw_only=True)
    class SensorEntityDescription:
        key: str
        device_class: Any = None
        name: str | None = None
        native_unit_of_measurement: str | None = None
        state_class: Any = None
        suggested_display_precision: int | None = None

    ha_components_sensor.SensorDeviceClass = SensorDeviceClass
    ha_components_sensor.SensorStateClass = SensorStateClass
    ha_components_sensor.SensorEntity = SensorEntity
    ha_components_sensor.SensorEntityDescription = SensorEntityDescription

    # components.weather
    weather_conditions = [
        "clear-night",
        "cloudy",
        "exceptional",
        "fog",
        "hail",
        "lightning",
        "lightning-rainy",
        "partlycloudy",
        "pouring",
        "rainy",
        "snowy",
        "snowy-rainy",
        "sunny",
        "windy",
        "windy-variant",
    ]
    for cond in weather_conditions:
        attr_name = "ATTR_CONDITION_" + cond.upper().replace("-", "_")
        setattr(ha_components_weather, attr_name, cond)

    # util.dt
    def utcnow():
        return datetime.now(timezone.utc)

    def as_local(dt):
        return dt.astimezone()

    ha_util_dt.utcnow = utcnow
    ha_util_dt.as_local = as_local

    # util.hass_dict
    class HassKey:
        def __init__(self, key):
            self.key = key

    ha_util_hass_dict.HassKey = HassKey

    # register modules
    sys.modules["homeassistant"] = ha
    sys.modules["homeassistant.core"] = ha_core
    sys.modules["homeassistant.const"] = ha_const
    sys.modules["homeassistant.config_entries"] = ha_config_entries
    sys.modules["homeassistant.helpers"] = ha_helpers
    sys.modules["homeassistant.helpers.config_validation"] = ha_helpers_cv
    sys.modules["homeassistant.helpers.device_registry"] = ha_helpers_device
    sys.modules["homeassistant.helpers.reload"] = ha_helpers_reload
    sys.modules["homeassistant.helpers.service"] = ha_helpers_service
    sys.modules["homeassistant.helpers.sun"] = ha_helpers_sun
    sys.modules["homeassistant.helpers.typing"] = ha_helpers_typing
    sys.modules["homeassistant.helpers.selector"] = ha_helpers_selector
    sys.modules["homeassistant.helpers.entity_platform"] = ha_helpers_entity_platform
    sys.modules["homeassistant.helpers.event"] = ha_helpers_event
    sys.modules["homeassistant.components"] = ha_components
    sys.modules["homeassistant.components.sensor"] = ha_components_sensor
    sys.modules["homeassistant.components.weather"] = ha_components_weather
    sys.modules["homeassistant.util"] = ha_util
    sys.modules["homeassistant.util.dt"] = ha_util_dt
    sys.modules["homeassistant.util.hass_dict"] = ha_util_hass_dict


_setup_homeassistant_mock()
