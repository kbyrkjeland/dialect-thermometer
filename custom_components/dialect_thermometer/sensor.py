"""Sensor platform for the Dialect Thermometer integration."""

from __future__ import annotations

import logging
from typing import Any, Callable, Iterable

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_DIALECT,
    CONF_TEMPERATURE_SENSOR_ID,
    UNKNOWN_STATE,
)
from .dialects import DIALECTS

_LOGGER = logging.getLogger(__name__)


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
        _LOGGER.debug(
            "Invalid temperature value '%s' for dialect '%s'",
            raw_value,
            dialect_key,
        )
        return UNKNOWN_STATE

    for threshold in _iter_sorted_thresholds(mapping):
        if temperature >= threshold:
            return mapping[threshold]

    return mapping.get(-999, UNKNOWN_STATE)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a Dialect Thermometer sensor from a config entry."""
    async_add_entities([DialectThermometerSensor(entry)])


class DialectThermometerSensor(SensorEntity):
    """Representation of a Dialect Thermometer sensor."""

    _attr_should_poll = False
    _attr_native_unit_of_measurement = None

    def __init__(self, entry: ConfigEntry) -> None:
        self._config_entry_id = entry.entry_id
        self._attr_name = entry.title
        self._source_entity_id = entry.data[CONF_TEMPERATURE_SENSOR_ID]
        self._dialect = entry.data[CONF_DIALECT]
        self._attr_unique_id = entry.unique_id or entry.entry_id
        self._attr_native_value = UNKNOWN_STATE
        self._attr_icon = "mdi:chat-outline"
        self._unsubscribe: Callable[[], None] | None = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self._subscribe_to_source()

        initial_state = self.hass.states.get(self._source_entity_id)
        self._process_state(initial_state)

    async def async_will_remove_from_hass(self) -> None:
        await super().async_will_remove_from_hass()
        if self._unsubscribe:
            self._unsubscribe()
            self._unsubscribe = None

    async def async_update_config_entry(self, config_entry: ConfigEntry) -> None:
        """Handle updates to the config entry (e.g. rename)."""
        if config_entry.entry_id != self._config_entry_id:
            return

        self._attr_name = config_entry.title
        new_source = config_entry.data[CONF_TEMPERATURE_SENSOR_ID]
        new_dialect = config_entry.data[CONF_DIALECT]

        reload_state = False

        if new_source != self._source_entity_id:
            self._source_entity_id = new_source
            self._subscribe_to_source()
            reload_state = True

        if new_dialect != self._dialect:
            self._dialect = new_dialect
            reload_state = True

        if reload_state:
            state = self.hass.states.get(self._source_entity_id)
            self._process_state(state)
        else:
            self.async_write_ha_state()

    def _subscribe_to_source(self) -> None:
        if self._unsubscribe:
            self._unsubscribe()

        def _state_listener(event) -> None:
            new_state: State | None = event.data.get("new_state")
            self._process_state(new_state)

        self._unsubscribe = async_track_state_change_event(
            self.hass,
            [self._source_entity_id],
            _state_listener,
        )

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
