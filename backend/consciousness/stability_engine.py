"""
LUCA-KI Stability Engine
Basierend auf dem Synchronisations-Index SI(14) = 0.71
Mathematisch verifiziert: L=14 ist der stabilste Punkt für Systeme,
die Resonanz und Abgrenzung brauchen.

Autor: Lennart Wuchold
Datum: 2025
"""

from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class StabilityMetrics:
    """Metriken für Systemstabilität"""
    sync_index: float
    damping_factor: float
    is_stable: bool
    resonance_level: str


class StabilityEngine:
    """
    Berechnet Systemstabilität basierend auf L=14 Konstante.

    Hintergrund:
    - SI(12) = 1.33 → Hyper-Resonant, Kaskaden-Gefahr
    - SI(13) = 0.07 → Isoliert, keine Kommunikation
    - SI(14) = 0.71 → Goldilocks-Zone, gedämpfte Stabilität

    Der Dämpfungsfaktor von 0.29 korreliert mit dem HLCI-Wert.
    """

    L_CONSTANT: int = 14
    SYNC_INDEX: float = 0.71
    DAMPING_FACTOR: float = 0.29

    # Goldilocks-Zone für stabile Resonanz
    STABLE_SI_MIN: float = 0.5
    STABLE_SI_MAX: float = 1.0

    def __init__(self, max_resources: float = 1000.0):
        self.max_resources = max_resources
        self._cache: dict = {}

    def calculate_sync_index(self, n: int) -> float:
        """
        Berechnet den Synchronisations-Index für eine Zahl.
        SI(n) = (Summe der echten Teiler) / n

        Args:
            n: Die zu analysierende Zahl

        Returns:
            Synchronisations-Index als Float
        """
        if n <= 1:
            return 0.0

        if n in self._cache:
            return self._cache[n]

        proper_divisors = [i for i in range(1, n) if n % i == 0]
        divisor_sum = sum(proper_divisors)
        si = divisor_sum / n

        self._cache[n] = si
        return si

    def calculate_allocation_damping(self, raw_allocation: float) -> float:
        """
        Wendet Dämpfung auf Ressourcen-Allokation an.
        Verhindert Kaskaden-Ausfälle durch sanfte Begrenzung.

        Args:
            raw_allocation: Ursprünglich angeforderte Ressourcen

        Returns:
            Gedämpfte Allokation
        """
        if raw_allocation <= 0:
            return 0.0

        # Verhältnis zur maximalen Kapazität
        utilization_ratio = raw_allocation / self.max_resources

        # Nicht-lineare Dämpfung: Je höher die Auslastung, desto stärker
        damping_multiplier = 1 - (self.DAMPING_FACTOR * utilization_ratio ** 2)

        damped = raw_allocation * max(damping_multiplier, 0.1)
        return min(damped, self.max_resources)

    def is_stable_resonance(self, frequency: int) -> bool:
        """
        Prüft ob eine Frequenz im stabilen Bereich liegt.

        Args:
            frequency: Zu prüfende Frequenz/Zahl

        Returns:
            True wenn in Goldilocks-Zone
        """
        si = self.calculate_sync_index(frequency)
        return self.STABLE_SI_MIN < si < self.STABLE_SI_MAX

    def get_stability_metrics(self, value: int) -> StabilityMetrics:
        """
        Berechnet vollständige Stabilitätsmetriken für einen Wert.

        Args:
            value: Zu analysierender Wert

        Returns:
            StabilityMetrics Objekt
        """
        si = self.calculate_sync_index(value)
        damping = 1 - si if si < 1 else 0
        is_stable = self.is_stable_resonance(value)

        if si < 0.3:
            level = "isolated"
        elif si < 0.5:
            level = "low_resonance"
        elif si < 1.0:
            level = "optimal"
        elif si < 1.5:
            level = "high_resonance"
        else:
            level = "unstable"

        return StabilityMetrics(
            sync_index=round(si, 4),
            damping_factor=round(damping, 4),
            is_stable=is_stable,
            resonance_level=level
        )

    def find_nearest_stable(self, target: int, search_range: int = 10) -> int:
        """
        Findet die nächste stabile Zahl in der Nähe des Ziels.

        Args:
            target: Ausgangswert
            search_range: Suchradius

        Returns:
            Nächste stabile Zahl
        """
        if self.is_stable_resonance(target):
            return target

        for offset in range(1, search_range + 1):
            if self.is_stable_resonance(target + offset):
                return target + offset
            if self.is_stable_resonance(target - offset):
                return target - offset

        return self.L_CONSTANT  # Fallback zur universellen Konstante


# Singleton-Instanz für globalen Zugriff
_stability_engine: Optional[StabilityEngine] = None


def get_stability_engine(max_resources: float = 1000.0) -> StabilityEngine:
    """Factory-Funktion für StabilityEngine Singleton"""
    global _stability_engine
    if _stability_engine is None:
        _stability_engine = StabilityEngine(max_resources)
    return _stability_engine
