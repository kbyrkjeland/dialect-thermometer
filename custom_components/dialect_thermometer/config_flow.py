"""Config flow for the Dialect Thermometer integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv, selector

from .const import CONF_DIALECT, CONF_TEMPERATURE_SENSOR_ID, DOMAIN
from .dialects import DIALECTS


class DialectThermometerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dialect Thermometer."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, str] | None = None):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        dialect_choices = sorted(DIALECTS)
        if not dialect_choices:
            return self.async_abort(reason="no_dialects_defined")

        default_dialect = dialect_choices[0]

        if user_input is not None:
            name = user_input[CONF_NAME]
            source_entity = user_input[CONF_TEMPERATURE_SENSOR_ID]
            dialect = user_input[CONF_DIALECT]

            unique_id = f"{source_entity}|{dialect}".lower()
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=name,
                data={
                    CONF_NAME: name,
                    CONF_TEMPERATURE_SENSOR_ID: source_entity,
                    CONF_DIALECT: dialect,
                },
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_TEMPERATURE_SENSOR_ID): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=["sensor"])
                ),
                vol.Required(CONF_DIALECT, default=default_dialect): vol.In(dialect_choices),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(data_schema, user_input),
            errors=errors,
        )
