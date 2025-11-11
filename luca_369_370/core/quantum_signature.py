"""
Quantum Signature System - S(M) Berechnung
Teil der mathematischen Formalisierung des L.U.C.A 3-6-9 Prinzips

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370 ≈ 0.997297

Mathematische Grundlage:
    Die Quantum Signature S(M) einer Nachricht M ist ein Hash-basierter
    Wert, der die energetische Qualität und Resonanz der Nachricht
    repräsentiert.

    S(M) = hash(M) mod (3 × 6 × 9) = hash(M) mod 162

    Die Signatur wird verwendet um:
    1. Nachrichten in die 3-6-9 Quantisierung einzuordnen
    2. Resonanz zwischen Input und Output zu messen
    3. Fibonacci-Optimierung zu steuern
"""

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class QuantumLevel(Enum):
    """Die drei Quanten-Levels des 3-6-9 Systems"""

    FOUNDATION = 3  # Basis-Level: 369 Tokens
    EXPANSION = 6  # Expansion-Level: 666 Tokens
    MASTERY = 9  # Mastery-Level: 999 Tokens


@dataclass
class QuantumSignature:
    """Quantum Signature einer Nachricht

    Attributes:
        value: Der berechnete Signatur-Wert (0-161)
        level: Das zugeordnete Quanten-Level (3, 6, oder 9)
        resonance: Resonanz-Score (0.0-1.0)
        token_target: Empfohlene Token-Anzahl basierend auf Level
    """

    value: int
    level: QuantumLevel
    resonance: float
    token_target: int

    def __post_init__(self):
        """Validiert die Signatur nach Initialisierung"""
        if not 0 <= self.value < 162:
            raise ValueError(f"Signatur-Wert muss 0-161 sein, ist {self.value}")
        if not 0.0 <= self.resonance <= 1.0:
            raise ValueError(f"Resonanz muss 0.0-1.0 sein, ist {self.resonance}")


