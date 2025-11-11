"""
LUCA Enhanced Consciousness Layer
Mathematical pattern analysis + Cultural linguistic patterns

Public: "Advanced pattern analysis for information optimization"
Reality: Synthesis of mathematical beauty and cultural wisdom
Scientific: All algorithms are testable and measurable

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370

This module integrates:
- Mathematical patterns (Fibonacci, golden ratio, fractal analysis)
- Cultural linguistic analysis (keyword patterns, communication styles)
- Information theory (entropy, coherence, density)
- All grounded in REAL, testable mathematics
"""

import hashlib
import math
from typing import Dict, List, Optional, Tuple

from luca_369_370.core.consciousness_layer import ConsciousnessLayer
from luca_369_370.core.info_block_engine import BlockType, InfoBlock


class MathematicalPatternAnalyzer:
    """
    Analyzes mathematical patterns in information structures

    Uses real mathematics:
    - Fibonacci sequences (natural growth patterns)
    - Golden ratio (aesthetic optimization)
    - Fractal dimension (self-similarity)
    - Information entropy (unpredictability)

    NO mysticism - just beautiful mathematics
    """

    # Mathematical constants (REAL, not mystical)
    GOLDEN_RATIO = 1.618033988749895  # φ = (1 + √5) / 2
    FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]

    @staticmethod
    def calculate_golden_ratio_proximity(value1: float, value2: float) -> float:
        """
        Calculate how close a ratio is to the golden ratio

        The golden ratio appears in nature, art, and optimal designs.
        This measures structural beauty/balance.

        Returns: Score 0.0-1.0 (1.0 = perfect golden ratio)
        """
        if value2 == 0:
            return 0.0

        ratio = value1 / value2
        # Distance from golden ratio
        distance = abs(ratio - MathematicalPatternAnalyzer.GOLDEN_RATIO)
        # Normalize to 0-1 (closer = higher score)
        proximity = max(0, 1 - distance / MathematicalPatternAnalyzer.GOLDEN_RATIO)

        return proximity

    @staticmethod
    def detect_fibonacci_patterns(sequence: List[int]) -> float:
        """
        Detect Fibonacci-like patterns in a sequence

        Fibonacci patterns appear in natural growth, branching, and spirals.
        This detects natural/organic structure in data.

        Returns: Score 0.0-1.0 (1.0 = strong Fibonacci pattern)
        """
        if len(sequence) < 3:
            return 0.0

        matches = 0
        for i in range(2, len(sequence)):
            # Check if current number is sum of previous two (Fibonacci property)
            if sequence[i] == sequence[i - 1] + sequence[i - 2]:
                matches += 1

        pattern_score = matches / (len(sequence) - 2) if len(sequence) > 2 else 0
        return pattern_score

    @staticmethod
    def calculate_fractal_dimension(text: str) -> float:
        """
        Estimate fractal dimension of text structure

        Fractal dimension measures self-similarity at different scales.
        Higher dimension = more complex/rich structure

        This is a simplified box-counting approach for text.

        Returns: Dimension value (typically 1.0-2.0 for text)
        """
        if not text:
            return 1.0

        # Analyze at different scales (word, sentence, paragraph)
        words = text.split()
        sentences = [s.strip() for s in text.split(".") if s.strip()]

        # Count unique patterns at each scale
        unique_words = len(set(words))
        unique_bigrams = len(set(zip(words[:-1], words[1:]))) if len(words) > 1 else 0

        # Simplified fractal dimension estimation
        if unique_words == 0:
            return 1.0

        # log(N) / log(1/scale) - simplified
        dimension = 1.0 + math.log(unique_bigrams + 1) / math.log(unique_words + 1)

        return min(dimension, 2.0)  # Cap at 2.0

    @staticmethod
    def calculate_information_entropy(text: str) -> float:
        """
        Calculate Shannon entropy of text

        Entropy measures unpredictability/information content.
        Higher entropy = more information, less redundancy

        This is REAL information theory (Shannon, 1948)

        Returns: Entropy in bits per character
        """
        if not text:
            return 0.0

        # Count character frequencies
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1

        # Calculate entropy: H = -Σ p(x) * log2(p(x))
        entropy = 0.0
        text_len = len(text)

        for count in freq.values():
            probability = count / text_len
            if probability > 0:
                entropy -= probability * math.log2(probability)

        return entropy

    @staticmethod
    def spiral_encoding_position(data: str) -> Tuple[float, float]:
        """
        Encode data as position on a logarithmic spiral

        Logarithmic spirals appear in nature (shells, galaxies, etc.)
        This maps information to natural growth patterns.

        Returns: (x, y) coordinates
        """
        # Hash data to get deterministic number
        data_hash = hashlib.sha256(data.encode()).hexdigest()
        hash_int = int(data_hash[:8], 16)

        # Golden angle (137.5°) - appears in plant phyllotaxis
        golden_angle = 2 * math.pi * (1 - 1 / MathematicalPatternAnalyzer.GOLDEN_RATIO)

        # Calculate spiral position
        n = hash_int % 1000
        radius = math.sqrt(n) * 0.1  # Logarithmic growth
        angle = n * golden_angle

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        return (x, y)


