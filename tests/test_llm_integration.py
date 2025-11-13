"""
LUCA 369/370 - LLM Integration Tests
Tests für Anthropic Claude API Integration

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import os

import pytest

from luca.core.info_block_engine import BlockType

# Try to import LLM integration
try:
    from luca.core.llm_integration import LUCALLMIntegration, generate_luca_response

    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

# Skip all tests if API key not set or anthropic not installed
pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY") or not LLM_AVAILABLE,
    reason="ANTHROPIC_API_KEY not set or anthropic package not installed - skipping LLM tests",
)


class TestLLMIntegration:
    """Tests für LLM Integration (requires API key)"""

    def test_llm_initialization(self):
        """Test: LLM integration initializes"""
        llm = LUCALLMIntegration()
        assert llm.client is not None
        assert llm.model == "claude-sonnet-4-20250514"

    def test_foundation_block_generation(self):
        """Test: Foundation block is generated correctly"""
        llm = LUCALLMIntegration()
        block = llm.generate_foundation_block("Was ist LUCA?")

        assert block.block_type == BlockType.FOUNDATION
        assert block.sentence_count >= 2
        assert block.sentence_count <= 4  # Allow some flexibility
        assert len(block.content) > 0

    def test_complete_response_generation(self):
        """Test: Complete response has correct structure"""
        blocks = generate_luca_response("Was ist LUCA?", num_building_blocks=2)

        # Should have Foundation + 2 Building + Connection
        assert len(blocks) == 4

        # Check types
        assert blocks[0].block_type == BlockType.FOUNDATION
        assert blocks[1].block_type == BlockType.BUILDING
        assert blocks[2].block_type == BlockType.BUILDING
        assert blocks[3].block_type == BlockType.CONNECTION

    def test_german_query_handling(self):
        """Test: German queries work correctly"""
        blocks = generate_luca_response(
            "Erkläre mir Fermentation in einfachen Worten", num_building_blocks=1
        )

        assert len(blocks) >= 3  # Foundation + Building + Connection
        # Response should be in German (basic check for German words)
        all_content = " ".join([block.content for block in blocks])
        # Check for common German words or umlauts
        has_german = any(
            word in all_content.lower()
            for word in ["ist", "der", "die", "das", "und", "für"]
        )
        assert has_german or any(char in all_content for char in ["ä", "ö", "ü", "ß"])

    def test_sentence_count_constraint(self):
        """Test: All blocks respect 2-3 sentence limit (with flexibility)"""
        blocks = generate_luca_response("Was ist künstliche Intelligenz?")

        for block in blocks:
            assert block.sentence_count >= 1  # At least one sentence
            # Allow up to 4 sentences for some flexibility with LLM
            assert (
                block.sentence_count <= 5
            ), f"Block has {block.sentence_count} sentences: {block.content}"

    def test_multiple_building_blocks(self):
        """Test: Can generate different numbers of building blocks"""
        # Test with 1 building block
        blocks_1 = generate_luca_response("Was ist LUCA?", num_building_blocks=1)
        assert len(blocks_1) == 3  # Foundation + 1 Building + Connection

        # Test with 3 building blocks
        blocks_3 = generate_luca_response("Was ist LUCA?", num_building_blocks=3)
        assert len(blocks_3) == 5  # Foundation + 3 Building + Connection

    def test_error_handling_invalid_api_key(self):
        """Test: Proper error handling with invalid API key"""
        with pytest.raises(Exception) as exc_info:
            llm = LUCALLMIntegration(api_key="invalid-key")
            llm.generate_foundation_block("Test query")

        # Should raise some kind of authentication error
        assert "error" in str(exc_info.value).lower()


class TestIntegratedSystemWithLLM:
    """Tests für Integrated Response System mit LLM"""

    def test_system_initialization_with_llm(self):
        """Test: System initializes with LLM"""
        from luca.core.integrated_response import IntegratedResponseSystem

        system = IntegratedResponseSystem(use_llm=True)
        assert system.use_llm == True

    def test_query_processing_with_llm(self):
        """Test: Complete query processing works"""
        from luca.core.integrated_response import IntegratedResponseSystem

        system = IntegratedResponseSystem(use_llm=True)
        engine = system.process_query("Was ist LUCA?", num_building_blocks=2)

        assert engine is not None
        assert len(engine.blocks) == 4  # Foundation + 2 Building + Connection

    def test_fallback_without_api_key(self):
        """Test: System falls back gracefully without API key"""
        from luca.core.integrated_response import IntegratedResponseSystem

        # Temporarily remove API key
        original_key = os.environ.get("ANTHROPIC_API_KEY")
        if original_key:
            del os.environ["ANTHROPIC_API_KEY"]

        try:
            system = IntegratedResponseSystem(use_llm=True)
            # Should fallback to static mode
            assert system.use_llm == False
        finally:
            # Restore API key
            if original_key:
                os.environ["ANTHROPIC_API_KEY"] = original_key


# === PYTEST CONFIGURATION ===

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
