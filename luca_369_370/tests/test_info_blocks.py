"""
LUCA 369/370 - Unit Tests
Pytest-Tests für Info-Block-Engine
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.block_formatter import BlockFormatter
from core.info_block_engine import (
    BlockType,
    InfoBlock,
    InfoBlockEngine,
    QualityException,
)
from core.quality_validator import QualityValidator


class TestInfoBlock:
    """Tests für InfoBlock-Klasse"""

    def test_valid_block_creation(self):
        """Test: Valider Block wird erstellt"""
        block = InfoBlock(
            content="Sentence one. Sentence two. Sentence three.",
            block_type=BlockType.FOUNDATION,
            sentence_count=3,
        )
        assert block.validate_quality() == True

    def test_invalid_block_too_many_sentences(self):
        """Test: Block mit >3 Sätzen wird rejected"""
        block = InfoBlock(
            content="One. Two. Three. Four.",
            block_type=BlockType.FOUNDATION,
            sentence_count=4,
        )
        assert block.validate_quality() == False

    def test_empty_block_invalid(self):
        """Test: Leerer Block ist invalid"""
        block = InfoBlock(content="", block_type=BlockType.FOUNDATION, sentence_count=0)
        assert block.validate_quality() == False

    def test_block_with_preview(self):
        """Test: Block mit Next-Preview wird korrekt erstellt"""
        block = InfoBlock(
            content="Test content.",
            block_type=BlockType.FOUNDATION,
            sentence_count=1,
            has_next_preview=True,
            next_block_hint="More coming",
        )
        assert block.has_next_preview == True
        assert block.next_block_hint == "More coming"


class TestInfoBlockEngine:
    """Tests für InfoBlockEngine"""

    def test_engine_initialization(self):
        """Test: Engine initialisiert korrekt"""
        engine = InfoBlockEngine()
        assert engine.max_blocks_per_response == 5
        assert engine.max_sentences_per_block == 3
        assert engine.quality_threshold == 369 / 370

    def test_foundation_block_creation(self):
        """Test: Foundation Block wird erstellt"""
        engine = InfoBlockEngine()
        block = engine.create_foundation_block("Test Concept")

        assert block.block_type == BlockType.FOUNDATION
        assert block.has_next_preview == True
        assert block.validate_quality() == True

    def test_building_block_creation(self):
        """Test: Building Block wird erstellt"""
        engine = InfoBlockEngine()
        foundation = engine.create_foundation_block("Foundation")
        building = engine.create_building_block(foundation, "Detail Aspect")

        assert building.block_type == BlockType.BUILDING
        assert building.validate_quality() == True

    def test_connection_block_creation(self):
        """Test: Connection Block wird erstellt"""
        engine = InfoBlockEngine()
        foundation = engine.create_foundation_block("Foundation")
        connection = engine.create_connection_block([foundation], "Application")

        assert connection.block_type == BlockType.CONNECTION
        assert connection.has_next_preview == False
        assert connection.validate_quality() == True

    def test_generate_response_structure(self):
        """Test: Generierte Response hat korrekte Struktur"""
        engine = InfoBlockEngine()
        blocks = engine.generate_response("Test query")

        # Should have at least foundation and connection
        assert len(blocks) >= 2
        assert len(blocks) <= 5

        # First should be foundation
        assert blocks[0].block_type == BlockType.FOUNDATION

        # Last should be connection
        assert blocks[-1].block_type == BlockType.CONNECTION

    def test_response_quality_validation(self):
        """Test: Response Quality Validation funktioniert"""
        engine = InfoBlockEngine()

        # Valid response
        valid_blocks = [
            InfoBlock("Test.", BlockType.FOUNDATION, 1),
            InfoBlock("Test.", BlockType.CONNECTION, 1),
        ]
        assert engine._validate_response_quality(valid_blocks) == True

        # Invalid: too many blocks
        invalid_blocks = [
            InfoBlock(f"Block {i}.", BlockType.FOUNDATION, 1) for i in range(6)
        ]
        assert engine._validate_response_quality(invalid_blocks) == False


class TestQualityValidator:
    """Tests für QualityValidator"""

    def test_quality_score_calculation(self):
        """Test: Quality Score wird korrekt berechnet"""
        validator = QualityValidator()

        blocks = [
            InfoBlock(
                content="Test. Content.",
                block_type=BlockType.FOUNDATION,
                sentence_count=2,
            ),
            InfoBlock(
                content="More test. Content.",
                block_type=BlockType.CONNECTION,
                sentence_count=2,
            ),
        ]

        score = validator._calculate_quality_score(blocks)
        assert score >= 0.8  # Sollte hohen Score haben

    def test_validation_catches_too_many_blocks(self):
        """Test: Validator erkennt zu viele Blocks"""
        validator = QualityValidator()

        # Erstelle 6 Blocks (zu viele)
        blocks = [InfoBlock(f"Block {i}.", BlockType.FOUNDATION, 1) for i in range(6)]

        results = validator.validate_response(blocks)
        assert any("Too many blocks" in issue for issue in results["issues"])
        assert results["passed"] == False

    def test_validation_catches_too_many_sentences(self):
        """Test: Validator erkennt zu viele Sätze"""
        validator = QualityValidator()

        blocks = [
            InfoBlock(
                content="One. Two. Three. Four.",
                block_type=BlockType.FOUNDATION,
                sentence_count=4,
            ),
            InfoBlock(
                content="Five.", block_type=BlockType.CONNECTION, sentence_count=1
            ),
        ]

        results = validator.validate_response(blocks)
        assert "Blocks exceed 3 sentences" in results["issues"]

    def test_flow_validation(self):
        """Test: Flow-Validierung funktioniert"""
        validator = QualityValidator()

        # Valid flow
        valid_blocks = [
            InfoBlock("Foundation.", BlockType.FOUNDATION, 1),
            InfoBlock("Building.", BlockType.BUILDING, 1),
            InfoBlock("Connection.", BlockType.CONNECTION, 1),
        ]
        assert validator._validate_flow(valid_blocks) == True

        # Invalid flow: no foundation
        invalid_blocks = [
            InfoBlock("Building.", BlockType.BUILDING, 1),
            InfoBlock("Connection.", BlockType.CONNECTION, 1),
        ]
        assert validator._validate_flow(invalid_blocks) == False

        # Invalid flow: no connection
        invalid_blocks2 = [
            InfoBlock("Foundation.", BlockType.FOUNDATION, 1),
            InfoBlock("Building.", BlockType.BUILDING, 1),
        ]
        assert validator._validate_flow(invalid_blocks2) == False

    def test_comprehensive_validation(self):
        """Test: Comprehensive Validation gibt korrektes Ergebnis"""
        validator = QualityValidator()

        # Perfect blocks
        perfect_blocks = [
            InfoBlock("Foundation content.", BlockType.FOUNDATION, 1, True, "Next"),
            InfoBlock("Building content.", BlockType.BUILDING, 1, True, "Next"),
            InfoBlock("Connection content.", BlockType.CONNECTION, 1, False, None),
        ]

        results = validator.validate_response(perfect_blocks)
        assert results["passed"] == True
        assert results["metrics"]["quality_score"] >= 369 / 370
        assert len(results["issues"]) == 0


class TestBlockFormatter:
    """Tests für BlockFormatter"""

    def test_formatter_initialization(self):
        """Test: Formatter initialisiert korrekt"""
        formatter = BlockFormatter()
        assert formatter.style == "minimal"
        assert BlockType.FOUNDATION in formatter.block_icons

    def test_format_response(self):
        """Test: Response wird formatiert"""
        formatter = BlockFormatter()
        blocks = [
            InfoBlock("Foundation.", BlockType.FOUNDATION, 1),
            InfoBlock("Connection.", BlockType.CONNECTION, 1),
        ]

        formatted = formatter.format_response(blocks)
        assert "LUCA 369/370 Response" in formatted
        assert "FOUNDATION" in formatted
        assert "CONNECTION" in formatted
        assert "Response complete" in formatted

    def test_format_for_web(self):
        """Test: Web-Format wird korrekt generiert"""
        formatter = BlockFormatter()
        blocks = [
            InfoBlock("Foundation.", BlockType.FOUNDATION, 1),
            InfoBlock("Connection.", BlockType.CONNECTION, 1),
        ]

        web_format = formatter.format_for_web(blocks)

        assert "blocks" in web_format
        assert "total_blocks" in web_format
        assert "quality_score" in web_format
        assert len(web_format["blocks"]) == 2
        assert web_format["total_blocks"] == 2

    def test_single_block_formatting(self):
        """Test: Einzelner Block wird korrekt formatiert"""
        formatter = BlockFormatter()
        block = InfoBlock(
            "Test content.", BlockType.FOUNDATION, 1, True, "Next block hint"
        )

        formatted = formatter._format_single_block(block, 1, 3)
        assert "Block 1/3" in formatted
        assert "FOUNDATION" in formatted
        assert "Test content." in formatted
        assert "Next block hint" in formatted


class TestIntegration:
    """Integration Tests für das gesamte System"""

    def test_full_pipeline(self):
        """Test: Vollständiger Pipeline-Test"""
        # 1. Engine erstellen
        engine = InfoBlockEngine()

        # 2. Response generieren
        blocks = engine.generate_response("Test query")

        # 3. Formatieren
        formatter = BlockFormatter()
        formatted = formatter.format_response(blocks)
        assert len(formatted) > 0

        # 4. Validieren
        validator = QualityValidator()
        results = validator.validate_response(blocks)
        assert results["passed"] == True

    def test_quality_standard_369_370(self):
        """Test: 369/370 Standard wird eingehalten"""
        engine = InfoBlockEngine()
        validator = QualityValidator()

        # Generate multiple responses and check quality
        for i in range(5):
            blocks = engine.generate_response(f"Test query {i}")
            results = validator.validate_response(blocks)

            # Should always meet 369/370 standard
            assert results["metrics"]["quality_score"] >= 369 / 370


# Pytest Konfiguration
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
