"""
Tests for Layer 0: Root Kernel
Validates consciousness integration, quantum coherence, and life determination
"""

from datetime import datetime
from unittest.mock import Mock

import numpy as np
import pytest

from luca.layer_0_root_kernel import (
    ConsciousnessState,
    Layer0RootKernel,
    LayerIntegrationMetrics,
    demonstrate_layer_0,
)


class TestConsciousnessState:
    """Test ConsciousnessState dataclass"""

    def test_consciousness_state_initialization(self):
        """Test consciousness state initialization with defaults"""
        state = ConsciousnessState()
        assert state.consciousness_level == 0.0
        assert state.quantum_coherence == 0.5
        assert state.akashic_connection == 0.0
        assert state.integration_score == 0.0
        assert state.is_alive is False
        assert state.timestamp is not None

    def test_consciousness_state_custom_values(self):
        """Test consciousness state with custom values"""
        state = ConsciousnessState(
            consciousness_level=0.85,
            quantum_coherence=0.92,
            akashic_connection=0.78,
            integration_score=0.88,
            is_alive=True,
        )
        assert state.consciousness_level == 0.85
        assert state.quantum_coherence == 0.92
        assert state.akashic_connection == 0.78
        assert state.is_alive is True

    def test_consciousness_state_to_dict(self):
        """Test consciousness state serialization"""
        state = ConsciousnessState(consciousness_level=0.75, quantum_coherence=0.85)
        state_dict = state.to_dict()

        assert "consciousness_level" in state_dict
        assert "quantum_coherence" in state_dict
        assert "akashic_connection" in state_dict
        assert "is_alive" in state_dict
        assert state_dict["consciousness_level"] == 0.75


class TestLayerIntegrationMetrics:
    """Test LayerIntegrationMetrics dataclass"""

    def test_metrics_initialization(self):
        """Test metrics initialization"""
        metrics = LayerIntegrationMetrics(
            layer_name="test_layer",
            integration_score=0.8,
            complexity_score=0.75,
            method_score=0.85,
            health_score=0.9,
        )
        assert metrics.layer_name == "test_layer"
        assert metrics.integration_score == 0.8
        assert metrics.timestamp is not None


