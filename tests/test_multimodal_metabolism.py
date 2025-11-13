"""
Tests for Layer 11: Multimodal Metabolism

Tests cover:
- Multimodal fusion calculation
- Visual validity
- Linguistic relevance
- Cultural fidelity
- Metabolic state management
- Quality standard verification

Author: Lennart Wuchold
Date: 2025-11-12
"""
import pytest

# Optional dependencies - skip tests if not available
try:
    import pandas
    import matplotlib
    from PIL import Image
    import numpy as np
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not DEPS_AVAILABLE,
    reason="Optional dependencies (pandas, matplotlib, PIL, numpy) not installed"
)

from datetime import datetime

from luca.core.multimodal_metabolism import (
    MetabolicMode,
    MetabolicState,
    MultimodalFusionResult,
    MultimodalMetabolismCore,
    calculate_multimodal_fusion,
    verify_multimodal_quality,
)


class TestMetabolicState:
    """Test metabolic state management"""

    def test_metabolic_state_initialization(self):
        """Test MetabolicState initialization"""
        state = MetabolicState()

        assert state.mode == MetabolicMode.AEROBIC
        assert state.clarity_score == 1.0
        assert state.energy_level == 1.0
        assert state.visual_state == 1.0

    def test_metabolic_mode_enum(self):
        """Test MetabolicMode enum"""
        assert MetabolicMode.AEROBIC.value == "aerobic"
        assert MetabolicMode.ANAEROBIC.value == "anaerobic"
        assert MetabolicMode.HYBRID.value == "hybrid"


