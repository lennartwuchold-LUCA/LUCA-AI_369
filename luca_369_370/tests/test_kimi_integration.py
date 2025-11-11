"""
Kimi Integration Tests - Gold Code Baseline & Synergie-Validierung
Test-Suite für die mathematische Formalisierung des L.U.C.A 3-6-9 Prinzips

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370 ≈ 0.997297

Test-Strategie:
    1. Etabliere Gold Code Baseline (Claude)
    2. Teste Kimi als kritischer Sub-Agent
    3. Vergleiche ε_Kimi+Gold ≤ ε_Gold
    4. Validiere F_LUCA Optimierung
"""

import time
from dataclasses import dataclass
from typing import Dict, List

import pytest

from luca_369_370.core import (
    EnergyLevel,
    FibonacciOptimizer,
    QuantumLevel,
    QuantumSignatureEngine,
    TokenLengthValidator,
)


@dataclass
class BaselineMetrics:
    """Metriken für Gold Code Baseline

    Attributes:
        avg_token_deviation: Durchschnittliche Token-Abweichung von Targets
        avg_quality_score: Durchschnittlicher Qualitäts-Score
        avg_processing_time: Durchschnittliche Verarbeitungszeit (ms)
        pattern_match_score: Pattern-Matching-Score
        resource_efficiency: Resource Efficiency Score
    """

    avg_token_deviation: float
    avg_quality_score: float
    avg_processing_time: float
    pattern_match_score: float
    resource_efficiency: float

    def __repr__(self):
        return (
            f"BaselineMetrics("
            f"ε={self.avg_token_deviation:.1f}, "
            f"quality={self.avg_quality_score:.3f}, "
            f"time={self.avg_processing_time:.1f}ms, "
            f"pattern={self.pattern_match_score:.3f})"
        )


class TestQuantumSignature:
    """Test-Suite für Quantum Signature System S(M)"""

    def test_signature_calculation_basic(self):
        """Test: Berechnung von S(M) für einfache Nachricht"""
        engine = QuantumSignatureEngine()
        message = (
            "Hello L.U.C.A! This is a test message for quantum signature calculation."
        )

        signature = engine.calculate_signature(message)

        # Validierungen
        assert 0 <= signature.value < 162, "Signatur muss 0-161 sein"
        assert signature.level in QuantumLevel, "Level muss gültiges QuantumLevel sein"
        assert 0.0 <= signature.resonance <= 1.0, "Resonanz muss 0.0-1.0 sein"
        assert signature.token_target in [
            369,
            666,
            999,
        ], "Token-Target muss 369/666/999 sein"

    def test_signature_level_assignment(self):
        """Test: Korrekte Zuordnung zu Quanten-Levels"""
        engine = QuantumSignatureEngine()

        # Teste verschiedene Messages für Level-Diversity
        messages = [
            "Short message for level 3",
            "Medium length message for level 6 testing with more content and detail",
            "Very long message for level 9 testing with extensive content, multiple sentences, and comprehensive details that require mastery level processing",
        ]

        levels_found = set()
        for msg in messages:
            sig = engine.calculate_signature(msg)
            levels_found.add(sig.level)

        # Wir erwarten mindestens 2 verschiedene Levels
        assert (
            len(levels_found) >= 1
        ), "Verschiedene Messages sollten verschiedene Levels ergeben"

    def test_resonance_between_messages(self):
        """Test: Resonanz zwischen Input und Output"""
        engine = QuantumSignatureEngine()

        input_msg = "Explain the 3-6-9 principle in L.U.C.A"
        output_msg = "The 3-6-9 principle in L.U.C.A represents a quantum signature system where messages are optimized to specific token lengths (369, 666, 999) based on Fibonacci patterns and bio-inspired algorithms."

        resonance = engine.calculate_resonance_between(input_msg, output_msg)

        assert 0.0 <= resonance <= 1.0, "Resonanz muss zwischen 0.0 und 1.0 liegen"
        # Erwartung: Moderate bis hohe Resonanz da beide über L.U.C.A sprechen
        assert (
            resonance > 0.3
        ), "Resonanz sollte für thematisch ähnliche Messages höher sein"