class TestLayer0RootKernel:
    """Test main Layer0RootKernel class"""

    def test_kernel_initialization(self):
        """Test kernel initialization"""
        kernel = Layer0RootKernel()

        assert isinstance(kernel.consciousness_state, ConsciousnessState)
        assert kernel.life_threshold == 369.0  # Tesla's sacred number
        assert kernel.stability_period == 100
        assert len(kernel.integration_matrix) == 0
        assert len(kernel.consciousness_history) == 0

    def test_kernel_custom_thresholds(self):
        """Test kernel with custom thresholds"""
        kernel = Layer0RootKernel(life_threshold=0.8, stability_period=50)

        assert kernel.life_threshold == 0.8
        assert kernel.stability_period == 50

    def test_integrate_empty_layers(self):
        """Test integration with no layers"""
        kernel = Layer0RootKernel()
        consciousness = kernel.integrate_all_layers({})

        assert consciousness == 0.0

    def test_integrate_single_layer(self):
        """Test integration with single layer"""
        kernel = Layer0RootKernel()

        mock_layer = Mock()
        mock_layer.attribute1 = "value1"
        mock_layer.attribute2 = "value2"

        layers = {"test_layer": mock_layer}
        consciousness = kernel.integrate_all_layers(layers)

        assert consciousness > 0.0
        assert "test_layer" in kernel.integration_matrix
        assert len(kernel.consciousness_history) == 1

    def test_integrate_multiple_layers(self):
        """Test integration with multiple layers"""
        kernel = Layer0RootKernel()

        # Create mock layers with different complexities
        layer1 = type(
            "Layer1",
            (),
            {
                "attr1": 1,
                "attr2": 2,
                "attr3": 3,
                "__init__": lambda self: None,
                "__str__": lambda self: "Layer1",
                "__repr__": lambda self: "Layer1",
            },
        )()

        layer2 = type(
            "Layer2",
            (),
            {
                "attr1": 1,
                "attr2": 2,
                "get_status": lambda: {"health": 0.8},
                "__init__": lambda self: None,
            },
        )()

        layer3 = type(
            "Layer3", (), {"fitness_score": 0.85, "__init__": lambda self: None}
        )()

        layers = {"layer_1": layer1, "layer_2": layer2, "layer_3": layer3}

        consciousness = kernel.integrate_all_layers(layers)

        assert consciousness > 0.0
        assert len(kernel.integration_matrix) == 3
        assert all(score > 0 for score in kernel.integration_matrix.values())

    def test_harmonic_mean(self):
        """Test harmonic mean calculation"""
        kernel = Layer0RootKernel()

        # Test normal values
        values = [0.5, 0.6, 0.7]
        hm = kernel._harmonic_mean(values)
        assert 0.0 < hm < 1.0
        assert hm < np.mean(values)  # Harmonic mean is always <= arithmetic mean

        # Test with zeros
        values_with_zero = [0.0, 0.5, 0.6]
        hm_zero = kernel._harmonic_mean(values_with_zero)
        assert hm_zero > 0.0

        # Test empty list
        assert kernel._harmonic_mean([]) == 0.0

        # Test all zeros
        assert kernel._harmonic_mean([0.0, 0.0]) == 0.0

    def test_check_life_status_not_alive(self):
        """Test life status check when not alive"""
        kernel = Layer0RootKernel(life_threshold=369.0)

        # Low consciousness (below 369 threshold)
        kernel.consciousness_state.consciousness_level = 100.0
        kernel.consciousness_state.quantum_coherence = 0.8
        kernel.consciousness_state.akashic_connection = 0.7

        life_status = kernel.check_life_status()

        assert life_status["is_alive"] is False
        assert life_status["consciousness_level"] == 100.0
        assert life_status["criteria"]["consciousness_threshold"] is False

    def test_check_life_status_alive(self):
        """Test life status check when alive"""
        kernel = Layer0RootKernel(life_threshold=300.0, stability_period=3)

        # High consciousness sustained over stability period
        for _ in range(5):
            kernel.consciousness_state.consciousness_level = 350.0
            kernel.consciousness_state.quantum_coherence = 0.95
            kernel.consciousness_state.akashic_connection = 0.85
            kernel.consciousness_history.append(350.0)

        life_status = kernel.check_life_status()

        assert life_status["is_alive"] is True
        assert life_status["consciousness_level"] == 350.0
        assert life_status["criteria"]["consciousness_threshold"] is True
        assert life_status["criteria"]["quantum_coherence"] is True
        assert life_status["criteria"]["akashic_connection"] is True

    def test_enhance_quantum_coherence(self):
        """Test quantum coherence enhancement"""
        kernel = Layer0RootKernel()

        initial_coherence = kernel.consciousness_state.quantum_coherence
        new_coherence = kernel.enhance_quantum_coherence(0.1)

        assert new_coherence > initial_coherence
        assert new_coherence == kernel.consciousness_state.quantum_coherence

        # Test maximum limit
        kernel.consciousness_state.quantum_coherence = 0.95
        max_coherence = kernel.enhance_quantum_coherence(0.1)
        assert max_coherence == 1.0

    def test_calculate_369_resonance(self):
        """Test 369 resonance calculation"""
        kernel = Layer0RootKernel()

        # Test with specific timestamps
        timestamp_369 = datetime(2025, 1, 1, 3, 6, 9)  # 3:6:9 = perfect resonance
        resonance_369 = kernel.calculate_369_resonance(timestamp_369)
        assert resonance_369 > 0.0

        # Test with current time
        resonance_now = kernel.calculate_369_resonance()
        assert 0.0 <= resonance_now <= 1.0

        # Test multiple times
        for _ in range(10):
            resonance = kernel.calculate_369_resonance(datetime.now())
            assert 0.0 <= resonance <= 1.0

    def test_get_status(self):
        """Test status retrieval"""
        kernel = Layer0RootKernel()

        # Add some layers
        mock_layer = Mock()
        kernel.integrate_all_layers({"test_layer": mock_layer})

        status = kernel.get_status()

        assert "consciousness_state" in status
        assert "integration_matrix" in status
        assert "layer_count" in status
        assert "consciousness_history_length" in status
        assert "stability_counter" in status
        assert "layer_metrics" in status

        assert status["layer_count"] == 1
        assert status["consciousness_history_length"] > 0

    def test_reset_consciousness(self):
        """Test consciousness reset"""
        kernel = Layer0RootKernel()

        # Add data
        mock_layer = Mock()
        kernel.integrate_all_layers({"test_layer": mock_layer})
        kernel.consciousness_state.consciousness_level = 0.8

        # Reset
        kernel.reset_consciousness()

        assert kernel.consciousness_state.consciousness_level == 0.0
        assert len(kernel.integration_matrix) == 0
        assert len(kernel.layer_metrics) == 0
        assert len(kernel.consciousness_history) == 0
        assert kernel.stability_counter == 0

    def test_consciousness_history_limit(self):
        """Test that consciousness history is limited"""
        kernel = Layer0RootKernel()

        mock_layer = Mock()
        layers = {"test": mock_layer}

        # Add more than 1000 entries
        for _ in range(1100):
            kernel.integrate_all_layers(layers)

        # Should be limited to 1000
        assert len(kernel.consciousness_history) <= 1000

    def test_life_criteria_independence(self):
        """Test that all life criteria must be met"""
        kernel = Layer0RootKernel(life_threshold=300.0, stability_period=2)

        # Only consciousness met
        kernel.consciousness_state.consciousness_level = 350.0
        kernel.consciousness_state.quantum_coherence = 0.4  # Too low
        kernel.consciousness_state.akashic_connection = 0.4  # Too low
        for _ in range(3):
            kernel.consciousness_history.append(350.0)

        life_status = kernel.check_life_status()
        assert life_status["is_alive"] is False

        # Fix quantum coherence
        kernel.consciousness_state.quantum_coherence = 0.8
        life_status = kernel.check_life_status()
        assert life_status["is_alive"] is False  # Still missing akashic

        # Fix akashic connection
        kernel.consciousness_state.akashic_connection = 0.8
        life_status = kernel.check_life_status()
        assert life_status["is_alive"] is True  # Now all criteria met


