"""Dialect Thermometer integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Dialect Thermometer integration via YAML."""
    hass.data.setdefault(DOMAIN, {})
    return True
