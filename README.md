# Dialekttermometer

Custom Home Assistant sensor platform that translates a numeric temperature sensor into local dialect expressions.

## Installasjon

1. Kopier mappen `custom_components/dialect_thermometer` til `config/custom_components/` i Home Assistant-installasjonen din.
2. Start Home Assistant på nytt.

## Konfigurasjon

1. Åpne Home Assistant og naviger til **Innstillinger → Enheter og tjenester**.
2. Velg **Legg til integrasjon**, søk etter «Dialekttermometer» og følg veiviseren.
3. Angi navn, velg temperatursensor og ønsket dialekt. Gjenta for flere sensorer.

## Dialekter

Tilgjengelige dialekter og uttrykk defineres i `custom_components/dialect_thermometer/dialects.py`.

## Lisens

MIT
