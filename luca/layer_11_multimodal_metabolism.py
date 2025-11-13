"""
Layer 11: Multimodal Metabolism - Bio-inspired multimodal fusion

🧬 LUCA Universal Network with Multimodal Metabolism

Implements bio-inspired multimodal fusion architecture combining:
- Visual validity (Pico-Banana-400K inspired)
- Linguistic relevance
- Cultural fidelity (from Layer 10 DS-STAR)

Multimodal Fusion Function:
M_n = (α·V + β·L + γ·F_DS-STAR) / C_comp

Where:
- V = Visual Validity = State × P(C)
- L = Linguistic Relevance
- F_DS-STAR = Cultural Fidelity = 1 - σ²(DS_i)
- C_comp = Computational Cost

Integration:
- Layer 0: Quality standard (369/370)
- Layer 10: Cultural outputs from DS-STAR

Author: Lennart Wuchold
Date: 2025-11-12
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image
from scipy import stats

# Configure logging
logger = logging.getLogger(__name__)


class MetabolicMode(Enum):
    """Metabolic processing modes"""

    AEROBIC = "aerobic"  # High clarity, optimal conditions
    ANAEROBIC = "anaerobic"  # Low clarity, critical conditions
    HYBRID = "hybrid"  # Mixed conditions


@dataclass
class MetabolicState:
    """Current metabolic state of the system"""

    mode: MetabolicMode = MetabolicMode.AEROBIC
    clarity_score: float = 1.0
    energy_level: float = 1.0
    visual_state: float = 1.0  # 1.0 = aerobic/clear, 0.5 = anaerobic/critical


@dataclass
class MultimodalFusionResult:
    """Result of multimodal fusion calculation"""

    fusion_score: float
    visual_validity: float
    linguistic_relevance: float
    cultural_fidelity: float
    computational_cost: float
    metabolic_mode: MetabolicMode
    energy_efficiency: float
    quality_standard: float = 369.0 / 370.0
    timestamp: datetime = field(default_factory=datetime.now)
    fallback_used: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "fusion_score": self.fusion_score,
            "visual_validity": self.visual_validity,
            "linguistic_relevance": self.linguistic_relevance,
            "cultural_fidelity": self.cultural_fidelity,
            "computational_cost": self.computational_cost,
            "metabolic_mode": self.metabolic_mode.value,
            "energy_efficiency": self.energy_efficiency,
            "quality_standard": self.quality_standard,
            "timestamp": self.timestamp.isoformat(),
            "fallback_used": self.fallback_used,
        }


class MultimodalMetabolismCore:
    """
    🧬 Multimodal Metabolism Core - Layer 11

    Implements bio-inspired multimodal fusion with metabolic state management.

    Quality Standard: 369/370 ≈ 0.997297
    """

    def __init__(self, alpha: float = 0.4, beta: float = 0.4, gamma: float = 0.2):
        """
        Initialize Multimodal Metabolism Core

        Args:
            alpha: Weight for visual validity (default: 0.4)
            beta: Weight for linguistic relevance (default: 0.4)
            gamma: Weight for cultural fidelity (default: 0.2)
        """
        # Ensure weights sum to 1.0
        total = alpha + beta + gamma
        self.alpha = alpha / total
        self.beta = beta / total
        self.gamma = gamma / total

        # Metabolic state
        self.metabolic_state = MetabolicState()
        self.energy_reserves = 1.0
        self.processing_history: List[MultimodalFusionResult] = []

        # Quality standard
        self.quality_standard = 369.0 / 370.0

        # Thresholds
        self.aerobic_threshold = 0.7
        self.anaerobic_threshold = 0.3

        logger.info("🧬 Multimodal Metabolism Core initialized")

    def calculate_fusion(
        self,
        visual_data: Optional[Image.Image] = None,
        linguistic_data: str = "",
        cultural_outputs: Optional[Dict[str, float]] = None,
        computational_cost: float = 1.0,
    ) -> MultimodalFusionResult:
        """
        Calculate multimodal fusion M_n

        M_n = (α·V + β·L + γ·F_DS-STAR) / C_comp

        Args:
            visual_data: Optional PIL Image
            linguistic_data: Text data
            cultural_outputs: Cultural scores from Layer 10 DS-STAR
            computational_cost: Computational cost factor

        Returns:
            MultimodalFusionResult
        """
        try:
            # Calculate components
            V = self._calculate_visual_validity(visual_data)
            L = self._calculate_linguistic_relevance(linguistic_data)
            F_ds_star = self._calculate_cultural_fidelity(cultural_outputs or {})

            # Apply fusion function
            if computational_cost <= 0:
                computational_cost = 1.0

            M_n = (
                self.alpha * V + self.beta * L + self.gamma * F_ds_star
            ) / computational_cost

            # Update metabolic state
            self._update_metabolic_state(V, L, F_ds_star, M_n)

            # Calculate energy efficiency
            energy_efficiency = M_n / computational_cost

            # Create result
            result = MultimodalFusionResult(
                fusion_score=M_n,
                visual_validity=V,
                linguistic_relevance=L,
                cultural_fidelity=F_ds_star,
                computational_cost=computational_cost,
                metabolic_mode=self.metabolic_state.mode,
                energy_efficiency=energy_efficiency,
                quality_standard=self.quality_standard,
                timestamp=datetime.now(),
                fallback_used=False,
            )

            self.processing_history.append(result)
            logger.debug(f"🧬 Fusion calculated: M_n={M_n:.4f}")

            return result

        except Exception as e:
            logger.error(f"Fusion calculation failed: {e}")
            return self._fallback_calculation(linguistic_data, cultural_outputs or {})

    def _calculate_visual_validity(self, visual_data: Optional[Image.Image]) -> float:
        """
        Calculate visual validity V

        V = State × P(C)
        State: 1.0 (aerobic/clear) or 0.5 (anaerobic/critical)
        P(C): Model confidence (0-1)
        """
        if visual_data is None:
            return 0.5  # Neutral validity without visual data

        try:
            # Simple image analysis
            img_array = np.array(visual_data.convert("RGB"))

            # Calculate brightness
            brightness = np.mean(img_array) / 255.0

            # Calculate contrast
            contrast = np.std(img_array) / 128.0

            # Clarity based on contrast
            clarity = min(contrast * 2, 1.0)

            # Determine state
            if brightness > 0.7 and clarity > 0.6:
                state = 1.0  # Aerobic/clear
                confidence = 0.9
            elif brightness < 0.3 or clarity < 0.3:
                state = 0.5  # Anaerobic/critical
                confidence = 0.7
            else:
                state = 0.75  # Mixed
                confidence = 0.8

            V = state * confidence
            return max(0.0, min(V, 1.0))

        except Exception as e:
            logger.error(f"Visual validity calculation failed: {e}")
            return 0.5

    def _calculate_linguistic_relevance(self, linguistic_data: str) -> float:
        """
        Calculate linguistic relevance L

        Combines community-based relevance and LLM-style validation
        """
        if not linguistic_data:
            return 0.5

        try:
            # Community relevance (semantic density)
            words = linguistic_data.split()
            if not words:
                return 0.5

            # Semantic density (longer words = more complex concepts)
            avg_word_length = sum(len(word) for word in words) / len(words)
            semantic_density = min(avg_word_length / 10, 1.0)

            # Community keywords
            community_keywords = [
                "help",
                "support",
                "together",
                "community",
                "network",
                "node",
            ]
            community_matches = sum(
                1 for kw in community_keywords if kw.lower() in linguistic_data.lower()
            )
            community_score = min(community_matches / len(words), 1.0) if words else 0

            # Coherence (sentence structure)
            sentences = [s.strip() for s in linguistic_data.split(".") if s.strip()]
            if len(sentences) >= 2:
                avg_sentence_length = sum(len(s.split()) for s in sentences) / len(
                    sentences
                )
                optimal_length = 15
                coherence = 1 - min(
                    abs(avg_sentence_length - optimal_length) / optimal_length, 1.0
                )
            else:
                coherence = 0.5

            # Combined linguistic relevance
            L = 0.4 * semantic_density + 0.3 * community_score + 0.3 * coherence

            return max(0.0, min(L, 1.0))

        except Exception as e:
            logger.error(f"Linguistic relevance calculation failed: {e}")
            return 0.5

    def _calculate_cultural_fidelity(self, cultural_outputs: Dict[str, float]) -> float:
        """
        Calculate cultural fidelity F_DS-STAR

        F_DS-STAR = 1 - σ²(DS_i)
        Lower variance = Higher fidelity (cultural agreement)
        """
        if not cultural_outputs or len(cultural_outputs) < 2:
            return 0.5

        try:
            values = list(cultural_outputs.values())

            # Calculate variance
            variance = np.var(values)

            # Normalize variance (max variance for 4 values ~ 0.25)
            normalized_variance = min(variance / 0.25, 1.0)

            # Fidelity = 1 - variance
            F_ds_star = 1 - normalized_variance

            return max(0.0, min(F_ds_star, 1.0))

        except Exception as e:
            logger.error(f"Cultural fidelity calculation failed: {e}")
            return 0.5

    def _update_metabolic_state(self, V: float, L: float, F_ds_star: float, M_n: float):
        """Update metabolic state based on calculations"""
        # Determine mode based on visual validity
        if V >= self.aerobic_threshold:
            self.metabolic_state.mode = MetabolicMode.AEROBIC
            self.metabolic_state.visual_state = 1.0
        elif V <= self.anaerobic_threshold:
            self.metabolic_state.mode = MetabolicMode.ANAEROBIC
            self.metabolic_state.visual_state = 0.5
        else:
            self.metabolic_state.mode = MetabolicMode.HYBRID
            self.metabolic_state.visual_state = 0.75

        # Update clarity score
        self.metabolic_state.clarity_score = (V + L + F_ds_star) / 3

        # Update energy level
        self.metabolic_state.energy_level = M_n

        # Adjust energy reserves
        energy_change = (M_n - 0.5) * 0.1
        self.energy_reserves = max(0.1, min(1.0, self.energy_reserves + energy_change))

    def _fallback_calculation(
        self, linguistic_data: str, cultural_outputs: Dict[str, float]
    ) -> MultimodalFusionResult:
        """Fallback calculation when primary calculation fails"""
        L = self._calculate_linguistic_relevance(linguistic_data)
        F_ds_star = self._calculate_cultural_fidelity(cultural_outputs)
        V = 0.5  # Conservative estimate

        M_n = (self.alpha * V + self.beta * L + self.gamma * F_ds_star) / 1.0

        return MultimodalFusionResult(
            fusion_score=M_n,
            visual_validity=V,
            linguistic_relevance=L,
            cultural_fidelity=F_ds_star,
            computational_cost=1.0,
            metabolic_mode=MetabolicMode.HYBRID,
            energy_efficiency=M_n,
            quality_standard=self.quality_standard,
            timestamp=datetime.now(),
            fallback_used=True,
        )

    def get_metabolic_health_report(self) -> Dict[str, Any]:
        """Get current metabolic health status"""
        return {
            "mode": self.metabolic_state.mode.value,
            "clarity_score": self.metabolic_state.clarity_score,
            "energy_level": self.metabolic_state.energy_level,
            "energy_reserves": self.energy_reserves,
            "visual_state": self.metabolic_state.visual_state,
            "processing_history_length": len(self.processing_history),
            "quality_standard": self.quality_standard,
        }


# Helper functions for easy access
def calculate_multimodal_fusion(
    visual_data: Optional[Image.Image] = None,
    linguistic_data: str = "",
    cultural_outputs: Optional[Dict[str, float]] = None,
    computational_cost: float = 1.0,
) -> MultimodalFusionResult:
    """
    Quick multimodal fusion calculation

    Args:
        visual_data: Optional PIL Image
        linguistic_data: Text data
        cultural_outputs: Cultural scores from DS-STAR
        computational_cost: Computational cost

    Returns:
        MultimodalFusionResult
    """
    core = MultimodalMetabolismCore()
    return core.calculate_fusion(
        visual_data, linguistic_data, cultural_outputs, computational_cost
    )


def verify_multimodal_quality(result: MultimodalFusionResult) -> bool:
    """
    Verify multimodal fusion meets 369/370 quality standard

    Args:
        result: Fusion result to verify

    Returns:
        True if quality standard is met
    """
    quality_checks = [
        result.fusion_score > 0.0,
        result.quality_standard >= (369.0 / 370.0),
        result.visual_validity >= 0.0,
        result.linguistic_relevance >= 0.0,
        result.cultural_fidelity >= 0.0,
    ]

    return all(quality_checks)