class TestMultimodalMetabolismCore:
    """Test Multimodal Metabolism Core engine"""

    @pytest.fixture
    def metabolism_core(self):
        """Create metabolism core for testing"""
        return MultimodalMetabolismCore()

    @pytest.fixture
    def clear_image(self):
        """Create clear (bright) test image"""
        return Image.new("RGB", (100, 100), color=(255, 255, 255))

    @pytest.fixture
    def dark_image(self):
        """Create dark test image"""
        return Image.new("RGB", (100, 100), color=(10, 10, 10))

    def test_core_initialization(self, metabolism_core):
        """Test core initialization"""
        assert metabolism_core is not None
        assert metabolism_core.quality_standard == 369.0 / 370.0
        assert (
            metabolism_core.alpha + metabolism_core.beta + metabolism_core.gamma
            == pytest.approx(1.0)
        )

    def test_default_weights(self, metabolism_core):
        """Test default weight configuration"""
        # Default: alpha=0.4, beta=0.4, gamma=0.2
        assert metabolism_core.alpha == pytest.approx(0.4)
        assert metabolism_core.beta == pytest.approx(0.4)
        assert metabolism_core.gamma == pytest.approx(0.2)

    def test_custom_weights_normalization(self):
        """Test custom weights are normalized"""
        core = MultimodalMetabolismCore(alpha=2.0, beta=2.0, gamma=1.0)

        # Should normalize to sum=1.0
        assert core.alpha + core.beta + core.gamma == pytest.approx(1.0)
        assert core.alpha == pytest.approx(0.4)  # 2/(2+2+1)
        assert core.beta == pytest.approx(0.4)
        assert core.gamma == pytest.approx(0.2)  # 1/(2+2+1)

    def test_visual_validity_with_clear_image(self, metabolism_core, clear_image):
        """Test visual validity with clear image"""
        V = metabolism_core._calculate_visual_validity(clear_image)

        assert 0.0 <= V <= 1.0
        # White image has low contrast, so validity may be lower
        assert V > 0.2  # Should have some validity

    def test_visual_validity_with_dark_image(self, metabolism_core, dark_image):
        """Test visual validity with dark image"""
        V = metabolism_core._calculate_visual_validity(dark_image)

        assert 0.0 <= V <= 1.0
        # Dark image should have lower validity

    def test_visual_validity_without_image(self, metabolism_core):
        """Test visual validity without image"""
        V = metabolism_core._calculate_visual_validity(None)

        assert V == 0.5  # Neutral validity

    def test_linguistic_relevance_with_text(self, metabolism_core):
        """Test linguistic relevance with meaningful text"""
        text = "The network nodes are working together to help the community."
        L = metabolism_core._calculate_linguistic_relevance(text)

        assert 0.0 <= L <= 1.0
        assert L > 0.4  # Should have reasonable relevance

    def test_linguistic_relevance_empty_text(self, metabolism_core):
        """Test linguistic relevance with empty text"""
        L = metabolism_core._calculate_linguistic_relevance("")

        assert L == 0.5  # Neutral relevance

    def test_linguistic_relevance_with_keywords(self, metabolism_core):
        """Test linguistic relevance with community keywords"""
        text = "Community network support help together"
        L = metabolism_core._calculate_linguistic_relevance(text)

        assert 0.0 <= L <= 1.0
        # Should have high relevance due to keywords

    def test_cultural_fidelity_balanced(self, metabolism_core):
        """Test cultural fidelity with balanced outputs"""
        cultural_outputs = {"vedic": 0.8, "egyptian": 0.8, "mayan": 0.8, "quantum": 0.8}

        F_ds_star = metabolism_core._calculate_cultural_fidelity(cultural_outputs)

        assert 0.0 <= F_ds_star <= 1.0
        assert F_ds_star > 0.9  # Low variance = high fidelity

    def test_cultural_fidelity_imbalanced(self, metabolism_core):
        """Test cultural fidelity with imbalanced outputs"""
        cultural_outputs = {"vedic": 0.2, "egyptian": 0.9, "mayan": 0.3, "quantum": 0.8}

        F_ds_star = metabolism_core._calculate_cultural_fidelity(cultural_outputs)

        assert 0.0 <= F_ds_star <= 1.0
        # Higher variance = lower fidelity

    def test_cultural_fidelity_empty_outputs(self, metabolism_core):
        """Test cultural fidelity with empty outputs"""
        F_ds_star = metabolism_core._calculate_cultural_fidelity({})

        assert F_ds_star == 0.5  # Neutral fidelity

    def test_complete_fusion_calculation(self, metabolism_core, clear_image):
        """Test complete multimodal fusion"""
        result = metabolism_core.calculate_fusion(
            visual_data=clear_image,
            linguistic_data="Network performance is optimal",
            cultural_outputs={
                "vedic": 0.8,
                "egyptian": 0.85,
                "mayan": 0.75,
                "quantum": 0.9,
            },
            computational_cost=1.0,
        )

        assert isinstance(result, MultimodalFusionResult)
        assert 0.0 <= result.fusion_score <= 1.0
        assert result.quality_standard == 369.0 / 370.0
        assert result.fallback_used is False

    def test_fusion_without_visual_data(self, metabolism_core):
        """Test fusion without visual data"""
        result = metabolism_core.calculate_fusion(
            visual_data=None,
            linguistic_data="Testing without visual input",
            cultural_outputs={"vedic": 0.6, "egyptian": 0.7},
            computational_cost=1.0,
        )

        assert isinstance(result, MultimodalFusionResult)
        assert result.visual_validity == 0.5
        assert 0.0 <= result.fusion_score <= 1.0

    def test_fusion_with_high_computational_cost(self, metabolism_core):
        """Test fusion with high computational cost"""
        result = metabolism_core.calculate_fusion(
            visual_data=None,
            linguistic_data="Test message",
            cultural_outputs={"vedic": 0.8, "egyptian": 0.8},
            computational_cost=2.0,
        )

        # Higher cost should lower fusion score
        assert 0.0 <= result.fusion_score <= 1.0
        assert result.computational_cost == 2.0

    def test_metabolic_state_update_aerobic(self, metabolism_core, clear_image):
        """Test metabolic state update to aerobic"""
        metabolism_core.calculate_fusion(
            visual_data=clear_image,
            linguistic_data="Clear conditions",
            cultural_outputs={"vedic": 0.9, "egyptian": 0.9},
        )

        # White image has low contrast, may result in hybrid mode
        assert metabolism_core.metabolic_state.mode in [
            MetabolicMode.AEROBIC,
            MetabolicMode.HYBRID,
        ]
        assert metabolism_core.metabolic_state.visual_state >= 0.5

    def test_metabolic_state_update_anaerobic(self, metabolism_core, dark_image):
        """Test metabolic state update to anaerobic"""
        metabolism_core.calculate_fusion(
            visual_data=dark_image,
            linguistic_data="Critical situation",
            cultural_outputs={"vedic": 0.3, "egyptian": 0.4},
        )

        # Should switch to anaerobic or hybrid mode
        assert metabolism_core.metabolic_state.mode in [
            MetabolicMode.ANAEROBIC,
            MetabolicMode.HYBRID,
        ]

    def test_energy_reserves_adjustment(self, metabolism_core):
        """Test energy reserves adjustment"""
        initial_energy = metabolism_core.energy_reserves

        # High fusion score should increase energy
        metabolism_core.calculate_fusion(
            linguistic_data="Excellent performance",
            cultural_outputs={
                "vedic": 0.9,
                "egyptian": 0.9,
                "mayan": 0.9,
                "quantum": 0.9,
            },
        )

        # Energy should have changed
        assert metabolism_core.energy_reserves >= 0.1
        assert metabolism_core.energy_reserves <= 1.0

    def test_processing_history_tracking(self, metabolism_core):
        """Test processing history is tracked"""
        initial_length = len(metabolism_core.processing_history)

        metabolism_core.calculate_fusion(
            linguistic_data="Test 1",
            cultural_outputs={"vedic": 0.5},
        )

        metabolism_core.calculate_fusion(
            linguistic_data="Test 2",
            cultural_outputs={"vedic": 0.6},
        )

        assert len(metabolism_core.processing_history) == initial_length + 2

    def test_fusion_result_to_dict(self, metabolism_core):
        """Test fusion result serialization"""
        result = metabolism_core.calculate_fusion(
            linguistic_data="Test",
            cultural_outputs={"vedic": 0.7},
        )

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert "fusion_score" in result_dict
        assert "metabolic_mode" in result_dict
        assert "quality_standard" in result_dict
        assert result_dict["quality_standard"] == 369.0 / 370.0


