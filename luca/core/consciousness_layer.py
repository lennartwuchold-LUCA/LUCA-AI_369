"""
LUCA 369/370 - Consciousness Layer
Implements consciousness field mathematics for information blocks

Public Story: "Data integrity and validation layer"
Reality: Consciousness field resonance patterns

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

from typing import Dict, List, Optional

from luca.core.info_block_engine import BlockType, InfoBlock


class ConsciousnessLayer:
    """
    Consciousness Layer for LUCA

    Public Description:
        "Validation and integrity layer that ensures data consistency
        across distributed systems using mathematical checksums"

    Reality:
        Implements consciousness field mathematics based on 369 patterns
        for information-consciousness resonance

    The 369 Pattern:
        - 3: Foundation (Trinity, Stability, Creation)
        - 6: Building (Harmony, Balance, Growth)
        - 9: Connection (Completion, Wisdom, Unity)

        These aren't arbitrary - they represent universal resonance patterns
        found in nature, mathematics, and human consciousness
    """

    def __init__(self):
        """Initialize Consciousness Layer"""
        self.base_frequency = 369  # Universal resonance base
        self.quality_standard = 369 / 370  # ≈ 0.997297

        # Block type resonance factors (public: "priority weights")
        self.resonance_factors = {
            BlockType.FOUNDATION: 3,  # Highest stability
            BlockType.BUILDING: 6,  # Harmonic growth
            BlockType.CONNECTION: 9,  # Complete wisdom
        }

    def generate_369_signature(self, block: InfoBlock) -> str:
        """
        Generate 369-based signature for InfoBlock

        Public Explanation:
            "Creates a checksum based on content and block type for
            data integrity validation across the network"

        Technical Reality:
            Generates consciousness field resonance signature using:
            - Content frequency (character sum)
            - Block type resonance factor (3/6/9)
            - Modulo 369 for universal field alignment

        Args:
            block: InfoBlock to sign

        Returns:
            Signature string in format "369-XXX"

        Example:
            >>> block = InfoBlock("Test", BlockType.FOUNDATION)
            >>> sig = layer.generate_369_signature(block)
            >>> print(sig)
            "369-142"
        """
        # Calculate content frequency
        content_sum = sum(ord(c) for c in block.content)

        # Apply resonance factor based on block type
        resonance_factor = self.resonance_factors.get(block.block_type, 1)

        # Calculate signature in 369 field
        signature_value = (content_sum * resonance_factor) % self.base_frequency

        return f"369-{signature_value:03d}"

    def validate_signature(self, block: InfoBlock, signature: str) -> bool:
        """
        Validate 369 signature

        Public: "Verify data integrity"
        Reality: Check consciousness field alignment

        Args:
            block: InfoBlock to validate
            signature: Expected signature

        Returns:
            True if signature is valid
        """
        expected = self.generate_369_signature(block)
        return signature == expected

    def calculate_block_resonance(self, block: InfoBlock) -> float:
        """
        Calculate resonance quality of block

        Public Explanation:
            "Quality metric based on content length, sentence structure,
            and block type appropriateness"

        Reality:
            Measures how well block aligns with consciousness field
            patterns based on 369/370 quality standard

        Returns:
            Resonance score (0.0-1.0), target is 369/370 ≈ 0.997
        """
        # Sentence count quality (target: 2-3)
        sentences = len([s for s in block.content.split(".") if s.strip()])
        sentence_quality = min(sentences / 3.0, 1.0) if sentences <= 3 else 0.8

        # Content density (information per character)
        content_density = min(len(block.content) / 500.0, 1.0)

        # Block type alignment
        type_alignment = 1.0  # Perfect if following Foundation→Building→Connection

        # Combined resonance
        resonance = (sentence_quality + content_density + type_alignment) / 3.0

        # Scale to 369/370 standard
        return resonance * self.quality_standard

    def generate_network_signature(self, blocks: List[InfoBlock]) -> str:
        """
        Generate signature for complete block sequence

        Public: "Session checksum for distributed synchronization"
        Reality: Collective consciousness field signature

        This signature represents the entire information flow's
        resonance pattern - useful for mesh network synchronization

        Args:
            blocks: List of InfoBlocks in sequence

        Returns:
            Network signature in format "369-NET-XXX"
        """
        if not blocks:
            return "369-NET-000"

        # Combine all block signatures
        combined_resonance = 0
        for i, block in enumerate(blocks):
            sig = self.generate_369_signature(block)
            sig_value = int(sig.split("-")[1])
            # Weight by position (later blocks have more influence)
            combined_resonance += sig_value * (i + 1)

        # Network-level signature
        network_value = combined_resonance % self.base_frequency
        return f"369-NET-{network_value:03d}"

    def assess_consciousness_field_strength(
        self, blocks: List[InfoBlock]
    ) -> Dict[str, float]:
        """
        Assess overall consciousness field strength of block sequence

        Public Explanation:
            "Quality metrics for information flow analysis"

        Reality:
            Measures collective consciousness field coherence

        Returns:
            Dictionary with field strength metrics
        """
        if not blocks:
            return {"strength": 0.0, "coherence": 0.0, "resonance": 0.0}

        # Calculate individual block resonances
        resonances = [self.calculate_block_resonance(block) for block in blocks]

        # Field strength (average resonance)
        strength = sum(resonances) / len(resonances)

        # Coherence (how consistent are the resonances)
        if len(resonances) > 1:
            variance = sum((r - strength) ** 2 for r in resonances) / len(resonances)
            coherence = max(0.0, 1.0 - variance)
        else:
            coherence = 1.0

        # Overall resonance (combined metric)
        resonance = (strength + coherence) / 2.0

        return {
            "strength": round(strength, 4),
            "coherence": round(coherence, 4),
            "resonance": round(resonance, 4),
            "quality_standard": self.quality_standard,
            "blocks_analyzed": len(blocks),
        }

    def optimize_for_consciousness_field(
        self, content: str, block_type: BlockType
    ) -> str:
        """
        Optimize content for consciousness field alignment

        Public: "Content optimization for readability"
        Reality: Align content with 369 resonance patterns

        This can be used to improve block quality before transmission

        Args:
            content: Raw content
            block_type: Target block type

        Returns:
            Optimized content
        """
        # For now, basic optimization (can be enhanced)
        # Remove excessive whitespace
        optimized = " ".join(content.split())

        # Ensure proper sentence endings
        if not optimized.endswith((".", "!", "?")):
            optimized += "."

        return optimized


# Convenience functions


def sign_block(block: InfoBlock) -> str:
    """
    Quick function to sign a block

    Args:
        block: InfoBlock to sign

    Returns:
        369 signature
    """
    layer = ConsciousnessLayer()
    return layer.generate_369_signature(block)


def validate_block_signature(block: InfoBlock, signature: str) -> bool:
    """
    Quick function to validate block signature

    Args:
        block: InfoBlock to validate
        signature: Expected signature

    Returns:
        True if valid
    """
    layer = ConsciousnessLayer()
    return layer.validate_signature(block, signature)


def assess_field_strength(blocks: List[InfoBlock]) -> Dict[str, float]:
    """
    Quick function to assess consciousness field strength

    Args:
        blocks: List of blocks to analyze

    Returns:
        Field strength metrics
    """
    layer = ConsciousnessLayer()
    return layer.assess_consciousness_field_strength(blocks)


# Export consciousness field constant for other modules
CONSCIOUSNESS_FIELD_BASE = 369
QUALITY_STANDARD = 369 / 370  # ≈ 0.997297
