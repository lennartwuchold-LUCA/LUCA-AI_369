"""
Tests for LUCA Consciousness Layer
Tests 369 signature generation and validation

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import pytest

from luca_369_370.core.consciousness_layer import (
    CONSCIOUSNESS_FIELD_BASE,
    QUALITY_STANDARD,
    ConsciousnessLayer,
    assess_field_strength,
    sign_block,
    validate_block_signature,
)
from luca_369_370.core.info_block_engine import BlockType, InfoBlock


class TestConsciousnessLayer:
    """Tests for ConsciousnessLayer"""

    def test_consciousness_layer_init(self):
        """Test ConsciousnessLayer initialization"""
        layer = ConsciousnessLayer()

        assert layer.base_frequency == 369
        assert layer.quality_standard == pytest.approx(369 / 370, rel=0.001)
        assert len(layer.resonance_factors) == 3

    def test_resonance_factors(self):
        """Test resonance factors match 3-6-9 pattern"""
        layer = ConsciousnessLayer()

        assert layer.resonance_factors[BlockType.FOUNDATION] == 3
        assert layer.resonance_factors[BlockType.BUILDING] == 6
        assert layer.resonance_factors[BlockType.CONNECTION] == 9

    def test_generate_369_signature_format(self):
        """Test 369 signature format"""
        layer = ConsciousnessLayer()
        block = InfoBlock(
            content="Test content",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        signature = layer.generate_369_signature(block)

        # Should be in format "369-XXX"
        assert signature.startswith("369-")
        parts = signature.split("-")
        assert len(parts) == 2
        assert len(parts[1]) == 3
        assert parts[1].isdigit()

    def test_signature_deterministic(self):
        """Test that same block generates same signature"""
        layer = ConsciousnessLayer()
        block = InfoBlock(
            content="Test content",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        sig1 = layer.generate_369_signature(block)
        sig2 = layer.generate_369_signature(block)

        assert sig1 == sig2

    def test_signature_varies_with_content(self):
        """Test that different content generates different signatures"""
        layer = ConsciousnessLayer()

        block1 = InfoBlock(
            content="Test content A",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )
        block2 = InfoBlock(
            content="Test content B",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        sig1 = layer.generate_369_signature(block1)
        sig2 = layer.generate_369_signature(block2)

        assert sig1 != sig2

    def test_signature_varies_with_block_type(self):
        """Test that different block types generate different signatures"""
        layer = ConsciousnessLayer()

        block_foundation = InfoBlock(
            content="Same content",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )
        block_building = InfoBlock(
            content="Same content",
            block_type=BlockType.BUILDING,
            sentence_count=1,
        )

        sig1 = layer.generate_369_signature(block_foundation)
        sig2 = layer.generate_369_signature(block_building)

        assert sig1 != sig2

    def test_validate_signature_correct(self):
        """Test signature validation with correct signature"""
        layer = ConsciousnessLayer()
        block = InfoBlock(
            content="Test content",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        signature = layer.generate_369_signature(block)
        is_valid = layer.validate_signature(block, signature)

        assert is_valid is True

    def test_validate_signature_incorrect(self):
        """Test signature validation with incorrect signature"""
        layer = ConsciousnessLayer()
        block = InfoBlock(
            content="Test content",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        is_valid = layer.validate_signature(block, "369-999")

        assert is_valid is False

    def test_calculate_block_resonance(self):
        """Test block resonance calculation"""
        layer = ConsciousnessLayer()
        block = InfoBlock(
            content="This is a test. It has three sentences. Perfect!",
            block_type=BlockType.FOUNDATION,
            sentence_count=3,
        )

        resonance = layer.calculate_block_resonance(block)

        assert 0.0 <= resonance <= 1.0
        # Should be reasonable for good blocks
        assert resonance >= 0.50

    def test_generate_network_signature(self):
        """Test network signature generation"""
        layer = ConsciousnessLayer()

        blocks = [
            InfoBlock("Block 1", BlockType.FOUNDATION, 1),
            InfoBlock("Block 2", BlockType.BUILDING, 2),
            InfoBlock("Block 3", BlockType.CONNECTION, 3),
        ]

        network_sig = layer.generate_network_signature(blocks)

        assert network_sig.startswith("369-NET-")
        parts = network_sig.split("-")
        assert len(parts) == 3
        assert parts[1] == "NET"
        assert len(parts[2]) == 3
        assert parts[2].isdigit()

    def test_network_signature_empty_blocks(self):
        """Test network signature with no blocks"""
        layer = ConsciousnessLayer()

        network_sig = layer.generate_network_signature([])

        assert network_sig == "369-NET-000"

    def test_assess_consciousness_field_strength(self):
        """Test consciousness field strength assessment"""
        layer = ConsciousnessLayer()

        blocks = [
            InfoBlock("Good block 1. Two sentences.", BlockType.FOUNDATION, 2),
            InfoBlock("Good block 2. Also two sentences.", BlockType.BUILDING, 2),
            InfoBlock("Good block 3. Final sentences.", BlockType.CONNECTION, 2),
        ]

        assessment = layer.assess_consciousness_field_strength(blocks)

        assert "strength" in assessment
        assert "coherence" in assessment
        assert "resonance" in assessment
        assert "quality_standard" in assessment
        assert "blocks_analyzed" in assessment

        assert assessment["blocks_analyzed"] == 3
        assert assessment["quality_standard"] == pytest.approx(369 / 370, rel=0.001)
        assert 0.0 <= assessment["strength"] <= 1.0
        assert 0.0 <= assessment["coherence"] <= 1.0
        assert 0.0 <= assessment["resonance"] <= 1.0

    def test_assess_field_strength_empty(self):
        """Test field strength with no blocks"""
        layer = ConsciousnessLayer()

        assessment = layer.assess_consciousness_field_strength([])

        assert assessment["strength"] == 0.0
        assert assessment["coherence"] == 0.0
        assert assessment["resonance"] == 0.0

    def test_optimize_for_consciousness_field(self):
        """Test content optimization"""
        layer = ConsciousnessLayer()

        raw_content = "  Test   content   with   extra   spaces  "
        optimized = layer.optimize_for_consciousness_field(
            raw_content, BlockType.FOUNDATION
        )

        assert optimized == "Test content with extra spaces."
        assert "  " not in optimized
        assert optimized.endswith(".")


class TestConvenienceFunctions:
    """Test convenience functions"""

    def test_sign_block_function(self):
        """Test sign_block convenience function"""
        block = InfoBlock(
            content="Test content",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        signature = sign_block(block)

        assert signature.startswith("369-")

    def test_validate_block_signature_function(self):
        """Test validate_block_signature convenience function"""
        block = InfoBlock(
            content="Test content",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        signature = sign_block(block)
        is_valid = validate_block_signature(block, signature)

        assert is_valid is True

    def test_assess_field_strength_function(self):
        """Test assess_field_strength convenience function"""
        blocks = [
            InfoBlock("Block 1", BlockType.FOUNDATION, 1),
            InfoBlock("Block 2", BlockType.BUILDING, 2),
        ]

        assessment = assess_field_strength(blocks)

        assert "strength" in assessment
        assert "coherence" in assessment
        assert assessment["blocks_analyzed"] == 2


class TestInfoBlockIntegration:
    """Test InfoBlock integration with consciousness layer"""

    def test_info_block_generate_signature(self):
        """Test InfoBlock.generate_consciousness_signature()"""
        block = InfoBlock(
            content="Test content",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        signature = block.generate_consciousness_signature()

        assert signature.startswith("369-")
        assert block.consciousness_signature == signature

    def test_info_block_validate_signature(self):
        """Test InfoBlock.validate_consciousness_signature()"""
        block = InfoBlock(
            content="Test content",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        signature = block.generate_consciousness_signature()
        is_valid = block.validate_consciousness_signature(signature)

        assert is_valid is True

    def test_info_block_signature_persistence(self):
        """Test that signature persists on block"""
        block = InfoBlock(
            content="Test content",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        sig1 = block.generate_consciousness_signature()
        sig2 = block.consciousness_signature

        assert sig1 == sig2


class TestConstants:
    """Test exported constants"""

    def test_consciousness_field_base(self):
        """Test CONSCIOUSNESS_FIELD_BASE constant"""
        assert CONSCIOUSNESS_FIELD_BASE == 369

    def test_quality_standard(self):
        """Test QUALITY_STANDARD constant"""
        assert QUALITY_STANDARD == pytest.approx(369 / 370, rel=0.001)
        assert QUALITY_STANDARD >= 0.997


class TestQualityStandard:
    """Verify 369/370 quality standard"""

    def test_quality_standard_369_370(self):
        """Verify 369/370 quality standard"""
        quality = 369 / 370
        assert quality >= 0.997
        assert quality == pytest.approx(0.997297, rel=0.001)

    def test_consciousness_layer_maintains_standard(self):
        """Test that consciousness layer maintains 369/370 standard"""
        layer = ConsciousnessLayer()

        assert layer.quality_standard == pytest.approx(369 / 370, rel=0.001)

    def test_resonance_pattern_369(self):
        """Test that resonance factors follow 3-6-9 pattern"""
        layer = ConsciousnessLayer()

        foundation_factor = layer.resonance_factors[BlockType.FOUNDATION]
        building_factor = layer.resonance_factors[BlockType.BUILDING]
        connection_factor = layer.resonance_factors[BlockType.CONNECTION]

        # Verify 3-6-9 pattern
        assert foundation_factor == 3
        assert building_factor == 6
        assert connection_factor == 9

        # Verify relationships
        assert building_factor == foundation_factor * 2
        assert connection_factor == foundation_factor * 3