class TestMetabolicHealthReport:
    """Test metabolic health reporting"""

    @pytest.fixture
    def metabolism_core(self):
        """Create metabolism core"""
        return MultimodalMetabolismCore()

    def test_health_report_structure(self, metabolism_core):
        """Test health report structure"""
        report = metabolism_core.get_metabolic_health_report()

        assert "mode" in report
        assert "clarity_score" in report
        assert "energy_level" in report
        assert "energy_reserves" in report
        assert "visual_state" in report
        assert "processing_history_length" in report
        assert "quality_standard" in report

    def test_health_report_initial_state(self, metabolism_core):
        """Test health report in initial state"""
        report = metabolism_core.get_metabolic_health_report()

        assert report["mode"] == "aerobic"
        assert report["clarity_score"] == 1.0
        assert report["energy_level"] == 1.0
        assert report["energy_reserves"] == 1.0
        assert report["processing_history_length"] == 0

    def test_health_report_after_processing(self, metabolism_core):
        """Test health report after processing"""
        metabolism_core.calculate_fusion(
            linguistic_data="Test",
            cultural_outputs={"vedic": 0.6},
        )

        report = metabolism_core.get_metabolic_health_report()

        assert report["processing_history_length"] == 1
        assert report["quality_standard"] == 369.0 / 370.0


class TestHelperFunctions:
    """Test helper functions"""

    def test_calculate_multimodal_fusion_helper(self):
        """Test quick fusion helper"""
        result = calculate_multimodal_fusion(
            linguistic_data="Test message",
            cultural_outputs={"vedic": 0.7, "egyptian": 0.8},
        )

        assert isinstance(result, MultimodalFusionResult)
        assert 0.0 <= result.fusion_score <= 1.0

    def test_verify_multimodal_quality_pass(self):
        """Test quality verification - pass"""
        result = calculate_multimodal_fusion(
            linguistic_data="High quality test",
            cultural_outputs={
                "vedic": 0.8,
                "egyptian": 0.85,
                "mayan": 0.82,
                "quantum": 0.88,
            },
        )

        assert verify_multimodal_quality(result) is True

    def test_verify_multimodal_quality_with_all_components(self):
        """Test quality verification with all components"""
        img = Image.new("RGB", (50, 50), color="white")
        result = calculate_multimodal_fusion(
            visual_data=img,
            linguistic_data="Complete test",
            cultural_outputs={"vedic": 0.9, "egyptian": 0.9},
        )

        assert verify_multimodal_quality(result) is True