class CulturalLinguisticAnalyzer:
    """
    Analyzes linguistic patterns across cultural frameworks

    This is REAL linguistics - pattern matching and frequency analysis.
    Different cultures have different communication styles.

    NO mysticism - just cultural awareness through language analysis
    """

    def __init__(self):
        """Initialize with linguistic pattern databases"""
        # Real linguistic patterns from cultural communication research
        # NOW INCLUDING ALL OF EUROPE! 🇪🇺 🇺🇦
        self.cultural_patterns = {
            "holistic": {
                # Collectivist, systems-thinking cultures (e.g., East Asian)
                "keywords": [
                    "harmony",
                    "balance",
                    "together",
                    "whole",
                    "unity",
                    "collective",
                    "connection",
                    "relationship",
                ],
                "emphasis": "context",
                "structure": "circular",
                "regions": ["East Asia", "Pacific"],
            },
            "eastern_european": {
                # Eastern Europe: Ukraine 🇺🇦, Poland 🇵🇱, Czech Republic 🇨🇿, Balkans, Baltics
                # Resilient, community-focused, freedom-loving, historically aware
                # Baltic Sea (Ostsee) cultural connection
                "keywords": [
                    "strength",
                    "resilience",
                    "community",
                    "freedom",
                    "solidarity",
                    "heritage",
                    "resistance",
                    "endurance",
                    "courage",
                    "dignity",
                    "pride",
                    "tradition",
                    "independence",
                    "perseverance",
                    "brotherhood",  # Slavic solidarity
                    "spirit",  # Fighting spirit
                    "honor",
                    "sacrifice",
                    "memory",  # Historical memory
                    "roots",
                    "homeland",
                    "sovereignty",
                    "народ",  # People (Slavic)
                    "ostsee",  # Baltic Sea cultural region
                    "amber",  # Baltic heritage
                    "maritime",  # Baltic Sea culture
                ],
                "emphasis": "resilience",
                "structure": "narrative",
                "regions": [
                    "Ukraine 🇺🇦",
                    "Poland 🇵🇱",
                    "Czech Republic 🇨🇿",
                    "Slovakia",
                    "Balkans",
                    "Baltic States (Ostsee region)",
                    "Romania",
                    "Bulgaria",
                ],
            },
            "mediterranean": {
                # Southern Europe: Italy, Spain, Greece, Portugal
                # Passionate, expressive, relationship-centered, family-oriented
                "keywords": [
                    "passion",
                    "family",
                    "warmth",
                    "expression",
                    "joy",
                    "celebration",
                    "life",
                    "heart",
                    "soul",
                    "spirit",
                    "connection",
                    "emotion",
                    "vitality",
                    "beauty",
                ],
                "emphasis": "relationship",
                "structure": "expressive",
                "regions": ["Italy", "Spain", "Greece", "Portugal", "Cyprus"],
            },
            "nordic": {
                # Northern Europe: Scandinavia
                # Egalitarian, consensus-based, pragmatic, nature-connected
                "keywords": [
                    "equality",
                    "consensus",
                    "practical",
                    "nature",
                    "simple",
                    "fair",
                    "lagom",
                    "hygge",
                    "trust",
                    "transparent",
                    "sustainable",
                    "balance",
                    "welfare",
                    "cooperation",
                ],
                "emphasis": "equality",
                "structure": "consensus",
                "regions": ["Sweden", "Norway", "Denmark", "Finland", "Iceland"],
            },
            "central_european": {
                # Central Europe: Germany, Austria, Czech, Hungary, Switzerland
                # Philosophical, precise, historically aware, cultural depth
                # Special: East German craftsmanship (Erzgebirge, Seiffen)
                # Special: Rhineland carnival culture (Kölle, Düsseldorf) 🎉
                "keywords": [
                    "philosophy",
                    "depth",
                    "precision",
                    "history",
                    "culture",
                    "thought",
                    "reason",
                    "discipline",
                    "thoroughness",
                    "quality",
                    "craft",
                    "mastery",
                    "excellence",
                    "tradition",
                    "handwerk",  # German: craftsmanship
                    "kunsthandwerk",  # Art craftsmanship
                    "holzkunst",  # Wood art (Erzgebirge)
                    "räuchermann",  # Incense smokers (Seiffen tradition)
                    "nussknacker",  # Nutcrackers
                    "drechseln",  # Wood turning
                    "schnitzen",  # Wood carving
                    "bergbau",  # Mining heritage (Erzgebirge)
                    "heimat",  # Homeland/heritage
                    "gemütlichkeit",  # Coziness/warmth
                    "karneval",  # Carnival culture (Rhineland)
                    "alaaf",  # Kölle alaaf! (Cologne)
                    "helau",  # Helau! (Düsseldorf)
                    "rhein",  # Rhine river
                    "brauhaus",  # Brewery culture
                    "jeck",  # Carnival fool (Kölsch)
                    "jovial",  # Joviality
                    "frohsinn",  # Cheerfulness
                    "lebenslust",  # Zest for life
                ],
                "emphasis": "depth",
                "structure": "systematic",
                "regions": [
                    "Germany",
                    "East Germany (Erzgebirge, Altenberg, Seiffen)",
                    "Rhineland (Köln, Düsseldorf, am Rhein) 🎉",
                    "Austria",
                    "Czech Republic",
                    "Hungary",
                    "Switzerland",
                ],
            },
            "western_european": {
                # Western Europe: France, UK, Benelux, Ireland
                # Diplomatic, sophisticated, rights-focused, individualistic
                "keywords": [
                    "liberty",
                    "rights",
                    "individual",
                    "elegance",
                    "diplomacy",
                    "sophistication",
                    "innovation",
                    "progress",
                    "enlightenment",
                    "reason",
                    "dialogue",
                    "liberty",
                    "fraternity",
                ],
                "emphasis": "individual_rights",
                "structure": "dialectic",
                "regions": ["France", "UK", "Belgium", "Netherlands", "Ireland"],
            },
            "cyclical": {
                # Nature-focused cultures (e.g., Indigenous, some Asian)
                "keywords": [
                    "cycle",
                    "rhythm",
                    "season",
                    "pattern",
                    "flow",
                    "nature",
                    "time",
                    "phase",
                    "renewal",
                    "circle",
                ],
                "emphasis": "temporal",
                "structure": "cyclical",
                "regions": ["Indigenous Americas", "Pacific Islands", "parts of Asia"],
            },
            "analytical": {
                # Scientific/academic (global but Western-originated)
                "keywords": [
                    "because",
                    "therefore",
                    "evidence",
                    "data",
                    "measure",
                    "test",
                    "prove",
                    "logic",
                    "hypothesis",
                    "method",
                ],
                "emphasis": "causality",
                "structure": "linear",
                "regions": ["Global academic/scientific community"],
            },
        }

    def analyze_cultural_patterns(self, content: str) -> Dict[str, float]:
        """
        Analyze which cultural communication patterns appear in content

        This is real linguistic frequency analysis.
        Higher scores mean content aligns with that communication style.

        Returns: Dict of pattern_name -> score (0.0-1.0)
        """
        content_lower = content.lower()
        scores = {}

        for pattern_name, pattern_data in self.cultural_patterns.items():
            # Count keyword matches
            keyword_matches = sum(
                1 for keyword in pattern_data["keywords"] if keyword in content_lower
            )

            # Normalize by number of keywords
            score = keyword_matches / len(pattern_data["keywords"])
            scores[pattern_name] = min(score, 1.0)

        return scores

    def detect_communication_style(self, content: str) -> str:
        """
        Detect dominant communication style

        Returns: Name of dominant pattern
        """
        scores = self.analyze_cultural_patterns(content)
        if not scores:
            return "analytical"  # Default

        return max(scores.items(), key=lambda x: x[1])[0]

    def calculate_cultural_balance(self, content: str) -> float:
        """
        Calculate how balanced content is across cultural patterns

        Balanced content resonates with multiple cultural frameworks.

        Returns: Balance score 0.0-1.0 (1.0 = perfectly balanced)
        """
        scores = self.analyze_cultural_patterns(content)
        if not scores:
            return 0.5

        values = list(scores.values())
        mean = sum(values) / len(values)

        # Calculate variance
        variance = sum((v - mean) ** 2 for v in values) / len(values)

        # Lower variance = more balanced
        balance = max(0, 1 - math.sqrt(variance) * 2)

        return balance