class QuantumSignatureEngine:
    """Engine zur Berechnung von Quantum Signatures

    Diese Engine implementiert die S(M) Funktion aus der mathematischen
    Formalisierung und ordnet Nachrichten den 3-6-9 Quanten-Levels zu.
    """

    # Quanten-Level Zuordnungen (basierend auf Signatur-Wert)
    LEVEL_THRESHOLDS = {
        QuantumLevel.FOUNDATION: (0, 54),  # 0-53: Level 3 → 369 Tokens
        QuantumLevel.EXPANSION: (54, 108),  # 54-107: Level 6 → 666 Tokens
        QuantumLevel.MASTERY: (108, 162),  # 108-161: Level 9 → 999 Tokens
    }

    # Target Token-Anzahlen für jedes Level
    TOKEN_TARGETS = {
        QuantumLevel.FOUNDATION: 369,
        QuantumLevel.EXPANSION: 666,
        QuantumLevel.MASTERY: 999,
    }

    def __init__(self):
        """Initialisiert die Quantum Signature Engine"""
        self.quality_standard = 369 / 370  # ≈ 0.997297

    def calculate_signature(self, message: str) -> QuantumSignature:
        """Berechnet die Quantum Signature S(M) einer Nachricht

        Args:
            message: Die zu analysierende Nachricht

        Returns:
            QuantumSignature: Vollständige Signatur-Analyse

        Mathematik:
            S(M) = SHA256(M) mod 162
            wobei 162 = 3 × 6 × 9 × 3 (erweiterte Quanten-Basis)
        """
        # Berechne Hash-Wert
        hash_value = self._compute_hash(message)

        # Extrahiere Signatur-Wert (mod 162)
        signature_value = hash_value % 162

        # Bestimme Quanten-Level
        level = self._determine_level(signature_value)

        # Berechne Resonanz
        resonance = self._calculate_resonance(message, level)

        # Hole Token-Target
        token_target = self.TOKEN_TARGETS[level]

        return QuantumSignature(
            value=signature_value,
            level=level,
            resonance=resonance,
            token_target=token_target,
        )

    def _compute_hash(self, message: str) -> int:
        """Berechnet SHA256 Hash als Integer

        Args:
            message: Nachricht zum Hashen

        Returns:
            int: Hash-Wert als Integer
        """
        hash_obj = hashlib.sha256(message.encode("utf-8"))
        return int(hash_obj.hexdigest(), 16)

    def _determine_level(self, signature_value: int) -> QuantumLevel:
        """Bestimmt Quanten-Level basierend auf Signatur-Wert

        Args:
            signature_value: Berechneter Signatur-Wert (0-161)

        Returns:
            QuantumLevel: Zugeordnetes Level
        """
        for level, (min_val, max_val) in self.LEVEL_THRESHOLDS.items():
            if min_val <= signature_value < max_val:
                return level

        # Fallback (sollte nicht erreicht werden)
        return QuantumLevel.FOUNDATION

    def _calculate_resonance(self, message: str, level: QuantumLevel) -> float:
        """Berechnet Resonanz-Score der Nachricht

        Die Resonanz misst wie gut die Nachricht mit dem zugeordneten
        Quanten-Level harmoniert.

        Args:
            message: Die Nachricht
            level: Das zugeordnete Quanten-Level

        Returns:
            float: Resonanz-Score (0.0-1.0)

        Mathematik:
            Resonance = base_resonance × (1 + fibonacci_factor)
            wobei fibonacci_factor die Fibonacci-Eigenschaften der Nachricht misst
        """
        # Basis-Resonanz aus Nachrichtenlänge
        base_resonance = self._base_resonance(len(message))

        # Fibonacci-Factor (wie gut passt die Länge zur Fibonacci-Sequenz?)
        fib_factor = self._fibonacci_factor(len(message))

        # Level-Bonus (höhere Levels = höhere Resonanz bei guter Passung)
        level_bonus = level.value / 9.0  # 3/9, 6/9, 9/9 = 0.33, 0.67, 1.0

        # Kombinierte Resonanz
        resonance = base_resonance * (1 + fib_factor * level_bonus)

        # Normalisiere auf 0.0-1.0
        return min(resonance, 1.0)

    def _base_resonance(self, length: int) -> float:
        """Berechnet Basis-Resonanz aus Nachrichtenlänge

        Args:
            length: Länge der Nachricht

        Returns:
            float: Basis-Resonanz (0.0-1.0)
        """
        # Optimale Längen: ~369, ~666, ~999 Zeichen
        # Berechne Distanz zur nächsten optimalen Länge
        targets = [369, 666, 999]
        min_distance = min(abs(length - target) for target in targets)

        # Konvertiere Distanz zu Resonanz (je näher, desto höher)
        # Max-Distanz für Normalisierung: 500 Zeichen
        max_distance = 500
        resonance = 1.0 - (min_distance / max_distance)

        return max(0.0, resonance)

    def _fibonacci_factor(self, length: int) -> float:
        """Berechnet Fibonacci-Factor der Nachrichtenlänge

        Args:
            length: Länge der Nachricht

        Returns:
            float: Fibonacci-Factor (0.0-1.0)
        """
        # Fibonacci-Sequenz bis ~1000
        fibonacci = [
            1,
            1,
            2,
            3,
            5,
            8,
            13,
            21,
            34,
            55,
            89,
            144,
            233,
            377,
            610,
            987,
        ]

        # Finde nächste Fibonacci-Zahl
        min_distance = min(abs(length - fib) for fib in fibonacci)

        # Konvertiere zu Factor (je näher, desto höher)
        max_distance = 100
        factor = 1.0 - (min_distance / max_distance)

        return max(0.0, factor)

    def calculate_resonance_between(
        self, input_message: str, output_message: str
    ) -> float:
        """Berechnet Resonanz zwischen Input und Output

        Diese Funktion misst wie gut Input und Output harmonieren.
        Hohe Resonanz = gutes Flow, niedrige Resonanz = Dissonanz.

        Args:
            input_message: Input-Nachricht
            output_message: Output-Nachricht

        Returns:
            float: Resonanz-Score zwischen Messages (0.0-1.0)
        """
        # Berechne Signaturen
        input_sig = self.calculate_signature(input_message)
        output_sig = self.calculate_signature(output_message)

        # Resonanz-Komponenten:
        # 1. Level-Kompatibilität (gleiche oder benachbarte Levels)
        level_compatibility = self._level_compatibility(
            input_sig.level, output_sig.level
        )

        # 2. Signatur-Harmonie (ähnliche Signatur-Werte)
        sig_harmony = self._signature_harmony(input_sig.value, output_sig.value)

        # 3. Individuelle Resonanzen
        avg_resonance = (input_sig.resonance + output_sig.resonance) / 2

        # Kombinierte Resonanz (gewichtet)
        total_resonance = (
            0.4 * level_compatibility + 0.3 * sig_harmony + 0.3 * avg_resonance
        )

        return total_resonance

    def _level_compatibility(self, level1: QuantumLevel, level2: QuantumLevel) -> float:
        """Berechnet Kompatibilität zwischen zwei Levels

        Args:
            level1: Erstes Level
            level2: Zweites Level

        Returns:
            float: Kompatibilität (0.0-1.0)
        """
        # Gleiche Levels = perfekte Kompatibilität
        if level1 == level2:
            return 1.0

        # Benachbarte Levels = gute Kompatibilität
        level_distance = abs(level1.value - level2.value)
        if level_distance == 3:  # 3-6 oder 6-9
            return 0.7

        # Entfernte Levels = moderate Kompatibilität
        return 0.4  # 3-9

    def _signature_harmony(self, sig1: int, sig2: int) -> float:
        """Berechnet Harmonie zwischen zwei Signatur-Werten

        Args:
            sig1: Erste Signatur (0-161)
            sig2: Zweite Signatur (0-161)

        Returns:
            float: Harmonie (0.0-1.0)
        """
        # Berechne Distanz
        distance = abs(sig1 - sig2)

        # Normalisiere (max distance = 161)
        harmony = 1.0 - (distance / 161.0)

        return harmony


# === EXPORT ===

__all__ = [
    "QuantumSignature",
    "QuantumSignatureEngine",
    "QuantumLevel",
]