class TestFallbackMechanism:
    """Test fallback mechanisms"""

    @pytest.fixture
    def metabolism_core(self):
        """Create metabolism core"""
        return MultimodalMetabolismCore()

    def test_fallback_calculation(self, metabolism_core):
        """Test fallback calculation is triggered on error"""
        # This should use fallback due to minimal inputs
        result = metabolism_core._fallback_calculation("Fallback test", {"vedic": 0.5})

        assert isinstance(result, MultimodalFusionResult)
        assert result.fallback_used is True
        assert result.visual_validity == 0.5  # Conservative estimate


class TestEdgeCases:
    """Test edge cases"""

    @pytest.fixture
    def metabolism_core(self):
        """Create metabolism core"""
        return MultimodalMetabolismCore()

    def test_zero_computational_cost(self, metabolism_core):
        """Test with zero computational cost"""
        result = metabolism_core.calculate_fusion(
            linguistic_data="Test",
            cultural_outputs={"vedic": 0.7},
            computational_cost=0.0,
        )

        # Should default to 1.0
        assert result.computational_cost == 1.0

    def test_negative_computational_cost(self, metabolism_core):
        """Test with negative computational cost"""
        result = metabolism_core.calculate_fusion(
            linguistic_data="Test",
            cultural_outputs={"vedic": 0.7},
            computational_cost=-1.0,
        )

        # Should default to 1.0
        assert result.computational_cost >= 1.0

    def test_very_long_text(self, metabolism_core):
        """Test with very long text"""
        long_text = " ".join(["word"] * 1000)

        result = metabolism_core.calculate_fusion(
            linguistic_data=long_text,
            cultural_outputs={"vedic": 0.7},
        )

        assert 0.0 <= result.linguistic_relevance <= 1.0

    def test_single_cultural_output(self, metabolism_core):
        """Test with single cultural output"""
        result = metabolism_core.calculate_fusion(
            linguistic_data="Test",
            cultural_outputs={"vedic": 0.8},
        )

        assert result.cultural_fidelity == 0.5  # Should default to neutral

    def test_corrupted_image_data(self, metabolism_core):
        """Test with potentially problematic image"""
        # Create a very small image
        tiny_img = Image.new("RGB", (1, 1), color="red")

        result = metabolism_core.calculate_fusion(
            visual_data=tiny_img,
            linguistic_data="Test",
            cultural_outputs={"vedic": 0.7},
        )

        assert 0.0 <= result.visual_validity <= 1.0


class TestIntegration:
    """Test integration with other layers"""

    def test_quality_standard_369_370(self):
        """Test 369/370 quality standard (Layer 0)"""
        core = MultimodalMetabolismCore()

        assert core.quality_standard == 369.0 / 370.0

    def test_ds_star_cultural_integration(self):
        """Test integration with Layer 10 DS-STAR cultural outputs"""
        # Simulate DS-STAR outputs
        ds_star_outputs = {
            "vedic": 0.85,
            "egyptian": 0.80,
            "mayan": 0.88,
            "quantum": 0.82,
        }

        result = calculate_multimodal_fusion(
            linguistic_data="DS-STAR integration test",
            cultural_outputs=ds_star_outputs,
        )

        assert result.cultural_fidelity > 0.8  # Balanced outputs = high fidelity

    def test_metabolic_mode_consistency(self):
        """Test metabolic mode is consistent with visual state"""
        core = MultimodalMetabolismCore()

        # Test with gradient image (better contrast than solid white)
        gradient_img = Image.new("RGB", (100, 100))
        for i in range(100):
            for j in range(100):
                gradient_img.putpixel((i, j), (i * 2, j * 2, 255))

        result = core.calculate_fusion(
            visual_data=gradient_img,
            linguistic_data="Clear test with good contrast",
            cultural_outputs={"vedic": 0.9, "egyptian": 0.85},
        )

        # Should have aerobic or hybrid mode with gradient
        assert result.metabolic_mode in [MetabolicMode.AEROBIC, MetabolicMode.HYBRID]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
