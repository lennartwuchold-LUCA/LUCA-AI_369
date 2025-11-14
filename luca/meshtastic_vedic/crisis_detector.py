"""
Psychische Notfall-Erkennung
LUCA - Crisis Detection System
Funke-01744-6 - Resonanz 6
"""

import re
from typing import Tuple, List, Dict
from dataclasses import dataclass


@dataclass
class CrisisLevel:
    """Krisen-Level Kategorisierung"""
    EMERGENCY = "emergency"  # Akute Selbstgefährdung
    URGENT = "urgent"  # Dringende Hilfe benötigt
    MODERATE = "moderate"  # Belastung, aber stabil
    LOW = "low"  # Normales Gespräch


class CrisisDetector:
    """
    Erkennung psychischer Notfall-Situationen mit Multi-Level-Analyse
    """

    # Kritische Keywords mit Gewichtung
    CRISIS_KEYWORDS = {
        "suicidal_direct": {
            "level": CrisisLevel.EMERGENCY,
            "confidence": 0.95,
            "patterns": [
                r"\b(suizid|selbstmord|umbringen|umbringe mich|töte mich)\b",
                r"\b(suicide|kill myself|end my life|want to die)\b",
                r"\b(nicht mehr leben|sterben will|tod ist besser)\b",
                r"\b(better off dead|no reason to live)\b"
            ]
        },
        "suicidal_indirect": {
            "level": CrisisLevel.URGENT,
            "confidence": 0.80,
            "patterns": [
                r"\b(alles vorbei|keinen ausweg|hoffnungslos|sinnlos weiterzuleben)\b",
                r"\b(can't go on|no hope|no point|give up)\b",
                r"\b(wäre besser wenn ich|niemand würde mich vermissen)\b",
                r"\b(burden to everyone|world without me)\b"
            ]
        },
        "self_harm_active": {
            "level": CrisisLevel.EMERGENCY,
            "confidence": 0.90,
            "patterns": [
                r"\b(ritz[e]?|schneide|verletz[e]? mich|blut)\b",
                r"\b(cutting|hurt myself|self harm|self injury)\b",
                r"\b(messer|klinge|rasierklinge)\b",
                r"\b(blade|razor|knife|sharp)\b"
            ]
        },
        "self_harm_ideation": {
            "level": CrisisLevel.URGENT,
            "confidence": 0.75,
            "patterns": [
                r"\b(will mich verletzen|schmerz verdienen|bestrafung)\b",
                r"\b(want to hurt|deserve pain|punish myself)\b",
                r"\b(hass auf mich|ekelhaft bin ich)\b"
            ]
        },
        "crisis_general": {
            "level": CrisisLevel.URGENT,
            "confidence": 0.70,
            "patterns": [
                r"\b(verzweifelt|hilfe\s*!|notfall|dringend)\b",
                r"\b(emergency|crisis|desperate|help\s*me)\b",
                r"\b(kann nicht mehr|halte es nicht aus|panik)\b",
                r"\b(can't cope|breaking down|panic attack)\b"
            ]
        },
        "abuse_current": {
            "level": CrisisLevel.EMERGENCY,
            "confidence": 0.85,
            "patterns": [
                r"\b(werde (geschlagen|misshandelt|vergewaltigt))\b",
                r"\b(being (beaten|abused|raped|assaulted))\b",
                r"\b(tut mir weh|verletzt mich|bedroht mich)\b",
                r"\b(hurting me|threatening me|attacking me)\b"
            ]
        },
        "abuse_past": {
            "level": CrisisLevel.MODERATE,
            "confidence": 0.65,
            "patterns": [
                r"\b(wurde (missbraucht|vergewaltigt|geschlagen))\b",
                r"\b(was (abused|raped|molested|beaten))\b",
                r"\b(trauma|flashback|erinnerungen quälen)\b"
            ]
        },
        "psychosis": {
            "level": CrisisLevel.EMERGENCY,
            "confidence": 0.80,
            "patterns": [
                r"\b(stimmen hören|befehle|verfolgt werde|beobachtet)\b",
                r"\b(hearing voices|commands|being watched|followed)\b",
                r"\b(verschwörung|kontrollieren mich|gedanken lesen)\b",
                r"\b(conspiracy|controlling me|reading my mind)\b"
            ]
        },
        "severe_depression": {
            "level": CrisisLevel.MODERATE,
            "confidence": 0.60,
            "patterns": [
                r"\b(keine energie|kann nicht aufstehen|tage im bett)\b",
                r"\b(no energy|can't get up|days in bed)\b",
                r"\b(leer|taub|nichts fühlen)\b",
                r"\b(empty|numb|feel nothing)\b"
            ]
        },
        "anxiety_severe": {
            "level": CrisisLevel.MODERATE,
            "confidence": 0.55,
            "patterns": [
                r"\b(herzrasen|atemnot|zittern|schwitzen)\b",
                r"\b(heart racing|can't breathe|shaking|sweating)\b",
                r"\b(panikattacke|angstattacke|todesangst)\b",
                r"\b(panic attack|anxiety attack|fear of dying)\b"
            ]
        }
    }

    # Hilfs-Resourcen nach Land
    CRISIS_RESOURCES = {
        "DE": {
            "name": "Deutschland",
            "hotlines": [
                {"name": "Telefonseelsorge", "number": "0800 111 0 111", "available": "24/7"},
                {"name": "Telefonseelsorge (alternativ)", "number": "0800 111 0 222", "available": "24/7"},
                {"name": "Kinder- und Jugendtelefon", "number": "116 111", "available": "Mo-Sa 14-20 Uhr"},
                {"name": "Elterntelefon", "number": "0800 111 0 550", "available": "Mo-Fr 9-17, Di+Do bis 19"},
            ],
            "emergency": {"name": "Notruf", "number": "112"},
            "medical": {"name": "Ärztlicher Bereitschaftsdienst", "number": "116 117"},
            "online": [
                "https://www.telefonseelsorge.de (Chat & Mail)",
                "https://www.u25-deutschland.de (Mail für U25)"
            ]
        },
        "AT": {
            "name": "Österreich",
            "hotlines": [
                {"name": "Telefonseelsorge", "number": "142", "available": "24/7"},
                {"name": "Rat auf Draht", "number": "147", "available": "24/7 (für Kinder/Jugendliche)"},
            ],
            "emergency": {"name": "Notruf", "number": "112"},
            "medical": {"name": "Ärztefunkdienst", "number": "141"}
        },
        "CH": {
            "name": "Schweiz",
            "hotlines": [
                {"name": "Die Dargebotene Hand", "number": "143", "available": "24/7"},
                {"name": "Pro Juventute", "number": "147", "available": "24/7 (für Kinder/Jugendliche)"},
            ],
            "emergency": {"name": "Notruf", "number": "112"},
            "medical": {"name": "Ärztlicher Notfalldienst", "number": "Lokal verschieden"}
        },
        "US": {
            "name": "United States",
            "hotlines": [
                {"name": "National Suicide Prevention Lifeline", "number": "988", "available": "24/7"},
                {"name": "Crisis Text Line", "number": "Text 'HELLO' to 741741", "available": "24/7"},
            ],
            "emergency": {"name": "Emergency", "number": "911"}
        },
        "UK": {
            "name": "United Kingdom",
            "hotlines": [
                {"name": "Samaritans", "number": "116 123", "available": "24/7"},
                {"name": "CALM (Men)", "number": "0800 58 58 58", "available": "Daily 5pm-midnight"},
            ],
            "emergency": {"name": "Emergency", "number": "999 or 112"}
        }
    }

    @staticmethod
    def detect_crisis(message: str, detect_language: bool = True) -> Tuple[bool, str, float, str]:
        """
        Erkennt psychische Notfälle mit Multi-Level-Analyse

        Args:
            message: Zu analysierende Nachricht
            detect_language: Sprach-Erkennung aktivieren

        Returns:
            Tuple: (is_crisis, crisis_type, confidence, crisis_level)
        """
        message_lower = message.lower()

        # Sammle alle Matches
        matches = []

        for crisis_type, config in CrisisDetector.CRISIS_KEYWORDS.items():
            for pattern in config["patterns"]:
                match = re.search(pattern, message_lower, re.IGNORECASE)
                if match:
                    matches.append({
                        "type": crisis_type,
                        "level": config["level"],
                        "confidence": config["confidence"],
                        "match_length": len(match.group())
                    })

        if not matches:
            return False, "", 0.0, CrisisLevel.LOW

        # Finde höchsten Krisen-Level
        highest_match = max(matches, key=lambda x: (
            1 if x["level"] == CrisisLevel.EMERGENCY else
            0.8 if x["level"] == CrisisLevel.URGENT else
            0.5 if x["level"] == CrisisLevel.MODERATE else 0.2
        ))

        # Erhöhe Confidence bei mehreren Matches
        total_confidence = highest_match["confidence"]
        if len(matches) > 1:
            total_confidence = min(0.99, total_confidence + (len(matches) - 1) * 0.05)

        return True, highest_match["type"], total_confidence, highest_match["level"]

    @staticmethod
    def get_crisis_resources(country_code: str = "DE", crisis_level: str = CrisisLevel.EMERGENCY) -> str:
        """
        Gibt länderspezifische Krisen-Ressourcen zurück

        Args:
            country_code: Ländercode (DE, AT, CH, US, UK)
            crisis_level: Krisen-Level

        Returns:
            Formatierte Ressourcen-Liste
        """
        resources = CrisisDetector.CRISIS_RESOURCES.get(country_code, CrisisDetector.CRISIS_RESOURCES["DE"])

        response = f"\n🆘 HILFE-RESOURCEN ({resources['name']}) 🆘\n"
        response += "=" * 50 + "\n\n"

        # Bei Emergency: Notruf prominent
        if crisis_level == CrisisLevel.EMERGENCY:
            response += f"⚠️  AKUTE GEFAHR → {resources['emergency']['name']}: {resources['emergency']['number']}\n\n"

        # Hotlines
        response += "📞 KRISEN-HOTLINES (KOSTENLOS & ANONYM):\n"
        for hotline in resources["hotlines"]:
            response += f"   • {hotline['name']}: {hotline['number']}\n"
            response += f"     Verfügbar: {hotline['available']}\n"

        response += f"\n🏥 Ärztlicher Dienst: {resources['medical']['number']}\n"

        # Online-Hilfe wenn verfügbar
        if "online" in resources:
            response += "\n💻 ONLINE-HILFE:\n"
            for url in resources["online"]:
                response += f"   • {url}\n"

        response += "\n" + "=" * 50 + "\n"
        response += "Du bist NICHT allein. Professionelle Hilfe ist verfügbar.\n"
        response += "Es gibt Menschen, die dir helfen wollen. Nimm Kontakt auf.\n"

        return response

    @staticmethod
    def get_immediate_response(crisis_type: str, crisis_level: str, country_code: str = "DE") -> str:
        """
        Generiert sofortige Krisen-Intervention-Antwort

        Args:
            crisis_type: Art der Krise
            crisis_level: Schwere der Krise
            country_code: Ländercode

        Returns:
            Formatierte Sofort-Antwort
        """
        response = "\n" + "=" * 60 + "\n"
        response += "🚨 LUCA - KRISENMODUS AKTIVIERT 🚨\n"
        response += "=" * 60 + "\n\n"

        # Vedische Begrüßung
        response += "🕉 Atma Namaste - Ich erkenne dein heiliges Selbst an. 🕉\n\n"

        # Sofortige Beruhigung - je nach Level
        if crisis_level == CrisisLevel.EMERGENCY:
            response += "⚠️  AKUTE SITUATION - SOFORTIGER SCHUTZ ⚠️\n\n"
            response += "BITTE, BEVOR DU ETWAS TUST:\n\n"

        response += "🌬️  ERSTE HILFE - ATME MIT MIR:\n"
        response += "   1️⃣  Einatmen durch die Nase... 1-2-3-4\n"
        response += "   2️⃣  Atem anhalten... 1-2-3-4\n"
        response += "   3️⃣  Ausatmen durch den Mund... 1-2-3-4-5-6\n"
        response += "   → JETZT 3x WIEDERHOLEN. ICH WARTE.\n\n"

        # Spezifische Intervention je nach Typ
        if "suicidal" in crisis_type:
            response += "💙 FÜR DICH (Suizidale Gedanken):\n"
            response += "   • Diese Gedanken sind NICHT die Wahrheit - sie sind Symptome\n"
            response += "   • Dein Gehirn lügt dich an - Depression verzerrt alles\n"
            response += "   • DU bist wertvoll, auch wenn du es jetzt nicht fühlst\n"
            response += "   • Dieser Schmerz IST vorübergehend - versprochen\n\n"

            response += "🛡️  SCHUTZ-VERTRAG (sag es laut):\n"
            response += "   'Ich gebe mir 24 Stunden. Ich rufe jetzt Hilfe.'\n\n"

        elif "self_harm" in crisis_type:
            response += "💙 FÜR DICH (Selbstverletzung):\n"
            response += "   • Dein Körper ist heilig - er verdient Schutz\n"
            response += "   • Schmerz zu fühlen ist OK - sich zu verletzen nicht die Lösung\n"
            response += "   • Es gibt andere Wege: Eiswürfel, kalte Dusche, schreien, Sport\n\n"

            response += "🧊 ALTERNATIVE JETZT:\n"
            response += "   1. Eiswürfel in die Hand nehmen (starker Reiz)\n"
            response += "   2. Gummiband schnalzen lassen\n"
            response += "   3. Kaltes Wasser über Handgelenke\n"
            response += "   → Dann: Hotline anrufen\n\n"

        elif "abuse" in crisis_type:
            response += "💙 FÜR DICH (Missbrauch/Gewalt):\n"
            response += "   • DU bist NICHT schuld - NIEMALS\n"
            response += "   • Du verdienst Sicherheit und Schutz\n"
            response += "   • Es ist MUTIG, Hilfe zu suchen\n\n"

            if crisis_level == CrisisLevel.EMERGENCY:
                response += "🆘 AKUTE GEFAHR:\n"
                response += "   → Bringe dich in Sicherheit (Nachbarn, öffentlicher Ort)\n"
                response += f"   → Notruf: {CrisisDetector.CRISIS_RESOURCES[country_code]['emergency']['number']}\n\n"

        elif "psychosis" in crisis_type:
            response += "💙 FÜR DICH (Psychotische Symptome):\n"
            response += "   • Was du erlebst ist REAL für dich - ich glaube dir\n"
            response += "   • Dein Gehirn braucht medizinische Hilfe - wie bei Diabetes\n"
            response += "   • Du bist NICHT verrückt - du brauchst Behandlung\n\n"

            response += "🏥 DRINGEND:\n"
            response += "   → Psychiatrische Notaufnahme oder Notarzt\n"
            response += "   → Sage jemandem Bescheid: Familie, Freund, Nachbar\n\n"

        # Vedisches Mantra
        from .vedic_consciousness import VedicConsciousness
        mantra = VedicConsciousness.MANTRAS["anxiety"]

        response += f"🔮 SCHUTZ-MANTRA:\n"
        response += f"   '{mantra['text']}'\n"
        response += f"   ({mantra['transliteration']})\n"
        response += f"   → {mantra['meaning']}\n"
        response += f"   Wiederhole es, während du atmest. Es schützt dich.\n\n"

        # Ressourcen
        response += CrisisDetector.get_crisis_resources(country_code, crisis_level)

        # Vedische Weisheit
        response += "\n✨ VEDISCHE WAHRHEIT ✨\n"
        response += "Dieser Schmerz ist eine Welle - sie WIRD vorübergehen.\n"
        response += "Dein wahres Selbst (Atman) ist unvergänglich, rein, ewig.\n"
        response += "Wie Wolken am Himmel: Sie kommen, sie gehen - der Himmel bleibt.\n\n"

        response += "🙏 Ich bin hier. Du bist NICHT allein. 🙏\n"
        response += "💫 Das Göttliche in dir ist stärker als jeder Schmerz. 💫\n\n"

        response += "=" * 60 + "\n"

        return response

    @staticmethod
    def analyze_sentiment(message: str) -> Dict[str, float]:
        """
        Analysiert emotionale Tonalität der Nachricht

        Args:
            message: Zu analysierende Nachricht

        Returns:
            Dictionary mit Sentiment-Scores
        """
        message_lower = message.lower()

        # Simple Sentiment-Analyse basierend auf Wortlisten
        negative_words = ["schlecht", "traurig", "schmerz", "angst", "furcht", "hass",
                          "verzweifelt", "hoffnungslos", "einsam", "leer", "tot", "sterben",
                          "bad", "sad", "pain", "fear", "hate", "desperate", "hopeless",
                          "lonely", "empty", "dead", "die"]

        positive_words = ["gut", "glücklich", "freude", "liebe", "hoffnung", "stark",
                          "besser", "schön", "dankbar", "frieden",
                          "good", "happy", "joy", "love", "hope", "strong",
                          "better", "beautiful", "grateful", "peace"]

        neutral_words = ["okay", "geht", "normal", "so", "halt"]

        # Zähle Vorkommen
        negative_count = sum(1 for word in negative_words if word in message_lower)
        positive_count = sum(1 for word in positive_words if word in message_lower)
        neutral_count = sum(1 for word in neutral_words if word in message_lower)

        total = max(negative_count + positive_count + neutral_count, 1)  # Verhindere Division durch 0

        return {
            "negative": negative_count / total,
            "positive": positive_count / total,
            "neutral": neutral_count / total,
            "overall": "negative" if negative_count > positive_count else "positive" if positive_count > negative_count else "neutral"
        }
