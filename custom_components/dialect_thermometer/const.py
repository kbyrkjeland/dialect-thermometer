"""Constants for the Dialect Thermometer integration."""

from __future__ import annotations

DOMAIN = "dialect_thermometer"
UNKNOWN_STATE = "Ukjent temperatur"

DIALECTS = {
    "sortland": {
        50: "Den morran våkner du ei",
        40: "Globitt",
        30: "Akonna",
        25: "Vi står han vel a'",
        20: "Det e ikkje bra førr haine med sånn sinkkyve...",
        15: "Kosallssommar",
        10: "God haustværka",
        5: "Lænt",
        0: "Haustri",
        -5: "Lævva",
        -10: "Vaskakailt",
        -15: "Snøkjær",
        -20: "Luggsjære",
        -25: "Beinkaildt",
        -30: "Svinkaildt",
        -35: "Gnallerfrost",
        -40: "Spikkjefrost",
        -999: "Tukjkaildt",
    },
    "hardanger": {
        40: "Sju varmt ha då",
        30: "Jeghalt været",
        25: "Eg liggja vakk",
        20: "I sniggo vetto",
        15: "Gødt utestøveir",
        10: "No kosmar det tå",
        5: "Astesjn inn",
        0: "Genokaildt",
        -5: "Førr fy so kaildt",
        -10: "Snøkje",
        -15: "Då vetto ordno kaildet",
        -20: "Eg tykkjje da so kaildt",
        -25: "Bein-kaildt",
        -30: "Opti! Gørrane land!",
        -40: "Nå kos då",
        -999: "De kan ikkje vø her",
    },
}