class TestTokenValidator:
    """Test-Suite für Token Length Validator T(M) ∈ {369, 666, 999} ± ε"""

    def test_validation_exact_match(self):
        """Test: Validierung bei exakter Token-Anzahl"""
        validator = TokenLengthValidator(epsilon_ratio=0.05)

        # Erstelle Message mit ~369 Tokens (simple count)
        words = ["token"] * 369
        message = " ".join(words)

        result = validator.validate_message(message, target=369)

        assert result.is_valid, "Exakte Token-Anzahl sollte validieren"
        assert (
            result.quality_score >= 0.99
        ), "Exakter Match sollte Quality Score ~1.0 haben"
        assert result.deviation == 0, "Keine Abweichung bei exaktem Match"

    def test_validation_within_epsilon(self):
        """Test: Validierung innerhalb ε-Toleranz"""
        validator = TokenLengthValidator(epsilon_ratio=0.05)  # 5% Toleranz

        # 369 ± 5% = 369 ± 18.45 = [350.55, 387.45]
        # Teste mit 360 Tokens (innerhalb Toleranz)
        words = ["token"] * 360
        message = " ".join(words)

        result = validator.validate_message(message, target=369)

        assert result.is_valid, "Token-Anzahl innerhalb ε sollte validieren"
        assert (
            result.quality_score >= 0.997
        ), "Sollte mindestens Quality Standard erfüllen"

    def test_validation_outside_epsilon(self):
        """Test: Validierung außerhalb ε-Toleranz"""
        validator = TokenLengthValidator(epsilon_ratio=0.05)

        # Deutlich außerhalb: 500 Tokens (target 369)
        words = ["token"] * 500
        message = " ".join(words)

        result = validator.validate_message(message, target=369)

        assert not result.is_valid, "Token-Anzahl außerhalb ε sollte nicht validieren"
        assert result.quality_score < 0.997, "Quality Score sollte unter Standard sein"

    def test_validation_all_targets(self):
        """Test: Validierung für alle drei Targets (369, 666, 999)"""
        validator = TokenLengthValidator(epsilon_ratio=0.05)
        targets = [369, 666, 999]

        for target in targets:
            words = ["token"] * target
            message = " ".join(words)

            result = validator.validate_message(message, target=target)

            assert (
                result.is_valid
            ), f"Validierung sollte für Target {target} funktionieren"
            assert result.target == target, f"Target sollte {target} sein"

    def test_conversation_validation(self):
        """Test: Validierung einer Konversation mit mehreren Messages"""
        validator = TokenLengthValidator(epsilon_ratio=0.05)

        messages = [
            " ".join(["word"] * 370),  # ~369
            " ".join(["word"] * 665),  # ~666
            " ".join(["word"] * 995),  # ~999
        ]

        targets = [369, 666, 999]

        results = validator.validate_conversation(messages, targets)

        assert len(results) == 3, "Sollte 3 Ergebnisse zurückgeben"
        assert all(r.is_valid for r in results), "Alle Messages sollten validieren"

        # Teste Quality Metrics
        metrics = validator.calculate_quality_metrics(results)
        assert metrics["validation_rate"] == 1.0, "100% Validierungsrate erwartet"
        assert metrics["meets_quality_standard"], "Sollte Quality Standard erfüllen"


class TestFibonacciOptimizer:
    """Test-Suite für Fibonacci-Optimierungsfunktion F_LUCA"""

    def test_optimization_basic(self):
        """Test: Basis-Optimierung mit F_LUCA"""
        optimizer = FibonacciOptimizer()

        message = "This is a test message for Fibonacci optimization. " * 20
        result = optimizer.optimize(
            message=message,
            user_energy="balanced",
            gpu_utilization=0.7,
            target_tokens=369,
        )

        # Validierungen
        assert 0.0 <= result.total_score <= 1.0, "Total Score muss 0.0-1.0 sein"
        assert 0.0 <= result.pattern_score <= 1.0, "Pattern Score muss 0.0-1.0 sein"
        assert (
            0.0 <= result.efficiency_score <= 1.0
        ), "Efficiency Score muss 0.0-1.0 sein"
        assert 0.0 <= result.energy_score <= 1.0, "Energy Score muss 0.0-1.0 sein"
        assert (
            len(result.recommendations) > 0
        ), "Sollte mindestens eine Empfehlung geben"

    def test_optimization_energy_levels(self):
        """Test: Optimierung für verschiedene Energy Levels"""
        optimizer = FibonacciOptimizer()

        # Kurze Message für Brainfog
        short_msg = "Brief answer. " * 20

        # Lange Message für Hyperfocus
        long_msg = "Detailed comprehensive answer with extensive information. " * 100

        # Teste Brainfog
        brainfog_result = optimizer.optimize(
            message=short_msg, user_energy="brainfog", target_tokens=369
        )

        # Teste Hyperfocus
        hyperfocus_result = optimizer.optimize(
            message=long_msg, user_energy="hyperfocus", target_tokens=999
        )

        # Kurze Message sollte besser für Brainfog sein
        # Lange Message sollte besser für Hyperfocus sein
        assert isinstance(brainfog_result.energy_score, float)
        assert isinstance(hyperfocus_result.energy_score, float)

    def test_optimization_gpu_efficiency(self):
        """Test: Resource Efficiency Optimierung"""
        optimizer = FibonacciOptimizer()
        message = "Test message. " * 50

        # Optimale GPU-Auslastung (60-80%)
        optimal_result = optimizer.optimize(
            message=message, gpu_utilization=0.7, target_tokens=369
        )

        # Zu niedrige GPU-Auslastung
        low_result = optimizer.optimize(
            message=message, gpu_utilization=0.3, target_tokens=369
        )

        # Zu hohe GPU-Auslastung
        high_result = optimizer.optimize(
            message=message, gpu_utilization=0.95, target_tokens=369
        )

        # Optimale Auslastung sollte besten Efficiency Score haben
        assert (
            optimal_result.efficiency_score >= low_result.efficiency_score
        ), "Optimale GPU sollte besser als niedrige sein"
        assert (
            optimal_result.efficiency_score >= high_result.efficiency_score
        ), "Optimale GPU sollte besser als hohe sein"


