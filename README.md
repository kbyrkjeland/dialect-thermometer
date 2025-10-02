# Dialekttermometer

Custom Home Assistant sensor platform som oversetter en temperatursensor til et lokalt dialektuttrykk.

## Installasjon

### HACS

1. Åpne **HACS → Integrations** og trykk på menyknappen (⋮).
2. Velg **Custom repositories** og legg til dette repoet som *Integration*.
3. Installer «Dialekttermometer» fra HACS-listen og vent til installasjonen fullføres.
4. Start Home Assistant på nytt.

### Manuelt

1. Kopier mappen `custom_components/dialect_thermometer` til `config/custom_components/` i Home Assistant-installasjonen din.
2. Start Home Assistant på nytt.

## Konfigurasjon

1. Åpne Home Assistant og naviger til **Innstillinger → Enheter og tjenester**.
2. Velg **Legg til integrasjon**, søk etter «Dialekttermometer» og følg veiviseren.
3. Angi navn, velg temperatursensor og ønsket dialekt. Gjenta for flere sensorer.

## Dialekter

Tilgjengelige dialekter og uttrykk ligger i mappen `custom_components/dialect_thermometer/dialects/`, en fil per dialekt.

## Bidra med dialekter

1. Lag en ny fil i `custom_components/dialect_thermometer/dialects/` med dialektnavn som filnavn, for eksempel `trondheim.py`.
2. Definer en `DIALECT`-dictionary med temperaturterskler som nøkler (fra høyest til lavest) og uttrykk som verdier, inkludert en `-999` fallback.
3. Legg dialekten til i `custom_components/dialect_thermometer/dialects/__init__.py` slik at den blir tilgjengelig i integrasjonen.
4. Oppdater `translations/en.json` og `translations/nb.json` dersom dialekten skal vises med et spesifikt navn i veiviseren.
5. Kjør `python3 -m compileall custom_components` for å sjekke at alt fortsatt kompilerer før du sender inn et pull request.

## Lisens

MIT
