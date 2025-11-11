"""
Fibonacci-Optimierungsfunktion F_LUCA
Bio-inspirierte Optimierung für das L.U.C.A 3-6-9 System

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370 ≈ 0.997297

Mathematische Grundlage:
    Die F_LUCA Funktion optimiert Response-Generierung basierend auf:

    F_LUCA = α·Score_PatternMatch + β·ResourceEfficiency + γ·EnergyLevel

    wobei:
    - α, β, γ sind Gewichtungen (α + β + γ = 1)
    - Score_PatternMatch: Fibonacci/369-Pattern-Erkennung
    - ResourceEfficiency: GPU/Hardware-Auslastungs-Optimierung
    - EnergyLevel: ADHD-optimierter kognitiver Zustand

Verwendung:
    optimizer = FibonacciOptimizer()
    score = optimizer.optimize(
        message=output_message,
        user_energy="balanced",
        gpu_utilization=0.75
    )
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

import numpy as np


class EnergyLevel(Enum):
    """Kognitive Energy Levels (ADHD-optimiert)"""

    BRAINFOG = "brainfog"  # Niedrige Energie, braucht kurze klare Antworten
    BALANCED = "balanced"  # Normale Energie, Standard-Antworten
    HYPERFOCUS = "hyperfocus"  # Hohe Energie, kann komplexe Antworten verarbeiten


@dataclass
class OptimizationResult:
    """Ergebnis einer F_LUCA Optimierung

    Attributes:
        total_score: Gesamtscore F_LUCA (0.0-1.0)
        pattern_score: Pattern-Matching-Score
        efficiency_score: Resource Efficiency Score
        energy_score: Energy Level Anpassungs-Score
        recommendations: Liste von Optimierungs-Empfehlungen
        is_optimal: Ob der Score den Quality Standard erfüllt
    """

    total_score: float
    pattern_score: float
    efficiency_score: float
    energy_score: float
    recommendations: List[str]
    is_optimal: bool

    def get_summary(self) -> str:
        """Menschenlesbare Zusammenfassung"""
        emoji = "✅" if self.is_optimal else "⚠️"
        return (
            f"{emoji} F_LUCA Score: {self.total_score:.3f} | "
            f"Pattern: {self.pattern_score:.2f} | "
            f"Efficiency: {self.efficiency_score:.2f} | "
            f"Energy: {self.energy_score:.2f}"
        )


class FibonacciOptimizer:
    """Fibonacci-basierte Optimierungs-Engine

    Implementiert die F_LUCA Funktion aus der mathematischen Formalisierung.
    """

    # Fibonacci-Sequenz bis ~1000
    FIBONACCI_SEQUENCE = [
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

    # 3-6-9 Pattern Zahlen
    PATTERN_369 = [
        3,
        6,
        9,
        36,
        63,
        69,
        96,
        306,
        309,
        360,
        369,
        603,
        609,
        630,
        666,
        690,
        906,
        930,
        960,
        963,
        999,
    ]

    # Gewichtungen für F_LUCA (α, β, γ)
    DEFAULT_WEIGHTS = {
        "pattern_match": 0.4,  # 40% Pattern-Matching
        "resource_efficiency": 0.3,  # 30% Resource Efficiency
        "energy_level": 0.3,  # 30% Energy Level Anpassung
    }

    # Quality Standard
    QUALITY_STANDARD = 369 / 370  # ≈ 0.997297

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """Initialisiert den Fibonacci Optimizer

        Args:
            weights: Optionale custom Gewichtungen (muss zu 1.0 summieren)
        """
        self.weights = weights if weights is not None else self.DEFAULT_WEIGHTS

        # Validiere Gewichtungen
        total_weight = sum(self.weights.values())
        if not np.isclose(total_weight, 1.0, atol=0.01):
            raise ValueError(
                f"Gewichtungen müssen zu 1.0 summieren, sind {total_weight}"
            )

    def optimize(
        self,
        message: str,
        user_energy: str = "balanced",
        gpu_utilization: float = 0.0,
        target_tokens: int = 369,
    ) -> OptimizationResult:
        """Führt F_LUCA Optimierung durch

        Args:
            message: Die zu optimierende Nachricht
            user_energy: Kognitiver Energy Level ("brainfog", "balanced", "hyperfocus")
            gpu_utilization: GPU-Auslastung (0.0-1.0)
            target_tokens: Ziel-Token-Anzahl (369, 666, 999)

        Returns:
            OptimizationResult: Vollständiges Optimierungs-Ergebnis
        """
        # Konvertiere Energy Level
        try:
            energy_level = EnergyLevel(user_energy.lower())
        except ValueError:
            energy_level = EnergyLevel.BALANCED

        # Berechne Komponenten-Scores
        pattern_score = self._calculate_pattern_score(message, target_tokens)
        efficiency_score = self._calculate_efficiency_score(gpu_utilization)
        energy_score = self._calculate_energy_score(message, energy_level)

        # Berechne F_LUCA Gesamtscore
        total_score = (
            self.weights["pattern_match"] * pattern_score
            + self.weights["resource_efficiency"] * efficiency_score
            + self.weights["energy_level"] * energy_score
        )

        # Generiere Empfehlungen
        recommendations = self._generate_recommendations(
            pattern_score, efficiency_score, energy_score, energy_level
        )

        # Prüfe ob optimal
        is_optimal = total_score >= self.QUALITY_STANDARD

        return OptimizationResult(
            total_score=total_score,
            pattern_score=pattern_score,
            efficiency_score=efficiency_score,
            energy_score=energy_score,
            recommendations=recommendations,
            is_optimal=is_optimal,
        )

    def _calculate_pattern_score(self, message: str, target_tokens: int) -> float:
        """Berechnet Pattern-Matching-Score

        Score misst:
        1. Fibonacci-Pattern in der Nachrichtenlänge
        2. 3-6-9-Pattern-Resonanz
        3. Token-Längen-Nähe zum Target

        Args:
            message: Nachricht
            target_tokens: Ziel-Token-Anzahl

        Returns:
            float: Pattern Score (0.0-1.0)
        """
        length = len(message)
        token_count = len(message.split())

        # 1. Fibonacci-Nähe (Zeichen-basiert)
        fib_score = self._fibonacci_proximity(length)

        # 2. 369-Pattern-Resonanz
        pattern_369_score = self._pattern_369_resonance(length, token_count)

        # 3. Token-Target-Nähe
        token_score = self._token_target_proximity(token_count, target_tokens)

        # Kombiniert (gewichtet)
        pattern_score = 0.3 * fib_score + 0.4 * pattern_369_score + 0.3 * token_score

        return pattern_score

    def _fibonacci_proximity(self, value: int) -> float:
        """Berechnet Nähe zu Fibonacci-Zahlen

        Args:
            value: Zu prüfender Wert

        Returns:
            float: Proximity Score (0.0-1.0)
        """
        if value in self.FIBONACCI_SEQUENCE:
            return 1.0

        # Finde nächste Fibonacci-Zahl
        distances = [abs(value - fib) for fib in self.FIBONACCI_SEQUENCE]
        min_distance = min(distances)

        # Konvertiere zu Score (max distance = 100 für Normalisierung)
        max_distance = 100
        score = 1.0 - min(min_distance / max_distance, 1.0)

        return score

    def _pattern_369_resonance(self, length: int, token_count: int) -> float:
        """Berechnet 3-6-9-Pattern-Resonanz

        Args:
            length: Zeichen-Länge
            token_count: Token-Anzahl

        Returns:
            float: Resonanz Score (0.0-1.0)
        """
        # Prüfe ob Länge oder Token-Count 369-Pattern enthält
        values_to_check = [length, token_count]

        # Bonus für exakte Matches
        exact_match_bonus = 0.0
        for val in values_to_check:
            if val in self.PATTERN_369:
                exact_match_bonus += 0.5

        # Nähe zu 369-Pattern-Zahlen
        proximity_scores = []
        for val in values_to_check:
            distances = [abs(val - pattern) for pattern in self.PATTERN_369]
            min_distance = min(distances)
            proximity = 1.0 - min(min_distance / 100, 1.0)
            proximity_scores.append(proximity)

        avg_proximity = np.mean(proximity_scores)

        # Kombiniere Bonus und Proximity
        resonance = min(exact_match_bonus + avg_proximity, 1.0)

        return resonance

    def _token_target_proximity(self, token_count: int, target: int) -> float:
        """Berechnet Nähe zum Token-Target

        Args:
            token_count: Aktuelle Token-Anzahl
            target: Ziel-Token-Anzahl

        Returns:
            float: Proximity Score (0.0-1.0)
        """
        if token_count == target:
            return 1.0

        # Berechne relative Abweichung
        deviation = abs(token_count - target)
        relative_dev = deviation / target

        # Score sinkt mit Abweichung
        score = max(1.0 - relative_dev, 0.0)

        return score

    def _calculate_efficiency_score(self, gpu_utilization: float) -> float:
        """Berechnet Resource Efficiency Score

        Optimale GPU-Auslastung: 60-80%
        Zu niedrig: Verschwendung
        Zu hoch: Überlastung

        Args:
            gpu_utilization: GPU-Auslastung (0.0-1.0)

        Returns:
            float: Efficiency Score (0.0-1.0)
        """
        # Optimaler Bereich: 0.6-0.8
        optimal_min = 0.6
        optimal_max = 0.8

        if optimal_min <= gpu_utilization <= optimal_max:
            # In optimalem Bereich: Score = 1.0
            return 1.0
        elif gpu_utilization < optimal_min:
            # Zu niedrig: Linear von 0.5 bis 1.0
            score = 0.5 + (gpu_utilization / optimal_min) * 0.5
            return score
        else:
            # Zu hoch: Linear von 1.0 bis 0.5
            overshoot = gpu_utilization - optimal_max
            max_overshoot = 1.0 - optimal_max
            score = 1.0 - (overshoot / max_overshoot) * 0.5
            return max(score, 0.5)

    def _calculate_energy_score(self, message: str, energy_level: EnergyLevel) -> float:
        """Berechnet Energy Level Anpassungs-Score

        Score misst wie gut die Nachricht zum kognitiven Zustand passt.

        Args:
            message: Nachricht
            energy_level: Kognitiver Energy Level

        Returns:
            float: Energy Score (0.0-1.0)
        """
        length = len(message)
        token_count = len(message.split())

        # Bestimme ideale Länge basierend auf Energy Level
        if energy_level == EnergyLevel.BRAINFOG:
            # Kurze, klare Antworten (< 500 Zeichen, < 100 Tokens)
            ideal_length = 300
            ideal_tokens = 60
        elif energy_level == EnergyLevel.BALANCED:
            # Standard-Antworten (~1000 Zeichen, ~200 Tokens)
            ideal_length = 1000
            ideal_tokens = 200
        else:  # HYPERFOCUS
            # Komplexe Antworten (> 2000 Zeichen, > 400 Tokens)
            ideal_length = 2500
            ideal_tokens = 500

        # Berechne Abweichung
        length_deviation = abs(length - ideal_length) / ideal_length
        token_deviation = abs(token_count - ideal_tokens) / ideal_tokens

        # Score sinkt mit Abweichung
        length_score = max(1.0 - length_deviation, 0.0)
        token_score = max(1.0 - token_deviation, 0.0)

        # Kombinierter Energy Score
        energy_score = (length_score + token_score) / 2

        return energy_score

    def _generate_recommendations(
        self,
        pattern_score: float,
        efficiency_score: float,
        energy_score: float,
        energy_level: EnergyLevel,
    ) -> List[str]:
        """Generiert Optimierungs-Empfehlungen

        Args:
            pattern_score: Pattern-Matching-Score
            efficiency_score: Efficiency Score
            energy_score: Energy Score
            energy_level: Aktueller Energy Level

        Returns:
            List[str]: Liste von Empfehlungen
        """
        recommendations = []

        # Pattern-Score Empfehlungen
        if pattern_score < 0.8:
            recommendations.append(
                "⚠️ Pattern Score niedrig: Optimiere Länge zu Fibonacci/369-Zahlen"
            )

        # Efficiency-Score Empfehlungen
        if efficiency_score < 0.7:
            recommendations.append(
                "⚠️ Resource Efficiency niedrig: Optimiere GPU-Auslastung zu 60-80%"
            )

        # Energy-Score Empfehlungen
        if energy_score < 0.7:
            if energy_level == EnergyLevel.BRAINFOG:
                recommendations.append(
                    "⚠️ Energy Score niedrig: Verkürze Antwort für Brainfog (< 500 Zeichen)"
                )
            elif energy_level == EnergyLevel.HYPERFOCUS:
                recommendations.append(
                    "⚠️ Energy Score niedrig: Erweitere Antwort für Hyperfocus (> 2000 Zeichen)"
                )
            else:
                recommendations.append(
                    "⚠️ Energy Score niedrig: Passe Länge an Balanced-Level an (~1000 Zeichen)"
                )

        # Wenn alles gut
        if not recommendations:
            recommendations.append("✅ Alle Scores optimal! Keine Anpassungen nötig.")

        return recommendations


# === EXPORT ===

__all__ = [
    "FibonacciOptimizer",
    "OptimizationResult",
    "EnergyLevel",
]