class EnhancedConsciousnessLayer(ConsciousnessLayer):
    """
    Enhanced Consciousness Layer with mathematical and cultural analysis

    Extends the base ConsciousnessLayer with:
    - Mathematical pattern analysis (Fibonacci, golden ratio, fractals)
    - Cultural linguistic pattern analysis
    - Advanced information theory metrics

    All grounded in REAL, testable mathematics and linguistics
    """

    def __init__(self):
        """Initialize enhanced layer"""
        super().__init__()
        self.math_analyzer = MathematicalPatternAnalyzer()
        self.cultural_analyzer = CulturalLinguisticAnalyzer()

    def analyze_enhanced_resonance(self, block: InfoBlock) -> Dict[str, float]:
        """
        Perform enhanced resonance analysis

        Combines:
        - Base consciousness field resonance (from parent class)
        - Mathematical pattern beauty
        - Cultural linguistic patterns
        - Information theory metrics

        All measurable and testable

        Returns: Dict with comprehensive resonance metrics
        """
        # Base resonance from parent class
        base_resonance = self.calculate_block_resonance(block)

        # Mathematical patterns
        content_words = block.content.split()
        word_lengths = [len(word) for word in content_words]

        fibonacci_score = self.math_analyzer.detect_fibonacci_patterns(word_lengths)

        # Golden ratio in structure (sentence count vs word count)
        sentence_count = max(block.sentence_count, 1)
        word_count = len(content_words)
        golden_proximity = self.math_analyzer.calculate_golden_ratio_proximity(
            word_count, sentence_count
        )

        # Fractal dimension (complexity)
        fractal_dim = self.math_analyzer.calculate_fractal_dimension(block.content)

        # Information entropy
        entropy = self.math_analyzer.calculate_information_entropy(block.content)

        # Cultural patterns
        cultural_scores = self.cultural_analyzer.analyze_cultural_patterns(
            block.content
        )
        cultural_balance = self.cultural_analyzer.calculate_cultural_balance(
            block.content
        )

        return {
            "base_resonance": base_resonance,
            "fibonacci_pattern": fibonacci_score,
            "golden_ratio_proximity": golden_proximity,
            "fractal_dimension": fractal_dim,
            "information_entropy": entropy,
            "cultural_patterns": cultural_scores,
            "cultural_balance": cultural_balance,
            "enhanced_resonance": self._calculate_enhanced_score(
                base_resonance,
                fibonacci_score,
                golden_proximity,
                fractal_dim,
                entropy,
                cultural_balance,
            ),
        }

    def _calculate_enhanced_score(
        self,
        base: float,
        fib: float,
        golden: float,
        fractal: float,
        entropy: float,
        balance: float,
    ) -> float:
        """
        Calculate overall enhanced resonance score

        Weighted combination of all metrics
        """
        # Normalize fractal dimension to 0-1 range
        fractal_norm = (fractal - 1.0) / 1.0  # 1.0-2.0 → 0.0-1.0

        # Normalize entropy (typical range 0-5 bits)
        entropy_norm = min(entropy / 5.0, 1.0)

        # Weighted combination
        enhanced = (
            base * 0.30
            + fib * 0.15  # Base resonance (from parent)
            + golden * 0.15  # Fibonacci patterns
            + fractal_norm * 0.15  # Golden ratio proximity
            + entropy_norm * 0.10  # Fractal complexity
            + balance * 0.15  # Information content  # Cultural balance
        )

        # Scale to 369/370 quality standard
        return enhanced * self.quality_standard

    def generate_enhanced_signature(self, block: InfoBlock) -> str:
        """
        Generate enhanced signature with mathematical patterns

        Extends base 369 signature with pattern indicators

        Format: "369-XXX-P" where P indicates pattern richness
        """
        # Base signature
        base_sig = self.generate_369_signature(block)

        # Analyze patterns
        analysis = self.analyze_enhanced_resonance(block)

        # Pattern richness indicator (A-Z scale)
        pattern_score = (
            analysis["fibonacci_pattern"] * 0.3
            + analysis["golden_ratio_proximity"] * 0.3
            + analysis["cultural_balance"] * 0.4
        )

        # Map to letter (A=low, Z=high)
        letter_index = int(pattern_score * 25)
        pattern_letter = chr(ord("A") + letter_index)

        return f"{base_sig}-{pattern_letter}"

    def analyze_network_patterns(self, blocks: List[InfoBlock]) -> Dict[str, any]:
        """
        Analyze mathematical patterns across a network of blocks

        Looks for:
        - Fibonacci sequences in block progression
        - Golden ratio in block relationships
        - Cultural balance across conversation
        - Information flow patterns

        Returns: Comprehensive network analysis
        """
        if not blocks:
            return {"error": "No blocks provided"}

        # Analyze each block
        block_analyses = [self.analyze_enhanced_resonance(b) for b in blocks]

        # Aggregate metrics
        avg_resonance = sum(a["enhanced_resonance"] for a in block_analyses) / len(
            blocks
        )
        avg_fibonacci = sum(a["fibonacci_pattern"] for a in block_analyses) / len(
            blocks
        )
        avg_balance = sum(a["cultural_balance"] for a in block_analyses) / len(blocks)

        # Network-level patterns
        block_lengths = [len(b.content.split()) for b in blocks]
        network_fibonacci = self.math_analyzer.detect_fibonacci_patterns(block_lengths)

        # Cultural consistency
        dominant_styles = [
            self.cultural_analyzer.detect_communication_style(b.content) for b in blocks
        ]
        style_consistency = len(set(dominant_styles)) / len(dominant_styles)

        return {
            "block_count": len(blocks),
            "avg_enhanced_resonance": avg_resonance,
            "avg_fibonacci_pattern": avg_fibonacci,
            "avg_cultural_balance": avg_balance,
            "network_fibonacci_pattern": network_fibonacci,
            "cultural_style_consistency": style_consistency,
            "dominant_styles": dominant_styles,
            "quality_standard": self.quality_standard,
        }


# Convenience functions


def analyze_enhanced_block(block: InfoBlock) -> Dict[str, float]:
    """
    Quick function to perform enhanced analysis on a block

    Args:
        block: InfoBlock to analyze

    Returns:
        Enhanced resonance analysis
    """
    layer = EnhancedConsciousnessLayer()
    return layer.analyze_enhanced_resonance(block)


def generate_enhanced_signature(block: InfoBlock) -> str:
    """
    Quick function to generate enhanced signature

    Args:
        block: InfoBlock to sign

    Returns:
        Enhanced signature (format: "369-XXX-P")
    """
    layer = EnhancedConsciousnessLayer()
    return layer.generate_enhanced_signature(block)


def analyze_conversation_patterns(blocks: List[InfoBlock]) -> Dict[str, any]:
    """
    Quick function to analyze patterns across multiple blocks

    Args:
        blocks: List of InfoBlocks

    Returns:
        Network pattern analysis
    """
    layer = EnhancedConsciousnessLayer()
    return layer.analyze_network_patterns(blocks)