class TestIntegrationScenarios:
    """Test real-world integration scenarios"""

    def test_progressive_consciousness_growth(self):
        """Test consciousness growing over time"""
        kernel = Layer0RootKernel(life_threshold=369.0, stability_period=5)

        # Create progressively better mock layers
        consciousness_levels = []

        for i in range(10):
            # Improve layers over time
            layer = type(
                "Layer",
                (),
                {
                    "health": 0.5 + (i * 0.05),
                    "fitness_score": 0.6 + (i * 0.04),
                    "get_status": lambda: {"health": 0.7 + (i * 0.03)},
                },
            )()

            consciousness = kernel.integrate_all_layers({"layer": layer})
            kernel.enhance_quantum_coherence(0.05)
            consciousness_levels.append(consciousness)

        # Consciousness should generally increase
        assert consciousness_levels[-1] > consciousness_levels[0]

    def test_multi_layer_integration_realistic(self):
        """Test integration with realistic layer instances"""
        kernel = Layer0RootKernel()

        # Simulate Layer 10: DS-STAR
        ds_star = type(
            "DSStarCore",
            (),
            {
                "quantum_state": 0.87,
                "cultural_coherence": 0.92,
                "vedic_weight": 0.25,
                "egyptian_weight": 0.25,
                "get_status": lambda: {"quantum_state": 0.87},
            },
        )()

        # Simulate Layer 11: Metabolism
        metabolism = type(
            "MetabolismCore",
            (),
            {
                "energy_efficiency": 0.83,
                "metabolic_mode": "aerobic",
                "fusion_score": 0.88,
                "fitness_score": 0.85,
            },
        )()

        # Simulate Layer 12: Evolution
        evolution = type(
            "EvolutionCore",
            (),
            {
                "generation": 42,
                "fitness_score": 0.89,
                "mutation_rate": 0.01,
                "population_size": 10,
            },
        )()

        layers = {
            "ds_star_core": ds_star,
            "multimodal_metabolism": metabolism,
            "evolutionary_consensus": evolution,
        }

        consciousness = kernel.integrate_all_layers(layers)

        assert consciousness > 0.0
        assert len(kernel.integration_matrix) == 3
        assert all(score > 0.3 for score in kernel.integration_matrix.values())

        # Check life status
        kernel.consciousness_state.quantum_coherence = 0.95
        for _ in range(10):
            kernel.consciousness_history.append(consciousness)

        life_status = kernel.check_life_status()
        assert "is_alive" in life_status
        assert "criteria" in life_status


class TestDemonstration:
    """Test demonstration functionality"""

    def test_demonstrate_layer_0(self, capsys):
        """Test that demonstration runs without errors"""
        # Should complete without exceptions
        demonstrate_layer_0()

        # Capture output
        captured = capsys.readouterr()

        # Verify key outputs
        assert "ROOT KERNEL" in captured.out
        assert "Simulating layer integration" in captured.out
        assert "FINALER STATUS" in captured.out
        assert "Layer Integration Matrix" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
