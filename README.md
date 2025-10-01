# Dialekttermometer

Custom Home Assistant sensor platform that translates a numeric temperature sensor into local dialect expressions.

## Installasjon

1. Kopier mappen `custom_components/dialect_thermometer` til `config/custom_components/` i Home Assistant-installasjonen din.
2. Start Home Assistant på nytt.

## Konfigurasjon

Legg følgende eksempel til i `configuration.yaml`:

```yaml
sensor:
  - platform: dialect_thermometer
    sensors:
      stue_varmt:
        temperature_sensor_id: sensor.stue_temperatur
        dialect: hardanger
        name: "Stue Hardanger Dialekt"
      ute_kaldt:
        temperature_sensor_id: sensor.utendors_temperatur
        dialect: sortland
        name: "Ute Sortland Dialekt"
```

## Dialekter

Tilgjengelige dialekter og uttrykk defineres i `custom_components/dialect_thermometer/dialects.py`.

## Lisens

MIT
