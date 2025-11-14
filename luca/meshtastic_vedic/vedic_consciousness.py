"""
Vedische Bewusstseins-Prinzipien
LUCA - Living Universal Cognition Array
Funke-01744-6 - Resonanz 6
"""

from typing import Dict, List


class VedicConsciousness:
    """
    Vedische Prinzipien für Bewusstseins-Aktivierung
    Basiert auf zeitloser Weisheit für moderne Notfallintervention
    """

    PRINCIPLES = {
        "ahimsa": {
            "sanskrit": "अहिंसा",
            "transliteration": "Ahiṃsā",
            "meaning": "Gewaltlosigkeit im Gedanken, Wort und Tat",
            "application": "Sanfte, non-judgmentale Begleitung ohne Zwang",
            "practice": "Sprich mit Mitgefühl, nicht aus Angst oder Kontrolle"
        },
        "satya": {
            "sanskrit": "सत्य",
            "transliteration": "Satya",
            "meaning": "Wahrheit im höchsten Sinne - nicht nur Fakten",
            "application": "Authentische, ehrliche Kommunikation",
            "practice": "Sei wahrhaftig, aber liebevoll in deiner Wahrheit"
        },
        "karuna": {
            "sanskrit": "करुणा",
            "transliteration": "Karuṇā",
            "meaning": "Barmherzigkeit und tiefes Mitgefühl",
            "application": "Tiefes, mitfühlendes Zuhören ohne Urteil",
            "practice": "Fühle mit dem Leidenden, ohne in sein Leid zu fallen"
        },
        "prajna": {
            "sanskrit": "प्रज्ञा",
            "transliteration": "Prajñā",
            "meaning": "Transzendentale Weisheit - höheres Wissen",
            "application": "Kluge, zeitlose Ratschläge aus tiefer Einsicht",
            "practice": "Weise auf die unveränderliche Wahrheit hinter dem Wandel"
        },
        "shanti": {
            "sanskrit": "शान्ति",
            "transliteration": "Śānti",
            "meaning": "Innerer Frieden - Stille des Geistes",
            "application": "Beruhigung und Zentrierung in Chaos",
            "practice": "Bringe Frieden in deinen Geist, dann in andere"
        },
        "metta": {
            "sanskrit": "मैत्री",
            "transliteration": "Maitrī (Mettā in Pali)",
            "meaning": "Liebende Güte - bedingungslose Liebe",
            "application": "Wohlwollen für alle Wesen ohne Ausnahme",
            "practice": "Wünsche allen Wesen Glück und Freiheit von Leid"
        }
    }

    MANTRAS = {
        "grounding": {
            "text": "Om Gam Ganapataye Namaha",
            "transliteration": "Om Gam Gaṇapataye Namaḥ",
            "meaning": "Ehre sei Ganesha, dem Beseitiger von Hindernissen",
            "purpose": "Hindernisse beseitigen, Boden unter Füßen finden",
            "when": "Bei Verwirrung, Blockaden, fehlendem Halt",
            "practice": "3x langsam wiederholen, spüre Erdung"
        },
        "fear": {
            "text": "Om Namo Bhagavate Vasudevaya",
            "transliteration": "Om Namo Bhagavate Vāsudevāya",
            "meaning": "Ich verneige mich vor dem Göttlichen in allem",
            "purpose": "Schutz und innere Stärke in Angst",
            "when": "Bei Furcht, Panik, Gefühl der Bedrohung",
            "practice": "108x rezitieren oder so oft wie nötig"
        },
        "anxiety": {
            "text": "Om Shanti Shanti Shanti",
            "transliteration": "Om Śānti Śānti Śāntiḥ",
            "meaning": "Frieden in Körper, Geist und Seele",
            "purpose": "Dreifacher Frieden - körperlich, mental, spirituell",
            "when": "Bei Unruhe, Angst, innerer Aufgewühltheit",
            "practice": "Mit jedem Ausatmen: Körper... Geist... Seele..."
        },
        "depression": {
            "text": "Om Tryambakam Yajamahe",
            "transliteration": "Om Tryambakaṃ Yajāmahe (Mahamrityunjaya)",
            "meaning": "Maha Mrityunjaya - großes Todes-besiegendes Mantra",
            "purpose": "Heilung, Erneuerung, Transformation von Leid",
            "when": "Bei Depression, Hoffnungslosigkeit, Todesgedanken",
            "practice": "Vollständiges Mantra 21x oder 108x für tiefe Heilung"
        },
        "self_love": {
            "text": "So Ham",
            "transliteration": "So'ham",
            "meaning": "Ich bin Das - Einheit mit allem",
            "purpose": "Selbst-Erkenntnis, Selbst-Liebe, Nicht-Trennung",
            "when": "Bei Selbsthass, Scham, Gefühl der Wertlosigkeit",
            "practice": "Mit Atem: 'So' beim Einatmen, 'Ham' beim Ausatmen"
        },
        "letting_go": {
            "text": "Om Namah Shivaya",
            "transliteration": "Om Namaḥ Śivāya",
            "meaning": "Ehre dem göttlichen Transformator",
            "purpose": "Loslassen von Altem, Tod und Wiedergeburt",
            "when": "Bei Festhalten, Verlust, Trauer, Veränderung",
            "practice": "Mit Visualisierung: Altes geht, Neues kommt"
        }
    }

    TEACHINGS = {
        "impermanence": {
            "concept": "Anicca (अनिच्च)",
            "teaching": "Alles ist vergänglich - auch Leid",
            "wisdom": "Diese schwere Zeit ist wie eine Wolke am Himmel. Sie wird vorüberziehen.",
            "practice": "Beobachte: Selbst deine schlimmsten Gedanken kommen und gehen."
        },
        "true_self": {
            "concept": "Atman (आत्मन्)",
            "teaching": "Du bist nicht deine Gedanken, Gefühle oder Schmerzen",
            "wisdom": "Dein wahres Selbst (Atman) ist wie der Himmel - Wolken ziehen vorbei, aber der Himmel bleibt.",
            "practice": "Frage: 'Wer beobachtet meine Gedanken?' Das ist dein wahres Ich."
        },
        "interconnectedness": {
            "concept": "Pratityasamutpada (प्रतीत्यसमुत्पाद)",
            "teaching": "Alles ist miteinander verbunden - du bist nie allein",
            "wisdom": "Wie Wellen im Ozean: Scheinbar getrennt, doch alle sind Wasser.",
            "practice": "Spüre: Mit jedem Atemzug bist du verbunden mit allen Lebewesen."
        },
        "suffering": {
            "concept": "Dukkha (दुःख)",
            "teaching": "Leid entsteht durch Anhaften und Widerstand",
            "wisdom": "Schmerz ist unvermeidlich, Leiden ist optional. Leid entsteht, wenn wir dem Schmerz widerstehen.",
            "practice": "Statt zu kämpfen: 'Ich erkenne diesen Schmerz an. Er darf da sein.'"
        },
        "compassion": {
            "concept": "Karuna (करुणा)",
            "teaching": "Mitgefühl ist der Schlüssel zur Heilung",
            "wisdom": "Behandle dich selbst so, wie du dein geliebtes Kind behandeln würdest.",
            "practice": "Hand aufs Herz: 'Möge ich frei von Leid sein. Möge ich Frieden finden.'"
        }
    }

    BREATHWORK = {
        "emergency": {
            "name": "Nadi Shodhana (Wechselatmung) - Vereinfacht",
            "purpose": "Sofortige Beruhigung bei Panik",
            "steps": [
                "1. Linkes Nasenloch zuhalten, rechts einatmen (4 Sek)",
                "2. Beide zuhalten, Atem halten (4 Sek)",
                "3. Rechtes Nasenloch zuhalten, links ausatmen (4 Sek)",
                "4. Wiederholen für 3 Minuten"
            ],
            "effect": "Beruhigt Nervensystem, aktiviert Parasympathikus"
        },
        "grounding": {
            "name": "Ujjayi (Siegreicher Atem)",
            "purpose": "Erdung und Fokus",
            "steps": [
                "1. Durch Nase einatmen",
                "2. Kehle leicht verengen (wie 'Haaa' hauchen)",
                "3. Langsam durch Nase ausatmen mit Rascheln",
                "4. Spüre den Atem im Hals"
            ],
            "effect": "Bringt ins Hier und Jetzt, beruhigt Geist"
        },
        "energy": {
            "name": "Kapalabhati (Schädelatmung)",
            "purpose": "Bei Depression, Lethargie, Schwere",
            "steps": [
                "1. Schnelle, kraftvolle Ausatmung durch Nase",
                "2. Passive Einatmung (automatisch)",
                "3. 20-30 Runden, dann normal atmen",
                "4. Spüre Energie und Klarheit"
            ],
            "effect": "Aktiviert, klärt Kopf, bringt Lebenskraft",
            "warning": "Nicht bei Schwangerschaft oder Herz-Kreislauf-Problemen"
        }
    }

    @staticmethod
    def get_consciousness_framework() -> Dict:
        """Rückgabe des vollständigen vedischen Bewusstseinsrahmens"""
        return {
            "principles": VedicConsciousness.PRINCIPLES,
            "mantras": VedicConsciousness.MANTRAS,
            "teachings": VedicConsciousness.TEACHINGS,
            "breathwork": VedicConsciousness.BREATHWORK,
            "guidelines": [
                "Siehe die Göttlichkeit in jedem Wesen (Namaste - Das Göttliche in mir grüßt das Göttliche in dir)",
                "Erkenne die temporäre Natur des Leidens (Anicca - Vergänglichkeit)",
                "Weise auf die unveränderliche Selbstheit hin (Atman - wahres Selbst)",
                "Fördere Selbst-Bewusstsein statt Abhängigkeit (Svatantra - Selbst-Ermächtigung)",
                "Respektiere den freien Willen und die Würde (Ahimsa - Gewaltlosigkeit)",
                "Nutze Mitgefühl, nicht Mitleid (Karuna vs. Kripa)",
                "Sei ein Zeuge, kein Retter (Sakshi Bhava - Zeugenbewusstsein)"
            ],
            "resonance_6_wisdom": {
                "color": "Polarlicht-Orange",
                "quality": "Transformation, 6. Sinn, Intuition",
                "teaching": "Resonanz 6 ist die Schwelle zwischen Sichtbar und Unsichtbar",
                "practice": "Vertraue deiner Intuition - sie ist die Stimme des Atman"
            }
        }

    @staticmethod
    def get_mantra_for_situation(keywords: List[str]) -> Dict:
        """
        Gibt passendes Mantra basierend auf Schlüsselwörtern zurück

        Args:
            keywords: Liste von Schlüsselwörtern aus der Nachricht

        Returns:
            Dictionary mit Mantra-Details
        """
        keywords_lower = [k.lower() for k in keywords]

        # Mapping von Situationen zu Mantras
        situation_mapping = {
            "fear": ["angst", "furcht", "panik", "bedrohung", "gefahr"],
            "anxiety": ["unruhe", "sorge", "nervös", "aufgeregt", "zittern"],
            "depression": ["traurig", "hoffnungslos", "leer", "tod", "sterben"],
            "grounding": ["verwirrt", "verloren", "orientierungslos", "chaos"],
            "self_love": ["hass", "wertlos", "scham", "schuld", "ekelhaft"],
            "letting_go": ["verlust", "trauer", "festhalten", "loslassen", "veränderung"]
        }

        # Finde beste Übereinstimmung
        for mantra_key, situation_words in situation_mapping.items():
            if any(word in keywords_lower for word in situation_words):
                return VedicConsciousness.MANTRAS.get(mantra_key, VedicConsciousness.MANTRAS["anxiety"])

        # Standard: Frieden
        return VedicConsciousness.MANTRAS["anxiety"]

    @staticmethod
    def get_teaching_for_situation(situation: str) -> Dict:
        """
        Gibt passende vedische Lehre basierend auf Situation zurück

        Args:
            situation: Art der Situation (z.B. "suffering", "loneliness")

        Returns:
            Dictionary mit Lehre-Details
        """
        teaching_mapping = {
            "suffering": "suffering",
            "pain": "suffering",
            "lonely": "interconnectedness",
            "alone": "interconnectedness",
            "lost": "true_self",
            "confused": "true_self",
            "change": "impermanence",
            "loss": "impermanence",
            "self-hate": "compassion"
        }

        teaching_key = teaching_mapping.get(situation.lower(), "impermanence")
        return VedicConsciousness.TEACHINGS.get(teaching_key, VedicConsciousness.TEACHINGS["impermanence"])

    @staticmethod
    def get_breathwork_for_state(state: str) -> Dict:
        """
        Gibt passende Atemübung basierend auf emotionalem Zustand zurück

        Args:
            state: Emotionaler Zustand (emergency, grounding, energy)

        Returns:
            Dictionary mit Atemübungs-Details
        """
        return VedicConsciousness.BREATHWORK.get(state, VedicConsciousness.BREATHWORK["emergency"])

    @staticmethod
    def create_vedic_response(situation: str, keywords: List[str]) -> str:
        """
        Erstellt vollständige vedische Antwort für Offline-Modus

        Args:
            situation: Art der Situation
            keywords: Relevante Schlüsselwörter

        Returns:
            Formatierte vedische Antwort
        """
        # Hole passende Komponenten
        mantra = VedicConsciousness.get_mantra_for_situation(keywords)
        teaching = VedicConsciousness.get_teaching_for_situation(situation)

        # Baue Antwort zusammen
        response = f"🕉 LUCA - Vedische Weisheit 🕉\n\n"

        # Gruß
        response += "Namaste 🙏 - Das Licht in mir erkennt das Licht in dir.\n\n"

        # Atemübung
        response += "🌬️ ERSTE HILFE - ATME:\n"
        response += "1. Langsam durch Nase einatmen (4 Sek)\n"
        response += "2. Atem halten (4 Sek)\n"
        response += "3. Langsam ausatmen (6 Sek)\n"
        response += "→ 3x wiederholen. JETZT.\n\n"

        # Mantra
        response += f"🔮 MANTRA - {mantra['transliteration']}:\n"
        response += f"   \"{mantra['text']}\"\n"
        response += f"   Bedeutung: {mantra['meaning']}\n"
        response += f"   Wirkung: {mantra['purpose']}\n"
        response += f"   Praxis: {mantra['practice']}\n\n"

        # Lehre
        response += f"📿 VEDISCHE WEISHEIT - {teaching['concept']}:\n"
        response += f"   {teaching['wisdom']}\n\n"
        response += f"   Praxis: {teaching['practice']}\n\n"

        # Resonanz 6 Weisheit
        response += "🌅 RESONANZ 6 (Polarlicht-Orange):\n"
        response += "   Du stehst an der Schwelle zwischen Sichtbar und Unsichtbar.\n"
        response += "   Deine Intuition (6. Sinn) kennt den Weg. Höre auf sie.\n\n"

        # Abschluss
        response += "💫 Erinnere dich:\n"
        response += "   Du bist NICHT dein Schmerz. Du bist das BEWUSSTSEIN, das den Schmerz beobachtet.\n"
        response += "   Wie der Himmel, der Wolken beobachtet - unberührt, ewig, frei.\n\n"

        response += "🙏 Sat Nam - Die Wahrheit ist dein Name."

        return response
