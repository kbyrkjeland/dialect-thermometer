"""Sensor platform for the Dialect Thermometer integration."""

from __future__ import annotations

import logging
from typing import Any, Iterable, Callable

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, UNKNOWN_STATE
from .dialects import DIALECTS

_LOGGER = logging.getLogger(__name__)

CONF_SENSORS = "sensors"
CONF_TEMPERATURE_SENSOR_ID = "temperature_sensor_id"
CONF_DIALECT = "dialect"

SENSOR_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_TEMPERATURE_SENSOR_ID): cv.entity_id,
        vol.Required(CONF_DIALECT): cv.string,
        vol.Optional(CONF_NAME): cv.string,
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SENSORS): vol.Schema({cv.slug: SENSOR_SCHEMA})
    }
)


def _iter_sorted_thresholds(thresholds: Iterable[int]) -> list[int]:
    """Return threshold values sorted descending."""
    return sorted(thresholds, reverse=True)


def get_dialect_word(raw_value: Any, dialect: str) -> str:
    """Translate a temperature into its dialect word."""
    if dialect is None:
        _LOGGER.debug("Dialect not provided; returning unknown state")
        return UNKNOWN_STATE

    dialect_key = dialect.lower()
    mapping = DIALECTS.get(dialect_key)
    if not mapping:
        _LOGGER.warning("Dialect '%s' not found in DIALECTS", dialect_key)
        return UNKNOWN_STATE

    if raw_value in (None, "", "unknown", "unavailable"):
        return UNKNOWN_STATE

    try:
        temperature = float(raw_value)
    except (TypeError, ValueError):
        _LOGGER.debug("Invalid temperature value '%s' for dialect '%s'", raw_value, dialect_key)
        return UNKNOWN_STATE

    for threshold in _iter_sorted_thresholds(mapping):
        if temperature >= threshold:
            return mapping[threshold]

    return mapping.get(-999, UNKNOWN_STATE)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up Dialect Thermometer sensors from YAML."""
    sensors_config = config.get(CONF_SENSORS, {})
    entities: list[DialectThermometerSensor] = []

    for sensor_id, sensor_conf in sensors_config.items():
        temperature_entity = sensor_conf[CONF_TEMPERATURE_SENSOR_ID]
        dialect = sensor_conf[CONF_DIALECT]
        name = sensor_conf.get(CONF_NAME) or sensor_id.replace("_", " ").title()

        entities.append(
            DialectThermometerSensor(
                name=name,
                source_entity_id=temperature_entity,
                dialect=dialect,
                unique_id=f"{DOMAIN}-{sensor_id}"
            )
        )

    if not entities:
        _LOGGER.warning("No Dialect Thermometer sensors defined in configuration")
        return

    async_add_entities(entities)


class DialectThermometerSensor(SensorEntity):
    """Representation of a Dialect Thermometer sensor."""

    _attr_has_entity_name = False
    _attr_should_poll = False
    _attr_native_unit_of_measurement = None

    def __init__(self, name: str, source_entity_id: str, dialect: str, unique_id: str | None = None) -> None:
        self._attr_name = name
        self._source_entity_id = source_entity_id
        self._dialect = dialect
        self._attr_unique_id = unique_id
        self._attr_native_value = UNKNOWN_STATE
        self._unsubscribe: Callable[[], None] | None = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()

        def _state_listener(event) -> None:
            new_state: State | None = event.data.get("new_state")
            self._process_state(new_state)

        self._unsubscribe = async_track_state_change_event(
            self.hass, [self._source_entity_id], _state_listener
        )

        initial_state = self.hass.states.get(self._source_entity_id)
        self._process_state(initial_state)

    async def async_will_remove_from_hass(self) -> None:
        await super().async_will_remove_from_hass()
        if self._unsubscribe:
            self._unsubscribe()
            self._unsubscribe = None

    def _process_state(self, state: State | None) -> None:
        if state is None:
            self._attr_native_value = UNKNOWN_STATE
        else:
            self._attr_native_value = get_dialect_word(state.state, self._dialect)
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        return {
            "source_entity_id": self._source_entity_id,
            "dialect": self._dialect,
        }
