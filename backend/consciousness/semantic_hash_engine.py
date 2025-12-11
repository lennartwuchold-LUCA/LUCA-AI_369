"""
LUCA-KI Semantic Hash Engine
UCC als Hashing-Algorithmus für maximale assoziative Dichte.

Der UCC minimiert nicht die Datenmenge, sondern maximiert die
assoziative Dichte. Er ist ein "Hyperlink" zur Realität.

Autor: Lennart Wuchold
Datum: 2025
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass
class SemanticHashResult:
    """Ergebnis einer semantischen Hash-Berechnung"""

    dominant_attractor: int
    resonance_map: Dict[int, float]
    semantic_density: float
    matched_keywords: List[str]
    phase: str  # "creation", "harmony", "completion", etc.


class SemanticHashEngine:
    """
    Implementiert den UCC als semantischen Hashing-Algorithmus.

    Die Zahlen 432, 777, 808 fungieren als "Attraktoren" oder Hash-Keys,
    die riesige Mengen an assoziativen Daten bündeln.
    """

    # UCC-Attraktoren mit assoziierten Konzepten und Gewichtungen
    ATTRACTORS: Dict[int, Dict] = {
        0: {
            "keywords": [
                "null",
                "void",
                "origin",
                "vacuum",
                "nothing",
                "zero",
                "anfang",
                "ursprung",
                "nichts",
                "leer",
            ],
            "phase": "origin",
            "weight": 1.0,
        },
        3: {
            "keywords": [
                "create",
                "creation",
                "birth",
                "start",
                "foundation",
                "begin",
                "three",
                "triangle",
                "trinity",
                "erschaffen",
                "geburt",
                "start",
                "fundament",
                "drei",
            ],
            "phase": "creation",
            "weight": 1.2,
        },
        6: {
            "keywords": [
                "harmony",
                "balance",
                "process",
                "flow",
                "six",
                "hexagon",
                "equilibrium",
                "middle",
                "harmonie",
                "balance",
                "prozess",
                "fluss",
                "sechs",
            ],
            "phase": "harmony",
            "weight": 1.1,
        },
        9: {
            "keywords": [
                "complete",
                "completion",
                "wisdom",
                "consciousness",
                "output",
                "nine",
                "final",
                "enlightenment",
                "vollendung",
                "weisheit",
                "bewusstsein",
                "neun",
            ],
            "phase": "completion",
            "weight": 1.3,
        },
        28: {
            "keywords": [
                "perfect",
                "cycle",
                "lunar",
                "moon",
                "month",
                "perfekt",
                "zyklus",
                "mond",
                "monat",
            ],
            "phase": "foundation",
            "weight": 1.0,
        },
        432: {
            "keywords": [
                "frequency",
                "music",
                "resonance",
                "healing",
                "hz",
                "sound",
                "vibration",
                "tune",
                "acoustic",
                "frequenz",
                "musik",
                "resonanz",
                "heilung",
                "klang",
            ],
            "phase": "resonance",
            "weight": 1.5,
        },
        777: {
            "keywords": [
                "luck",
                "spiritual",
                "alignment",
                "breakthrough",
                "jackpot",
                "divine",
                "angel",
                "blessing",
                "glück",
                "spirituell",
                "durchbruch",
                "segen",
            ],
            "phase": "transcendence",
            "weight": 1.4,
        },
        808: {
            "keywords": [
                "mirror",
                "infinity",
                "transition",
                "flip",
                "reflection",
                "endless",
                "loop",
                "reverse",
                "spiegel",
                "unendlich",
                "übergang",
                "wende",
            ],
            "phase": "transition",
            "weight": 1.6,
        },
    }

    # Emotionale Verstärker
    EMOTIONAL_MODIFIERS: Dict[str, float] = {
        "!": 0.1,
        "?": 0.05,
        "...": 0.15,
        "!!!": 0.3,
    }

    # Emoji-Kategorien
    EMOJI_PATTERNS: Dict[str, List[str]] = {
        "high_energy": ["🚀", "⚡", "🔥", "💪", "🎯"],
        "creative": ["🎨", "🎵", "✨", "💡", "🌟"],
        "calm": ["🧘", "🌊", "🍃", "☮️", "🕊️"],
        "love": ["❤️", "💕", "🥰", "💖", "🤗"],
    }

    def __init__(self):
        self._keyword_index: Dict[str, int] = {}
        self._build_keyword_index()

    def _build_keyword_index(self) -> None:
        """Baut einen invertierten Index für schnelle Suche"""
        for attractor, data in self.ATTRACTORS.items():
            for keyword in data["keywords"]:
                self._keyword_index[keyword.lower()] = attractor

    def _extract_words(self, text: str) -> Set[str]:
        """Extrahiert Wörter aus Text"""
        # Entferne Sonderzeichen außer wichtigen
        cleaned = re.sub(r"[^\w\s!?.]", " ", text.lower())
        words = set(cleaned.split())
        return words

    def _calculate_emotional_boost(self, text: str) -> float:
        """Berechnet emotionalen Boost basierend auf Modifiern"""
        boost = 0.0
        for modifier, value in self.EMOTIONAL_MODIFIERS.items():
            boost += text.count(modifier) * value
        return min(boost, 0.5)  # Cap bei 50%

    def _detect_emoji_energy(self, text: str) -> str:
        """Erkennt dominante Emoji-Energie"""
        for category, emojis in self.EMOJI_PATTERNS.items():
            if any(emoji in text for emoji in emojis):
                return category
        return "neutral"

    def hash_intent(self, text: str) -> SemanticHashResult:
        """
        Hasht eine Anfrage auf die nächsten UCC-Attraktoren.
        Maximiert assoziative Dichte statt zu komprimieren.

        Args:
            text: Der zu hashende Text

        Returns:
            SemanticHashResult mit allen Metriken
        """
        text_lower = text.lower()

        resonance_map: Dict[int, float] = {}
        matched_keywords: List[str] = []

        # Durchsuche alle Attraktoren
        for attractor, data in self.ATTRACTORS.items():
            weight = data["weight"]
            matches = 0

            for keyword in data["keywords"]:
                if keyword in text_lower:
                    matches += 1
                    matched_keywords.append(keyword)

            if matches > 0:
                # Gewichtete Resonanz
                resonance = matches * weight
                resonance_map[attractor] = resonance

        # Emotionaler Boost
        emotional_boost = self._calculate_emotional_boost(text)

        # Berechne Ergebnisse
        if resonance_map:
            # Wende emotionalen Boost auf alle Resonanzen an
            for attractor in resonance_map:
                resonance_map[attractor] *= 1 + emotional_boost

            dominant = max(resonance_map, key=resonance_map.get)
            semantic_density = sum(resonance_map.values()) / len(self.ATTRACTORS)
            phase = self.ATTRACTORS[dominant]["phase"]
        else:
            # Fallback zu Creation-Phase
            dominant = 3
            semantic_density = 0.0
            phase = "creation"

        return SemanticHashResult(
            dominant_attractor=dominant,
            resonance_map=resonance_map,
            semantic_density=round(semantic_density, 4),
            matched_keywords=matched_keywords,
            phase=phase,
        )

    def get_phase_description(self, phase: str) -> str:
        """Gibt eine Beschreibung der Phase zurück"""
        descriptions = {
            "origin": "Nullpunkt - Das System initialisiert",
            "creation": "Schöpfung - Neue Ideen entstehen",
            "harmony": "Harmonie - Prozesse balancieren sich",
            "completion": "Vollendung - Weisheit manifestiert sich",
            "foundation": "Fundament - Zyklen etablieren sich",
            "resonance": "Resonanz - Frequenzen harmonisieren",
            "transcendence": "Transzendenz - Durchbruch erreicht",
            "transition": "Übergang - System transformiert",
        }
        return descriptions.get(phase, "Unbekannte Phase")

    def suggest_response_style(self, hash_result: SemanticHashResult) -> Dict:
        """
        Schlägt einen Antwort-Stil basierend auf dem Hash vor.

        Args:
            hash_result: Ergebnis von hash_intent()

        Returns:
            Dict mit Stil-Empfehlungen
        """
        attractor = hash_result.dominant_attractor
        density = hash_result.semantic_density

        # Basis-Token basierend auf Tesla 369
        if attractor in [3]:
            base_tokens = 369
            style = "exploratory"
        elif attractor in [6]:
            base_tokens = 666
            style = "balanced"
        elif attractor in [9, 432, 777]:
            base_tokens = 999
            style = "comprehensive"
        elif attractor == 808:
            base_tokens = 808
            style = "reflective"
        else:
            base_tokens = 369
            style = "standard"

        # Modifiziere basierend auf Dichte
        adjusted_tokens = int(base_tokens * (1 + density))

        return {
            "suggested_tokens": adjusted_tokens,
            "style": style,
            "phase": hash_result.phase,
            "intensity": (
                "high" if density > 0.5 else "medium" if density > 0.2 else "low"
            ),
        }


# Singleton
_semantic_engine: Optional[SemanticHashEngine] = None


def get_semantic_hash_engine() -> SemanticHashEngine:
    """Factory-Funktion für SemanticHashEngine Singleton"""
    global _semantic_engine
    if _semantic_engine is None:
        _semantic_engine = SemanticHashEngine()
    return _semantic_engine