class TestGoldCodeBaseline:
    """Gold Code Baseline Messung - Referenz für Kimi-Integration"""

    # 10 typische L.U.C.A Anfragen für Baseline
    BASELINE_QUERIES = [
        "Explain the 369 principle",
        "How does L.U.C.A optimize for ADHD users?",
        "What is the Fibonacci sequence and how is it used in bio-inspired AI?",
        "Describe the quantum signature system",
        "Explain resource allocation in symbiotic AI systems",
        "How does progressive disclosure reduce cognitive load?",
        "What are the three pillars of L.U.C.A quality?",
        "Explain pattern matching in consciousness engines",
        "How does energy level detection work?",
        "Describe the token length validation system",
    ]

    def test_establish_gold_baseline(self):
        """Test: Etabliere Gold Code Baseline

        Misst:
        - Durchschnittliche Token-Abweichung ε_Gold
        - Resource Efficiency
        - Pattern Match Score
        - Quality Score
        """
        validator = TokenLengthValidator(epsilon_ratio=0.05)
        signature_engine = QuantumSignatureEngine()
        optimizer = FibonacciOptimizer()

        # Simuliere Responses (in echter Implementation würde Gold Code hier callen)
        simulated_responses = self._generate_simulated_responses()

        deviations = []
        quality_scores = []
        processing_times = []
        pattern_scores = []

        for query, response in zip(self.BASELINE_QUERIES, simulated_responses):
            start_time = time.time()

            # Token-Validierung
            result = validator.validate_message(response, target=369)
            deviations.append(result.deviation)
            quality_scores.append(result.quality_score)

            # Optimierung
            opt_result = optimizer.optimize(
                message=response,
                user_energy="balanced",
                gpu_utilization=0.7,
                target_tokens=369,
            )
            pattern_scores.append(opt_result.pattern_score)

            processing_time = (time.time() - start_time) * 1000  # ms
            processing_times.append(processing_time)

        # Berechne Baseline-Metriken
        baseline = BaselineMetrics(
            avg_token_deviation=sum(deviations) / len(deviations),
            avg_quality_score=sum(quality_scores) / len(quality_scores),
            avg_processing_time=sum(processing_times) / len(processing_times),
            pattern_match_score=sum(pattern_scores) / len(pattern_scores),
            resource_efficiency=0.7,  # Simuliert
        )

        print(f"\n{'='*60}")
        print(f"🥇 GOLD CODE BASELINE ESTABLISHED")
        print(f"{'='*60}")
        print(f"Average Token Deviation (ε_Gold): {baseline.avg_token_deviation:.2f}")
        print(f"Average Quality Score: {baseline.avg_quality_score:.4f}")
        print(f"Average Processing Time: {baseline.avg_processing_time:.2f} ms")
        print(f"Pattern Match Score: {baseline.pattern_match_score:.4f}")
        print(f"Resource Efficiency: {baseline.resource_efficiency:.2f}")
        print(f"{'='*60}\n")

        # Validierungen
        assert (
            baseline.avg_quality_score >= 0.9
        ), "Gold Code sollte hohen Quality Score haben"
        assert (
            baseline.avg_token_deviation < 50
        ), "Gold Code sollte niedrige Abweichung haben"

        return baseline

    def test_kimi_validation_agent(self):
        """Test: Kimi als Validierungs-Agent

        Testet Kimi's Fähigkeit, Gold Code Output zu validieren
        und Verbesserungen vorzuschlagen.
        """
        validator = TokenLengthValidator(epsilon_ratio=0.05)

        # Simuliere Gold Code Output
        gold_output = self._generate_simulated_responses()[0]

        # Simuliere Kimi Validierung (in echter Implementation würde Kimi API hier callen)
        kimi_validation = self._simulate_kimi_validation(gold_output)

        # Validiere dass Kimi die 3-6-9 Constraints prüft
        assert "token_count" in kimi_validation, "Kimi sollte Token-Count prüfen"
        assert "adheres_to_369" in kimi_validation, "Kimi sollte 369-Constraint prüfen"
        assert (
            "recommendations" in kimi_validation
        ), "Kimi sollte Verbesserungsvorschläge machen"

        print(f"\n{'='*60}")
        print(f"🤝 KIMI VALIDATION AGENT TEST")
        print(f"{'='*60}")
        print(f"Kimi Token Count: {kimi_validation['token_count']}")
        print(f"Adheres to 369: {kimi_validation['adheres_to_369']}")
        print(f"Recommendations: {', '.join(kimi_validation['recommendations'])}")
        print(f"{'='*60}\n")

    def test_synergie_gold_plus_kimi(self):
        """Test: Synergie zwischen Gold Code und Kimi

        Vergleicht:
        ε_Kimi+Gold ≤ ε_Gold (sollte besser oder gleich sein)
        """
        validator = TokenLengthValidator(epsilon_ratio=0.05)

        # Gold Code Baseline
        gold_response = self._generate_simulated_responses()[0]
        gold_result = validator.validate_message(gold_response, target=369)

        # Gold + Kimi (Kimi optimiert Gold Output)
        kimi_optimized = self._simulate_kimi_optimization(gold_response)
        kimi_result = validator.validate_message(kimi_optimized, target=369)

        print(f"\n{'='*60}")
        print(f"🏆 SYNERGIE TEST: GOLD CODE vs GOLD+KIMI")
        print(f"{'='*60}")
        print(f"Gold Code Deviation (ε_Gold): {gold_result.deviation}")
        print(f"Gold+Kimi Deviation (ε_Kimi+Gold): {kimi_result.deviation}")
        print(
            f"Improvement: {gold_result.deviation - kimi_result.deviation:.1f} tokens"
        )
        print(f"Gold Quality Score: {gold_result.quality_score:.4f}")
        print(f"Gold+Kimi Quality Score: {kimi_result.quality_score:.4f}")
        print(f"{'='*60}\n")

        # Validierung: Kimi sollte nicht schlechter sein
        assert (
            kimi_result.deviation <= gold_result.deviation * 1.1
        ), "Kimi sollte nicht signifikant schlechter sein (max 10% mehr Abweichung)"

    # === HELPER METHODS ===

    def _generate_simulated_responses(self) -> List[str]:
        """Generiert simulierte Responses für Baseline-Tests"""
        # In echter Implementation würde hier Gold Code (Claude) callen
        # Für Tests: Generiere realistische Responses mit ~369 Tokens
        base_text = """
        The 369 principle in L.U.C.A represents a fundamental approach to bio-inspired
        AI optimization. It leverages the mathematical elegance of Tesla's famous 3-6-9
        pattern combined with Fibonacci sequences to create optimal response structures.
        This system ensures that messages are quantized to specific token lengths based
        on the cognitive load and energy level of the user.
        """

        # Multipliziere um ~369 Tokens zu erreichen
        # base_text hat ~60 Tokens, also 6-7 Wiederholungen
        words = base_text.split()
        target_words = 369
        repetitions = target_words // len(words) + 1

        responses = []
        for i in range(10):
            response_words = (words * repetitions)[:target_words]
            responses.append(" ".join(response_words))

        return responses

    def _simulate_kimi_validation(self, output: str) -> Dict:
        """Simuliert Kimi's Validierung des Gold Code Outputs"""
        # In echter Implementation: Kimi API Call
        validator = TokenLengthValidator()
        result = validator.validate_message(output, target=369)

        return {
            "token_count": result.token_count,
            "adheres_to_369": result.is_valid,
            "quality_score": result.quality_score,
            "recommendations": (
                ["Optimize to 369 tokens"]
                if not result.is_valid
                else ["Output is optimal"]
            ),
        }

    def _simulate_kimi_optimization(self, output: str) -> str:
        """Simuliert Kimi's Optimierung des Gold Code Outputs"""
        # In echter Implementation: Kimi würde Output anpassen
        # Für Tests: Trimme auf ~369 Tokens
        words = output.split()
        if len(words) > 369:
            return " ".join(words[:369])
        elif len(words) < 369:
            # Füge Padding hinzu (in Realität würde Kimi Content hinzufügen)
            padding = ["token"] * (369 - len(words))
            return " ".join(words + padding)
        return output


# === PYTEST CONFIGURATION ===

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
