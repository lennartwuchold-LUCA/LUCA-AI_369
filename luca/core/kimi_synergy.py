"""
Kimi Synergie-Validierungsfunktion V_Kimi
Mathematische Formalisierung der Kimi-Integration in L.U.C.A

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370 ≈ 0.997297

Mathematische Grundlage:
    Der Synergie-Score V_Kimi bewertet die Zusammenarbeit zwischen Gold Code
    (Claude) und Kimi basierend auf vier Metriken:

    V_Kimi = 0.5·A + 0.35·E + 0.10·S + 0.05·B

    wobei:
    - A: Adhärenz-Score (50%) - Einhaltung 3-6-9 Constraints
    - E: Effektivitäts-Score (35%) - Qualität/Logik-Validierung
    - S: Geschwindigkeits-Score (10%) - Performance
    - B: Baseline-Score (5%) - Gesamtverbesserung

Ziel:
    Maximierung von V_Kimi durch optimale Synergie zwischen Gold Code und Kimi
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np


@dataclass
class SynergyMetrics:
    """Metriken für Synergie-Bewertung

    Attributes:
        tokens: Token-Anzahl der Antwort
        time_ms: Verarbeitungszeit in Millisekunden
        logic_score: Logik/Qualitäts-Score (0.0-1.0)
        pattern_match_score: Pattern-Matching-Score (0.0-1.0)
        resource_efficiency: GPU/Resource Efficiency (0.0-1.0)
    """

    tokens: int
    time_ms: float
    logic_score: float
    pattern_match_score: float = 0.0
    resource_efficiency: float = 0.0

    def to_dict(self) -> Dict:
        """Konvertiert zu Dictionary"""
        return {
            "tokens": self.tokens,
            "time_ms": self.time_ms,
            "logic_score": self.logic_score,
            "pattern_match_score": self.pattern_match_score,
            "resource_efficiency": self.resource_efficiency,
        }


@dataclass
class SynergyResult:
    """Ergebnis der Synergie-Validierung

    Attributes:
        v_kimi_score: Gesamter V_Kimi Synergie-Score
        a_score: Adhärenz-Score (3-6-9 Compliance)
        e_score: Effektivitäts-Score (Qualität)
        s_score: Geschwindigkeits-Score (Performance)
        b_score: Baseline-Score (Verbesserung)
        is_synergetic: Ob Synergie erfolgreich (V_Kimi >= 0.997)
        improvement_summary: Zusammenfassung der Verbesserungen
    """

    v_kimi_score: float
    a_score: float
    e_score: float
    s_score: float
    b_score: float
    is_synergetic: bool
    improvement_summary: str

    def get_summary(self) -> str:
        """Menschenlesbare Zusammenfassung"""
        emoji = "✅" if self.is_synergetic else "⚠️"
        return (
            f"{emoji} V_Kimi: {self.v_kimi_score:.3f} | "
            f"A: {self.a_score:.2f} | E: {self.e_score:.2f} | "
            f"S: {self.s_score:.2f} | B: {self.b_score:.2f}"
        )


class KimiSynergyValidator:
    """Validator für Kimi-Gold Code Synergie

    Implementiert die V_Kimi Funktion zur Bewertung der Zusammenarbeit
    zwischen Gold Code (Claude) und Kimi.
    """

    # Gewichtungen für V_Kimi
    WEIGHTS = {
        "adherence": 0.50,  # 50% Adhärenz (3-6-9 Constraints)
        "effectiveness": 0.35,  # 35% Effektivität (Qualität)
        "speed": 0.10,  # 10% Geschwindigkeit
        "baseline": 0.05,  # 5% Baseline-Verbesserung
    }

    # Quality Standard
    QUALITY_STANDARD = 369 / 370  # ≈ 0.997297

    def __init__(self):
        """Initialisiert den Kimi Synergie Validator"""
        pass

    def validate_kimi_synergy(
        self,
        target_state: int,
        gold_baseline: SynergyMetrics,
        kimi_synergy_result: SynergyMetrics,
    ) -> SynergyResult:
        """Validiert Kimi-Synergie gegen Gold Code Baseline

        Args:
            target_state: Ziel-Token-Anzahl (369, 666, oder 999)
            gold_baseline: Gold Code Baseline-Metriken
            kimi_synergy_result: Kimi-validierte Metriken

        Returns:
            SynergyResult: Vollständige Synergie-Bewertung

        Mathematik:
            V_Kimi = 0.5·A + 0.35·E + 0.10·S + 0.05·B
        """
        # Berechne Komponenten-Scores
        a_score = self._calculate_adherence_score(target_state, kimi_synergy_result)
        e_score = self._calculate_effectiveness_score(
            gold_baseline, kimi_synergy_result
        )
        s_score = self._calculate_speed_score(gold_baseline, kimi_synergy_result)
        b_score = self._calculate_baseline_score(
            target_state, gold_baseline, kimi_synergy_result
        )

        # Berechne V_Kimi Gesamtscore
        v_kimi = (
            self.WEIGHTS["adherence"] * a_score
            + self.WEIGHTS["effectiveness"] * e_score
            + self.WEIGHTS["speed"] * s_score
            + self.WEIGHTS["baseline"] * b_score
        )

        # Prüfe ob synergistisch
        is_synergetic = v_kimi >= self.QUALITY_STANDARD

        # Generiere Zusammenfassung
        improvement_summary = self._generate_improvement_summary(
            target_state,
            gold_baseline,
            kimi_synergy_result,
            a_score,
            e_score,
            s_score,
            b_score,
        )

        return SynergyResult(
            v_kimi_score=v_kimi,
            a_score=a_score,
            e_score=e_score,
            s_score=s_score,
            b_score=b_score,
            is_synergetic=is_synergetic,
            improvement_summary=improvement_summary,
        )

    def _calculate_adherence_score(
        self, target_state: int, result: SynergyMetrics
    ) -> float:
        """Berechnet Adhärenz-Score A

        Misst wie nah das Ergebnis am 3-6-9 Constraint (L_i) liegt.

        Args:
            target_state: Ziel-Token-Anzahl (369, 666, 999)
            result: Kimi-Ergebnis-Metriken

        Returns:
            float: Adhärenz-Score (0.0-2.0, verstärkt da 50% Gewichtung)

        Mathematik:
            A = 2.0 × (1 - |T_syn - L_i| / L_i)
        """
        L_i = target_state
        T_syn = result.tokens

        # Relative Abweichung
        relative_deviation = abs(T_syn - L_i) / L_i

        # Adhärenz-Score (verstärkt mit Faktor 2.0)
        a_score = 2.0 * (1.0 - relative_deviation)

        # Clamp auf [0.0, 2.0]
        return max(0.0, min(a_score, 2.0))

    def _calculate_effectiveness_score(
        self, gold: SynergyMetrics, kimi: SynergyMetrics
    ) -> float:
        """Berechnet Effektivitäts-Score E

        Misst Qualitätsverbesserung durch Kimi-Validierung.

        Args:
            gold: Gold Code Baseline
            kimi: Kimi-Ergebnis

        Returns:
            float: Effektivitäts-Score (0.0-2.0)

        Mathematik:
            E = Q_syn × (1 + (Q_syn - Q_gold))
        """
        Q_gold = gold.logic_score
        Q_syn = kimi.logic_score

        # Effektivitäts-Score: Qualität verstärkt durch Verbesserung
        e_score = Q_syn * (1.0 + (Q_syn - Q_gold))

        # Clamp auf [0.0, 2.0]
        return max(0.0, min(e_score, 2.0))

    def _calculate_speed_score(
        self, gold: SynergyMetrics, kimi: SynergyMetrics
    ) -> float:
        """Berechnet Geschwindigkeits-Score S

        Misst Performance-Verhältnis (Gold vs Kimi).

        Args:
            gold: Gold Code Baseline
            kimi: Kimi-Ergebnis

        Returns:
            float: Geschwindigkeits-Score (0.0-1.0)

        Mathematik:
            S = min(1.0, log10(t_gold / t_syn + 1) / log10(2))
        """
        t_gold = gold.time_ms
        t_syn = kimi.time_ms

        # Vermeide Division durch Null
        if t_syn <= 0:
            t_syn = 0.1

        # Geschwindigkeits-Score (logarithmisch gedämpft)
        ratio = t_gold / t_syn + 1
        s_score = math.log10(ratio) / math.log10(2)

        # Clamp auf [0.0, 1.0]
        return max(0.0, min(s_score, 1.0))

    def _calculate_baseline_score(
        self, target_state: int, gold: SynergyMetrics, kimi: SynergyMetrics
    ) -> float:
        """Berechnet Baseline-Score B

        Prüft ob Kimi das Gesamtergebnis verbessert hat.

        Args:
            target_state: Ziel-Token-Anzahl
            gold: Gold Code Baseline
            kimi: Kimi-Ergebnis

        Returns:
            float: Baseline-Score (0.5 oder 1.0)

        Mathematik:
            B = 1.0 wenn (ε_syn < ε_gold UND Q_syn >= Q_gold)
            B = 0.5 sonst
        """
        epsilon_gold = abs(gold.tokens - target_state)
        epsilon_syn = abs(kimi.tokens - target_state)

        Q_gold = gold.logic_score
        Q_syn = kimi.logic_score

        # Prüfe ob Verbesserung vorliegt
        improved = (epsilon_syn < epsilon_gold) and (Q_syn >= Q_gold)

        return 1.0 if improved else 0.5

    def _generate_improvement_summary(
        self,
        target_state: int,
        gold: SynergyMetrics,
        kimi: SynergyMetrics,
        a_score: float,
        e_score: float,
        s_score: float,
        b_score: float,
    ) -> str:
        """Generiert Zusammenfassung der Verbesserungen

        Args:
            target_state: Ziel-Token-Anzahl
            gold: Gold Code Baseline
            kimi: Kimi-Ergebnis
            a_score: Adhärenz-Score
            e_score: Effektivitäts-Score
            s_score: Geschwindigkeits-Score
            b_score: Baseline-Score

        Returns:
            str: Zusammenfassung
        """
        improvements = []

        # Token-Adhärenz
        token_improvement = abs(gold.tokens - target_state) - abs(
            kimi.tokens - target_state
        )
        if token_improvement > 0:
            improvements.append(
                f"Token-Adhärenz: +{token_improvement:.0f} Tokens näher an {target_state}"
            )

        # Qualität
        quality_improvement = kimi.logic_score - gold.logic_score
        if quality_improvement > 0:
            improvements.append(f"Qualität: +{quality_improvement:.1%}")

        # Geschwindigkeit
        time_improvement = ((gold.time_ms - kimi.time_ms) / gold.time_ms) * 100
        if time_improvement > 0:
            improvements.append(f"Geschwindigkeit: +{time_improvement:.1f}% schneller")

        # Gesamtbewertung
        if b_score == 1.0:
            improvements.append("✅ Gesamtverbesserung erreicht")

        if not improvements:
            return "Keine signifikanten Verbesserungen"

        return " | ".join(improvements)

    def calculate_batch_synergy(
        self,
        target_state: int,
        gold_batch: List[SynergyMetrics],
        kimi_batch: List[SynergyMetrics],
    ) -> Dict:
        """Berechnet Synergie für einen Batch von Ergebnissen

        Args:
            target_state: Ziel-Token-Anzahl
            gold_batch: Liste von Gold Code Metriken
            kimi_batch: Liste von Kimi-Metriken

        Returns:
            Dict: Aggregierte Synergie-Metriken
        """
        if len(gold_batch) != len(kimi_batch):
            raise ValueError("gold_batch und kimi_batch müssen gleiche Länge haben")

        results = []
        for gold, kimi in zip(gold_batch, kimi_batch):
            result = self.validate_kimi_synergy(target_state, gold, kimi)
            results.append(result)

        # Aggregierte Metriken
        avg_v_kimi = np.mean([r.v_kimi_score for r in results])
        avg_a = np.mean([r.a_score for r in results])
        avg_e = np.mean([r.e_score for r in results])
        avg_s = np.mean([r.s_score for r in results])
        avg_b = np.mean([r.b_score for r in results])

        synergetic_count = sum(1 for r in results if r.is_synergetic)
        synergy_rate = synergetic_count / len(results)

        return {
            "total_samples": len(results),
            "avg_v_kimi_score": avg_v_kimi,
            "avg_adherence": avg_a,
            "avg_effectiveness": avg_e,
            "avg_speed": avg_s,
            "avg_baseline": avg_b,
            "synergy_rate": synergy_rate,
            "meets_quality_standard": avg_v_kimi >= self.QUALITY_STANDARD,
            "individual_results": results,
        }


# === EXPORT ===

__all__ = [
    "KimiSynergyValidator",
    "SynergyMetrics",
    "SynergyResult",
]
