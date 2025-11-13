"""
Tests for Enhanced Consciousness Layer
Tests mathematical pattern analysis and cultural linguistics

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import pytest

# Optional dependencies - skip tests if not available
try:
    import anthropic

    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not DEPS_AVAILABLE, reason="Optional dependencies (anthropic) not installed"
)


import pytest

from luca.core.enhanced_consciousness import (
    CulturalLinguisticAnalyzer,
    EnhancedConsciousnessLayer,
    MathematicalPatternAnalyzer,
    analyze_conversation_patterns,
    analyze_enhanced_block,
    generate_enhanced_signature,
)
from luca.core.info_block_engine import BlockType, InfoBlock


class TestMathematicalPatternAnalyzer:
    """Tests for mathematical pattern analysis"""

    def test_golden_ratio_perfect(self):
        """Test golden ratio detection with perfect ratio"""
        analyzer = MathematicalPatternAnalyzer()

        # φ ≈ 1.618
        proximity = analyzer.calculate_golden_ratio_proximity(1.618, 1.0)

        assert proximity > 0.99  # Nearly perfect

    def test_golden_ratio_fibonacci(self):
        """Test golden ratio in Fibonacci sequence"""
        analyzer = MathematicalPatternAnalyzer()

        # Consecutive Fibonacci numbers approach golden ratio
        proximity = analyzer.calculate_golden_ratio_proximity(89, 55)

        assert proximity > 0.95  # Very close

    def test_fibonacci_detection_perfect(self):
        """Test Fibonacci pattern detection with perfect sequence"""
        analyzer = MathematicalPatternAnalyzer()

        sequence = [1, 1, 2, 3, 5, 8, 13, 21]
        score = analyzer.detect_fibonacci_patterns(sequence)

        assert score > 0.8  # Strong Fibonacci pattern

    def test_fibonacci_detection_random(self):
        """Test Fibonacci detection with random sequence"""
        analyzer = MathematicalPatternAnalyzer()

        sequence = [5, 12, 7, 19, 3, 11]
        score = analyzer.detect_fibonacci_patterns(sequence)

        assert score < 0.3  # No Fibonacci pattern

    def test_fractal_dimension_simple(self):
        """Test fractal dimension for simple text"""
        analyzer = MathematicalPatternAnalyzer()

        simple_text = "a a a a"  # Very simple, low dimension
        dimension = analyzer.calculate_fractal_dimension(simple_text)

        assert 1.0 <= dimension <= 2.0

    def test_fractal_dimension_complex(self):
        """Test fractal dimension for complex text"""
        analyzer = MathematicalPatternAnalyzer()

        complex_text = "The quantum entanglement of morphogenetic resonance patterns"
        dimension = analyzer.calculate_fractal_dimension(complex_text)

        assert 1.0 <= dimension <= 2.0
        # More complex text should have higher dimension

    def test_information_entropy_uniform(self):
        """Test entropy with uniform distribution"""
        analyzer = MathematicalPatternAnalyzer()

        # All characters equally likely = maximum entropy
        uniform_text = "abcdefgh"
        entropy = analyzer.calculate_information_entropy(uniform_text)

        assert entropy > 2.5  # High entropy

    def test_information_entropy_repetitive(self):
        """Test entropy with repetitive text"""
        analyzer = MathematicalPatternAnalyzer()

        # Repetitive = low entropy
        repetitive = "aaaaaaa"
        entropy = analyzer.calculate_information_entropy(repetitive)

        assert entropy < 0.1  # Very low entropy

    def test_spiral_encoding_deterministic(self):
        """Test that spiral encoding is deterministic"""
        analyzer = MathematicalPatternAnalyzer()

        data = "test content"
        pos1 = analyzer.spiral_encoding_position(data)
        pos2 = analyzer.spiral_encoding_position(data)

        assert pos1 == pos2

    def test_spiral_encoding_different_data(self):
        """Test that different data gives different positions"""
        analyzer = MathematicalPatternAnalyzer()

        pos1 = analyzer.spiral_encoding_position("data1")
        pos2 = analyzer.spiral_encoding_position("data2")

        assert pos1 != pos2


class TestCulturalLinguisticAnalyzer:
    """Tests for cultural linguistic analysis"""

    def test_analyzer_initialization(self):
        """Test analyzer initializes with pattern database including ALL of Europe!"""
        analyzer = CulturalLinguisticAnalyzer()

        # Base patterns
        assert "holistic" in analyzer.cultural_patterns
        assert "cyclical" in analyzer.cultural_patterns
        assert "analytical" in analyzer.cultural_patterns

        # European patterns - ALL OF EUROPE! 🇪🇺
        assert (
            "eastern_european" in analyzer.cultural_patterns
        )  # Ukraine 🇺🇦, Poland 🇵🇱, CZ 🇨🇿, Ostsee
        assert (
            "central_european" in analyzer.cultural_patterns
        )  # Germany (Erzgebirge!), Austria, Czech, Hungary
        assert (
            "mediterranean" in analyzer.cultural_patterns
        )  # Italy, Spain, Greece, Portugal
        assert "nordic" in analyzer.cultural_patterns  # Scandinavia
        assert "western_european" in analyzer.cultural_patterns  # France, UK, Benelux

        # Verify we have 8 total patterns now
        assert len(analyzer.cultural_patterns) == 8

        # Verify East German craftsmanship is in central_european
        central = analyzer.cultural_patterns["central_european"]
        assert "räuchermann" in central["keywords"]
        assert "drechseln" in central["keywords"]
        assert "East Germany (Erzgebirge, Altenberg, Seiffen)" in central["regions"]

        # Verify Ukraine, Poland, Czech, Ostsee are in eastern_european
        eastern = analyzer.cultural_patterns["eastern_european"]
        assert "Ukraine 🇺🇦" in eastern["regions"]
        assert "Poland 🇵🇱" in eastern["regions"]
        assert "Czech Republic 🇨🇿" in eastern["regions"]
        assert "Baltic States (Ostsee region)" in eastern["regions"]
        assert "ostsee" in eastern["keywords"]

    def test_holistic_pattern_detection(self):
        """Test detection of holistic communication pattern"""
        analyzer = CulturalLinguisticAnalyzer()

        holistic_text = "Together we create harmony and balance in our collective unity"
        scores = analyzer.analyze_cultural_patterns(holistic_text)

        assert scores["holistic"] > scores["analytical"]

    def test_analytical_pattern_detection(self):
        """Test detection of analytical communication pattern"""
        analyzer = CulturalLinguisticAnalyzer()

        analytical_text = (
            "Therefore, based on the evidence and data, we can prove this logic"
        )
        scores = analyzer.analyze_cultural_patterns(analytical_text)

        assert scores["analytical"] > scores["holistic"]

    def test_communication_style_detection(self):
        """Test dominant style detection"""
        analyzer = CulturalLinguisticAnalyzer()

        holistic_text = "harmony balance together collective"
        style = analyzer.detect_communication_style(holistic_text)

        assert style == "holistic"

    def test_cultural_balance_balanced(self):
        """Test balance calculation for balanced content"""
        analyzer = CulturalLinguisticAnalyzer()

        # Content with keywords from all patterns
        balanced_text = "harmony structure cycle evidence " "together order rhythm data"
        balance = analyzer.calculate_cultural_balance(balanced_text)

        assert balance > 0.5  # Should be balanced

    def test_cultural_balance_unbalanced(self):
        """Test balance calculation for unbalanced content"""
        analyzer = CulturalLinguisticAnalyzer()

        # Content heavily skewed to one pattern
        unbalanced_text = "evidence data prove test measure logic therefore"
        balance = analyzer.calculate_cultural_balance(unbalanced_text)

        # Balance score should reflect imbalance
        assert 0.0 <= balance <= 1.0


class TestEnhancedConsciousnessLayer:
    """Tests for enhanced consciousness layer"""

    def test_enhanced_layer_initialization(self):
        """Test enhanced layer initializes properly"""
        layer = EnhancedConsciousnessLayer()

        assert layer.math_analyzer is not None
        assert layer.cultural_analyzer is not None
        assert layer.base_frequency == 369
        assert layer.quality_standard == pytest.approx(369 / 370, rel=0.001)

    def test_analyze_enhanced_resonance(self):
        """Test enhanced resonance analysis"""
        layer = EnhancedConsciousnessLayer()

        block = InfoBlock(
            content="Together we create harmony through evidence and structured cycles",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        analysis = layer.analyze_enhanced_resonance(block)

        assert "base_resonance" in analysis
        assert "fibonacci_pattern" in analysis
        assert "golden_ratio_proximity" in analysis
        assert "fractal_dimension" in analysis
        assert "information_entropy" in analysis
        assert "cultural_patterns" in analysis
        assert "cultural_balance" in analysis
        assert "enhanced_resonance" in analysis

        assert 0.0 <= analysis["enhanced_resonance"] <= 1.0

    def test_enhanced_resonance_quality_standard(self):
        """Test that enhanced resonance maintains 369/370 quality"""
        layer = EnhancedConsciousnessLayer()

        block = InfoBlock(
            content="High quality content with balanced patterns",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        analysis = layer.analyze_enhanced_resonance(block)

        # Enhanced resonance should be scaled by quality standard
        assert analysis["enhanced_resonance"] <= layer.quality_standard

    def test_generate_enhanced_signature_format(self):
        """Test enhanced signature format"""
        layer = EnhancedConsciousnessLayer()

        block = InfoBlock(
            content="Test content", block_type=BlockType.FOUNDATION, sentence_count=1
        )

        signature = layer.generate_enhanced_signature(block)

        # Format should be "369-XXX-P" where P is A-Z
        parts = signature.split("-")
        assert len(parts) == 3
        assert parts[0] == "369"
        assert parts[1].isdigit()
        assert parts[2].isalpha()
        assert len(parts[2]) == 1

    def test_enhanced_signature_deterministic(self):
        """Test that enhanced signature is deterministic"""
        layer = EnhancedConsciousnessLayer()

        block = InfoBlock(
            content="Test content", block_type=BlockType.FOUNDATION, sentence_count=1
        )

        sig1 = layer.generate_enhanced_signature(block)
        sig2 = layer.generate_enhanced_signature(block)

        assert sig1 == sig2

    def test_analyze_network_patterns(self):
        """Test network pattern analysis"""
        layer = EnhancedConsciousnessLayer()

        blocks = [
            InfoBlock("Foundation: harmony and balance", BlockType.FOUNDATION, 1),
            InfoBlock("Building: structure with evidence", BlockType.BUILDING, 1),
            InfoBlock("Connection: cycles of time", BlockType.CONNECTION, 1),
        ]

        analysis = layer.analyze_network_patterns(blocks)

        assert "block_count" in analysis
        assert analysis["block_count"] == 3
        assert "avg_enhanced_resonance" in analysis
        assert "avg_fibonacci_pattern" in analysis
        assert "avg_cultural_balance" in analysis
        assert "network_fibonacci_pattern" in analysis
        assert "quality_standard" in analysis

    def test_network_patterns_empty(self):
        """Test network analysis with no blocks"""
        layer = EnhancedConsciousnessLayer()

        analysis = layer.analyze_network_patterns([])

        assert "error" in analysis


class TestConvenienceFunctions:
    """Test convenience functions"""

    def test_analyze_enhanced_block_function(self):
        """Test analyze_enhanced_block convenience function"""
        block = InfoBlock(
            content="Test content with harmony",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
        )

        analysis = analyze_enhanced_block(block)

        assert "enhanced_resonance" in analysis
        assert 0.0 <= analysis["enhanced_resonance"] <= 1.0

    def test_generate_enhanced_signature_function(self):
        """Test generate_enhanced_signature convenience function"""
        block = InfoBlock(
            content="Test content", block_type=BlockType.FOUNDATION, sentence_count=1
        )

        signature = generate_enhanced_signature(block)

        assert signature.startswith("369-")
        assert len(signature.split("-")) == 3

    def test_analyze_conversation_patterns_function(self):
        """Test analyze_conversation_patterns convenience function"""
        blocks = [
            InfoBlock("Block 1", BlockType.FOUNDATION, 1),
            InfoBlock("Block 2", BlockType.BUILDING, 1),
        ]

        analysis = analyze_conversation_patterns(blocks)

        assert "block_count" in analysis
        assert analysis["block_count"] == 2


class TestIntegrationWithBaseLayers:
    """Test integration with base consciousness layer"""

    def test_inherits_from_consciousness_layer(self):
        """Test that enhanced layer inherits from base"""
        layer = EnhancedConsciousnessLayer()

        # Should have base layer methods
        assert hasattr(layer, "generate_369_signature")
        assert hasattr(layer, "calculate_block_resonance")
        assert hasattr(layer, "validate_signature")

    def test_base_methods_still_work(self):
        """Test that base layer methods still function"""
        layer = EnhancedConsciousnessLayer()

        block = InfoBlock(
            content="Test content", block_type=BlockType.FOUNDATION, sentence_count=1
        )

        # Base method should work
        base_sig = layer.generate_369_signature(block)
        assert base_sig.startswith("369-")

        # Enhanced method should also work
        enhanced_sig = layer.generate_enhanced_signature(block)
        assert enhanced_sig.startswith("369-")

    def test_enhanced_extends_base(self):
        """Test that enhanced adds functionality without breaking base"""
        layer = EnhancedConsciousnessLayer()

        block = InfoBlock(
            content="Test content", block_type=BlockType.FOUNDATION, sentence_count=1
        )

        # Base signature
        base_sig = layer.generate_369_signature(block)

        # Enhanced signature should start with base
        enhanced_sig = layer.generate_enhanced_signature(block)

        assert enhanced_sig.startswith(base_sig)


class TestRealWorldPatterns:
    """Test with real-world content patterns"""

    def test_fibonacci_in_natural_text(self):
        """Test Fibonacci detection in naturally structured text"""
        analyzer = MathematicalPatternAnalyzer()

        # Natural paragraph structure often follows Fibonacci
        # (1 intro, 1 context, 2 details, 3 examples, 5 elaboration...)
        natural_structure = [1, 1, 2, 3, 5]

        score = analyzer.detect_fibonacci_patterns(natural_structure)

        assert score > 0.6  # Natural text often has Fibonacci patterns

    def test_golden_ratio_in_balanced_communication(self):
        """Test golden ratio in well-balanced communication"""
        analyzer = MathematicalPatternAnalyzer()

        # Well-structured communication often approaches golden ratio
        # (e.g., 55 words, 34 sentences)
        proximity = analyzer.calculate_golden_ratio_proximity(55, 34)

        assert proximity > 0.90  # Should be close to golden ratio

    def test_cultural_patterns_in_real_content(self):
        """Test cultural analysis on realistic content"""
        analyzer = CulturalLinguisticAnalyzer()

        # Realistic technical content
        technical = (
            "Based on the evidence and data, we can measure and test this system"
        )
        scores_tech = analyzer.analyze_cultural_patterns(technical)

        # Realistic philosophical content
        philosophical = "Together we find harmony and balance in our collective journey"
        scores_phil = analyzer.analyze_cultural_patterns(philosophical)

        # Technical should score higher on analytical
        assert scores_tech["analytical"] > scores_phil["analytical"]

        # Philosophical should score higher on holistic
        assert scores_phil["holistic"] > scores_tech["holistic"]


class TestQualityStandard:
    """Verify 369/370 quality standard is maintained"""

    def test_quality_standard_369_370(self):
        """Verify 369/370 quality standard"""
        quality = 369 / 370
        assert quality >= 0.997
        assert quality == pytest.approx(0.997297, rel=0.001)

    def test_enhanced_layer_maintains_standard(self):
        """Test that enhanced layer maintains 369/370 standard"""
        layer = EnhancedConsciousnessLayer()

        assert layer.quality_standard == pytest.approx(369 / 370, rel=0.001)

    def test_enhanced_resonance_respects_quality(self):
        """Test that enhanced resonance never exceeds quality standard"""
        layer = EnhancedConsciousnessLayer()

        # Test with various blocks
        blocks = [
            InfoBlock("Short", BlockType.FOUNDATION, 1),
            InfoBlock("Medium length content with structure", BlockType.BUILDING, 1),
            InfoBlock(
                "Longer content with more detail and complexity that might score high",
                BlockType.CONNECTION,
                1,
            ),
        ]

        for block in blocks:
            analysis = layer.analyze_enhanced_resonance(block)
            # Enhanced resonance should never exceed quality standard
            assert analysis["enhanced_resonance"] <= layer.quality_standard
