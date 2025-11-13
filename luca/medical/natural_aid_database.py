"""
🌿 NATÜRLICHE & PFLANZLICHE NOTFALLHILFEN
Natural and herbal emergency aid database with regional localization

Quellen:
- Helsana Erste-Hilfe-Ratgeber
- Malteser Hilfsdienst
- Traditional herbal knowledge

⚠️ WICHTIG: Diese Informationen ersetzen KEINE ärztliche Behandlung!
Bei lebensbedrohlichen Situationen IMMER 112 wählen!

Author: Großvater
Standard: 369/370
"""

NATURAL_EMERGENCY_AIDS = {
    "Wunden & Schürfwunden": {
        "pflanzlich": [
            {
                "name": "Arnika",
                "form": "Gel/Salbe/Tinktur",
                "effect": "Abschwellend, entzündungshemmend",
                "warning": "Nicht auf offene Wunden",
            },
            {
                "name": "Aloe Vera",
                "form": "Gel",
                "effect": "Wundheilung, kühlend",
                "warning": "Nur reine Aloe verwenden",
            },
            {
                "name": "Breitwegerich",
                "form": "Gepresste Blätter",
                "effect": "Blutung stillen, entzündungshemmend",
                "application": "Blätter zerquetschen, auf Wunde pressen",
            },
        ],
        "regional": {
            "Wald": "Moose (desinfizierend), Rinde innenseite",
            "Garten": "Mutterkraut, Kamille (als Kompresse)",
            "Wiese": "Spitzwegerich, Schafgarbe",
        },
        "immediate": ["Druckverband", "Desinfektion", "Stabile Lagerung"],
    },
    "Insektenstiche & Bisse": {
        "pflanzlich": [
            {
                "name": "Lavendelöl",
                "effect": "Juckreiz lindern",
                "application": "Verdünnt aufstupfen",
            },
            {
                "name": "Kiefernnadeln",
                "effect": "Entzündungshemmend",
                "application": "Aufguss als Kompresse",
            },
            {
                "name": "Zwiebel",
                "effect": "Abschwellend",
                "application": "Scheibe auf Stich legen",
            },
        ],
        "regional": {
            "Küche": "Zwiebel, Knoblauch (desinfizierend)",
            "Wiese": "Gänseblümchen, Klee (kühlend)",
        },
        "warning": "⚠️ Bei Allergiker sofort 112 wählen!",
    },
    "Prellungen & Zerrungen": {
        "pflanzlich": [
            {
                "name": "Arnika",
                "form": "Kompressen",
                "effect": "Standard bei Prellungen",
                "timing": "Sofort nach Verletzung",
            },
            {
                "name": "Beinwell",
                "form": "Blätter",
                "effect": "Knochenheilung",
                "application": "Blätter zu Brei verarbeiten",
            },
            {
                "name": "Rosmarin",
                "effect": "Durchblutung fördern",
                "application": "Ätherisches Öl massieren",
            },
        ],
        "regional": {
            "Wald": "Tannenzapfen-Aufguss (abschwellend)",
            "Garten": "Rosemary, Thymian",
        },
    },
    "Verbrennungen": {
        "pflanzlich": [
            {
                "name": "Aloe Vera",
                "effect": "1. Grades: sofort kühlen und Aloe",
                "warning": "2./3. Grades: SOFORT ARZT!",
            },
            {
                "name": "Kamille",
                "effect": "Kühlende Kompresse",
                "application": "Aufguss abkühlen lassen",
            },
        ],
        "immediate": [
            "15 Min kühlen unter fließendem Wasser",
            "Nicht aufbrechen",
            "Keine Hausmittel bei schweren Verbrennungen!",
        ],
    },
    "Unterkühlung": {
        "pflanzlich": [
            {
                "name": "Ingwer",
                "form": "Tee",
                "effect": "Innerliche Wärmegewinnung",
                "application": "Sofort warme Getränke",
            },
            {
                "name": "Rosmarin",
                "effect": "Durchblutung anregen",
            },
        ],
        "regional": {
            "Unterwegs": "Körperwärme anderer Personen",
            "Hütte": "Warmes Feuer, Decken",
        },
        "immediate": [
            "Trockene Kleidung",
            "Wärmflasche (nicht direkt auf Haut)",
            "144 bei Bewusstlosigkeit",
        ],
    },
}

# LOKALE APOTHEKEN & NOTDIENSTE
# Regional angepasst für Deutschland/Österreich/Schweiz
LOCAL_RESOURCES = {
    "Hamburg": {
        "notdienst_apotheken": "https://www.apotheken.de/notdienst/hamburg/",
        "aerzte_notdienst": "116117",
        "giftnotruf": "040 19240",
        "emergency": "112",
        "regionale_pflanzen": [
            "Wegerich",
            "Gänseblümchen",
            "Kiefer",
            "Birke",
            "Hagebutte",
        ],
    },
    "Berlin": {
        "notdienst_apotheken": "https://www.akd.notdienst-apotheke.de",
        "aerzte_notdienst": "116117",
        "giftnotruf": "030 19240",
        "emergency": "112",
        "regionale_pflanzen": [
            "Spitzwegerich",
            "Gänseblümchen",
            "Tannenzapfen",
            "Hagebutte",
        ],
    },
    "München": {
        "notdienst_apotheken": "https://www.aponet.de",
        "aerzte_notdienst": "116117",
        "giftnotruf": "089 19240",
        "emergency": "112",
        "regionale_pflanzen": [
            "Arnika (Alpen)",
            "Enzian",
            "Beinwell",
            "Wacholder",
        ],
    },
    "Wien": {
        "notdienst_apotheken": "https://www.apotheker.or.at",
        "aerzte_notdienst": "141",
        "giftnotruf": "01 406 43 43",
        "emergency": "144",
        "regionale_pflanzen": ["Arnika", "Enzian", "Kamille", "Salbei"],
    },
    "Zürich": {
        "notdienst_apotheken": "https://www.apotheke.ch",
        "aerzte_notdienst": "0800 33 66 55",
        "giftnotruf": "145",
        "emergency": "144",
        "regionale_pflanzen": ["Arnika", "Enzian", "Edelweiss", "Wacholder"],
    },
}

# Fallback für unbekannte Regionen
DEFAULT_RESOURCES = {
    "emergency": "112",
    "giftnotruf": "Lokale Giftnotrufzentrale kontaktieren",
    "aerzte_notdienst": "116117 (Deutschland)",
    "regionale_pflanzen": ["Arnika", "Wegerich", "Aloe Vera (falls verfügbar)"],
}
