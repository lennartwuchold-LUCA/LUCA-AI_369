"""
Neurodiversity Parameter (γ)

Quantifies cognitive variance for resource allocation optimization.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class Neurotype(Enum):
    """Neurodiversity categories"""
    NEUROTYPICAL = "neurotypical"
    ADHD = "adhd"
    AUTISM = "autism"
    CUSTOM = "custom"


@dataclass
class NeurodiversityParameter:
    """
    Gamma (γ) parameter for neurodiversity modeling

    Based on empirical observations:
    - γ = 1.0: Neurotypical baseline
    - γ = 1.8-2.5: ADHD range (higher chaos tolerance)
    - γ > 3.0: Autism range (lower chaos tolerance, sustained focus)

    Mathematical basis:
        μ(γ, S) = μ_max × (γ × S) / (K_s + γ × S)

    Where higher γ → faster saturation (ADHD: quick context switching)
    """

    value: float
    neurotype: Neurotype
    description: Optional[str] = None

    @classmethod
    def from_neurotype(cls, neurotype: Neurotype) -> 'NeurodiversityParameter':
        """
        Create gamma parameter from neurotype

        Args:
            neurotype: Neurotype enum value

        Returns:
            NeurodiversityParameter instance with appropriate gamma value
        """
        gamma_map = {
            Neurotype.NEUROTYPICAL: (1.0, "Baseline cognitive processing"),
            Neurotype.ADHD: (2.0, "Faster context switching, higher chaos tolerance"),
            Neurotype.AUTISM: (3.5, "Sustained focus, lower chaos tolerance"),
            Neurotype.CUSTOM: (1.0, "Custom gamma value")
        }

        value, description = gamma_map[neurotype]

        return cls(
            value=value,
            neurotype=neurotype,
            description=description
        )

    @classmethod
    def from_value(cls, value: float) -> 'NeurodiversityParameter':
        """
        Create gamma parameter from numeric value

        Args:
            value: Gamma value (typically 0.5-5.0)

        Returns:
            NeurodiversityParameter instance
        """
        # Classify neurotype based on value
        if 0.8 <= value <= 1.2:
            neurotype = Neurotype.NEUROTYPICAL
        elif 1.8 <= value <= 2.5:
            neurotype = Neurotype.ADHD
        elif value > 3.0:
            neurotype = Neurotype.AUTISM
        else:
            neurotype = Neurotype.CUSTOM

        return cls(
            value=value,
            neurotype=neurotype,
            description=f"Gamma = {value:.2f}"
        )

    def adjust_for_energy(self, energy_level: str) -> float:
        """
        Adjust gamma based on user energy level

        Args:
            energy_level: 'hyperfocus', 'normal', or 'brainfog'

        Returns:
            Adjusted gamma value
        """
        adjustments = {
            'hyperfocus': 1.2,   # Increase gamma (more capacity)
            'normal': 1.0,       # No adjustment
            'brainfog': 0.6      # Decrease gamma (less capacity)
        }

        multiplier = adjustments.get(energy_level.lower(), 1.0)
        return self.value * multiplier

    def is_adhd_range(self) -> bool:
        """Check if gamma is in ADHD range"""
        return 1.8 <= self.value <= 2.5

    def is_autism_range(self) -> bool:
        """Check if gamma is in autism range"""
        return self.value > 3.0

    def is_neurotypical_range(self) -> bool:
        """Check if gamma is in neurotypical range"""
        return 0.8 <= self.value <= 1.2


# Predefined gamma values for convenience
GAMMA_NEUROTYPICAL = NeurodiversityParameter.from_neurotype(Neurotype.NEUROTYPICAL)
GAMMA_ADHD = NeurodiversityParameter.from_neurotype(Neurotype.ADHD)
GAMMA_AUTISM = NeurodiversityParameter.from_neurotype(Neurotype.AUTISM)
