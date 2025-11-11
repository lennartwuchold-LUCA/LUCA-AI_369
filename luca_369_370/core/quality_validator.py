"""
LUCA 369/370 - Quality Validator
Validiert alle Outputs gegen den 369/370 Standard

Lennart's Brauwesen-Präzision trifft KI
"""

from typing import Dict, List

from .info_block_engine import BlockType, InfoBlock


class QualityValidator:
    """
    Validiert LUCA-Outputs gegen multiple Qualitätskriterien
    """

    def __init__(self):
        self.quality_threshold = 369 / 370
        self.metrics = {
            "block_count": 0,
            "sentence_distribution": [],
            "flow_score": 0.0,
            "overall_quality": 0.0,
        }

    def validate_response(self, blocks: List[InfoBlock]) -> Dict:
        """
        Comprehensive Quality Check

        Returns:
            Dict mit Validierungs-Ergebnissen und Metriken
        """
        results = {"passed": False, "metrics": {}, "issues": [], "recommendations": []}

        # 1. Block Count Check
        if len(blocks) > 5:
            results["issues"].append("Too many blocks (max 5)")

        # 2. Sentence Distribution
        sentence_counts = [b.sentence_count for b in blocks]
        if any(count > 3 for count in sentence_counts):
            results["issues"].append("Blocks exceed 3 sentences")

        # 3. Flow Check
        flow_valid = self._validate_flow(blocks)
        if not flow_valid:
            results["issues"].append("Invalid block flow")

        # 4. Calculate Overall Quality
        quality_score = self._calculate_quality_score(blocks)
        results["metrics"]["quality_score"] = quality_score
        results["metrics"]["block_count"] = len(blocks)
        results["metrics"]["avg_sentences"] = (
            sum(sentence_counts) / len(sentence_counts) if sentence_counts else 0
        )

        # 5. Final Verdict
        results["passed"] = (
            quality_score >= self.quality_threshold and len(results["issues"]) == 0
        )

        return results

    def _validate_flow(self, blocks: List[InfoBlock]) -> bool:
        """
        Validiert den Flow: Foundation → Building → Connection
        """
        if len(blocks) < 2:
            return False

        # Erster Block muss Foundation sein
        if blocks[0].block_type != BlockType.FOUNDATION:
            return False

        # Letzter Block muss Connection sein
        if blocks[-1].block_type != BlockType.CONNECTION:
            return False

        return True

    def _calculate_quality_score(self, blocks: List[InfoBlock]) -> float:
        """
        Berechnet Gesamt-Qualitätsscore

        Faktoren:
        - Block-Validierung (50%)
        - Flow-Korrektheit (30%)
        - Sentence-Distribution (20%)
        """
        if not blocks:
            return 0.0

        valid_blocks = sum(1 for b in blocks if b.validate_quality())
        block_score = valid_blocks / len(blocks)

        flow_score = 1.0 if self._validate_flow(blocks) else 0.0

        sentence_counts = [b.sentence_count for b in blocks]
        avg_sentences = sum(sentence_counts) / len(sentence_counts)
        sentence_score = 1.0 if avg_sentences <= 3 else 0.5

        total_score = block_score * 0.5 + flow_score * 0.3 + sentence_score * 0.2

        return total_score
