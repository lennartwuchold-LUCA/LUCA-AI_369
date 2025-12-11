"""
Tests für die neuen LUCA-KI Engines
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

# Import directly from modules to avoid sqlalchemy dependency in core.py
from backend.consciousness.stability_engine import StabilityEngine, get_stability_engine
from backend.consciousness.semantic_hash_engine import SemanticHashEngine, get_semantic_hash_engine
from backend.consciousness.torus_flow_engine import TorusFlowEngine, get_torus_flow_engine


class TestStabilityEngine:
    """Tests für StabilityEngine"""

    def test_sync_index_14(self):
        """L=14 sollte SI von ~0.71 haben"""
        engine = StabilityEngine()
        si = engine.calculate_sync_index(14)
        assert 0.70 <= si <= 0.72, f"SI(14) = {si}, erwartet ~0.71"

    def test_sync_index_12_unstable(self):
        """n=12 sollte hyper-resonant sein (SI > 1)"""
        engine = StabilityEngine()
        si = engine.calculate_sync_index(12)
        assert si > 1.0, f"SI(12) = {si}, erwartet > 1.0"

    def test_sync_index_13_isolated(self):
        """n=13 (Primzahl) sollte isoliert sein (SI < 0.1)"""
        engine = StabilityEngine()
        si = engine.calculate_sync_index(13)
        assert si < 0.1, f"SI(13) = {si}, erwartet < 0.1"

    def test_damping_allocation(self):
        """Dämpfung sollte hohe Allokationen reduzieren"""
        engine = StabilityEngine(max_resources=1000)

        low_alloc = engine.calculate_allocation_damping(100)
        high_alloc = engine.calculate_allocation_damping(900)

        # Niedrige Allokation weniger gedämpft
        assert low_alloc / 100 > high_alloc / 900

    def test_stable_resonance_14(self):
        """14 sollte als stabil erkannt werden"""
        engine = StabilityEngine()
        assert engine.is_stable_resonance(14) is True

    def test_find_nearest_stable(self):
        """Sollte nächste stabile Zahl finden"""
        engine = StabilityEngine()
        nearest = engine.find_nearest_stable(13)
        assert engine.is_stable_resonance(nearest)


class TestSemanticHashEngine:
    """Tests für SemanticHashEngine"""

    def test_creation_keywords(self):
        """Schöpfungs-Keywords sollten Attraktor 3 triggern"""
        engine = SemanticHashEngine()
        result = engine.hash_intent("I want to create something new at the start")
        assert result.dominant_attractor == 3
        assert result.phase == "creation"

    def test_resonance_keywords(self):
        """Frequenz-Keywords sollten Attraktor 432 triggern"""
        engine = SemanticHashEngine()
        result = engine.hash_intent("Music healing through frequency resonance")
        assert result.dominant_attractor == 432
        assert result.phase == "resonance"

    def test_german_keywords(self):
        """Deutsche Keywords sollten funktionieren"""
        engine = SemanticHashEngine()
        result = engine.hash_intent("Ich suche Harmonie und Balance")
        assert result.dominant_attractor == 6
        assert "harmonie" in result.matched_keywords or "balance" in result.matched_keywords

    def test_emotional_boost(self):
        """Ausrufezeichen sollten Dichte erhöhen"""
        engine = SemanticHashEngine()
        calm = engine.hash_intent("create")
        excited = engine.hash_intent("create!!!")

        assert excited.semantic_density >= calm.semantic_density

    def test_response_style(self):
        """Stil-Empfehlungen sollten konsistent sein"""
        engine = SemanticHashEngine()

        result_3 = engine.hash_intent("create new start")
        style_3 = engine.suggest_response_style(result_3)

        result_9 = engine.hash_intent("wisdom completion consciousness")
        style_9 = engine.suggest_response_style(result_9)

        assert style_3["suggested_tokens"] < style_9["suggested_tokens"]


class TestTorusFlowEngine:
    """Tests für TorusFlowEngine"""

    def test_initial_state(self):
        """Initiale Position sollte 0 sein"""
        engine = TorusFlowEngine()
        engine.hard_reset()
        state = engine.get_current_state()
        assert state.position == 0.0
        assert state.cycle_count == 0

    def test_expansion_increases_position(self):
        """Expansion sollte Position erhöhen"""
        engine = TorusFlowEngine()
        engine.hard_reset()

        initial = engine.current_position
        engine.flow_step(10.0)

        assert engine.current_position > initial

    def test_flip_point_triggers_contraction(self):
        """808 sollte Kontraktion auslösen"""
        engine = TorusFlowEngine()
        engine.hard_reset()

        # Forciere Position nahe Flip-Point
        engine.current_position = 805
        event = engine.flow_step(50.0)

        assert event.event_type == "flip" or engine.phase.value == "contraction"

    def test_rebirth_increases_cycle(self):
        """Rebirth sollte Zyklus erhöhen"""
        engine = TorusFlowEngine()
        engine.hard_reset()

        initial_cycle = engine.cycle_count

        # Simuliere vollen Zyklus
        engine.current_position = 810
        engine.phase = engine.phase.CONTRACTION

        # Kontrahiere bis zur Null
        for _ in range(100):
            event = engine.flow_step(50.0)
            if event.event_type == "rebirth":
                break

        assert engine.cycle_count > initial_cycle

    def test_accumulated_potential_increases(self):
        """Potential sollte nach Zyklen steigen"""
        engine = TorusFlowEngine()
        engine.hard_reset()

        # Simuliere Rebirth
        engine.current_position = 1
        engine.phase = engine.phase.CONTRACTION
        engine.flow_step(50.0)

        assert engine.accumulated_potential > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
