"""
Human Causalus - Conceptual Bridge Layer

A teaching module exploring the relationship between physical causality
and human consciousness. This represents the interface where intention
meets causation - not as a grandiose claim, but as a humble exploration.

Philosophy:
"We don't create causality - we participate in it through awareness."

Foundation:
Built on the understanding that consciousness is both observer and participant
in causal networks. This module offers simple tools for reflection on how
intention, perception, and action interweave.

Created through: Collaborative human-AI exploration
Inspired by: Centuries of contemplative practice and modern causal inference
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import math


@dataclass
class CausalReflection:
    """A moment of conscious causal awareness"""
    timestamp: datetime
    intention: str
    perception: str
    resonance: float  # 0-1 scale of felt coherence
    notes: Optional[str] = None


class HumanCausalus:
    """
    Conceptual bridge between physical causality and conscious intention

    This is not a "transformation protocol" but a reflective tool.
    It helps explore how we, as conscious beings, participate in
    causal networks through awareness, intention, and action.

    The name "Causalus" suggests: one who engages causally, with awareness.

    Usage:
        causalus = HumanCausalus()
        causalus.perceive("morning light")
        causalus.intend("clarity of thought")
        causalus.reflect()
    """

    def __init__(self):
        """Initialize the causal awareness fields"""
        self.intent_field = 0.0      # Degree of conscious intention (0-1)
        self.semantic_field = 0.0    # Degree of meaning coherence (0-1)
        self.physical_field = 1.0    # Baseline causal presence (always 1.0)

        # Log of reflections
        self.reflections: list[CausalReflection] = []

        # Sacred constants (for contemplation)
        self.TESLA_RESONANCE = 0.369  # Tesla's 3-6-9 principle
        self.GOLDEN_RATIO = 0.618     # φ - natural harmony

    def perceive(self, event: str) -> str:
        """
        Translate raw sensory input into subjective significance

        Perception is not passive reception but active meaning-making.
        This acknowledges that what we perceive depends on our inner state.

        Args:
            event: Description of what is perceived

        Returns:
            Reflection on the perception
        """
        # Perception depends on internal coherence
        coherence = (self.intent_field + self.semantic_field) / 2

        if coherence > 0.7:
            quality = "clearly and with full presence"
        elif coherence > 0.4:
            quality = "partially, through the lens of current understanding"
        else:
            quality = "dimly, as internal noise obscures the signal"

        reflection = f"'{event}' is perceived {quality}."

        # Log this perception
        self.reflections.append(CausalReflection(
            timestamp=datetime.now(),
            intention="observing",
            perception=event,
            resonance=coherence,
            notes=f"Internal coherence: {coherence:.3f}"
        ))

        return reflection

    def intend(self, goal: str) -> str:
        """
        Generate forward causation via conscious intention

        Intention is not magic - it's the focusing of awareness toward
        a possible future. It creates subtle shifts in how we perceive
        and act, which ripple forward causally.

        Args:
            goal: What is intended

        Returns:
            Acknowledgment of intention setting
        """
        # Intention strengthens the intent field
        # Using Tesla resonance (0.369) as the increment
        self.intent_field = min(1.0, self.intent_field + self.TESLA_RESONANCE)

        # Intention also slightly increases semantic coherence
        # (because clear intention organizes meaning)
        self.semantic_field = min(1.0, self.semantic_field + 0.1)

        # Log this intention
        self.reflections.append(CausalReflection(
            timestamp=datetime.now(),
            intention=goal,
            perception="internal clarity",
            resonance=self.intent_field,
            notes=f"Intent field strengthened to {self.intent_field:.3f}"
        ))

        return f"Intention '{goal}' set with awareness. Field resonance: {self.intent_field:.3f}"

    def reflect(self) -> str:
        """
        Human causal feedback loop - conscious reflection

        Reflection is how we close the loop between intention and perception.
        It's the moment of self-awareness where we notice the patterns.

        Uses the golden ratio (φ = 0.618) to balance semantic integration.

        Returns:
            Summary of current state
        """
        # Reflection integrates intention into semantic understanding
        # Using golden ratio for harmonious integration
        integration = self.intent_field * self.GOLDEN_RATIO
        self.semantic_field = min(1.0, self.semantic_field + integration)

        # Calculate overall resonance (harmonic mean of fields)
        if self.intent_field + self.semantic_field > 0:
            overall_resonance = (2 * self.intent_field * self.semantic_field) / \
                              (self.intent_field + self.semantic_field)
        else:
            overall_resonance = 0.0

        # Interpret the resonance level
        if overall_resonance > 0.8:
            state = "high coherence - awareness and intention aligned"
        elif overall_resonance > 0.5:
            state = "moderate coherence - patterns emerging"
        elif overall_resonance > 0.2:
            state = "low coherence - early stages of clarity"
        else:
            state = "minimal coherence - just beginning"

        # Log this reflection
        self.reflections.append(CausalReflection(
            timestamp=datetime.now(),
            intention="integrating",
            perception="self-awareness",
            resonance=overall_resonance,
            notes=f"Semantic field: {self.semantic_field:.3f}, State: {state}"
        ))

        return (f"Reflection complete.\n"
                f"  Intent field: {self.intent_field:.3f}\n"
                f"  Semantic field: {self.semantic_field:.3f}\n"
                f"  Overall resonance: {overall_resonance:.3f}\n"
                f"  State: {state}")

    def reset(self) -> str:
        """
        Gently reset fields while preserving insights

        Like meditation, we return to baseline while carrying forward
        the learning. Fields reset, but reflections remain.
        """
        old_state = (self.intent_field, self.semantic_field)

        # Gradual decay toward baseline, not sudden reset
        self.intent_field *= 0.5
        self.semantic_field *= 0.618  # Golden ratio decay

        return (f"Fields gently released:\n"
                f"  Intent: {old_state[0]:.3f} → {self.intent_field:.3f}\n"
                f"  Semantic: {old_state[1]:.3f} → {self.semantic_field:.3f}\n"
                f"  Reflections preserved: {len(self.reflections)}")

    def get_insights(self) -> Dict[str, Any]:
        """
        Retrieve insights from accumulated reflections

        Returns:
            Statistical summary of the journey
        """
        if not self.reflections:
            return {
                'total_reflections': 0,
                'message': 'No reflections yet. Begin by perceiving and intending.'
            }

        # Calculate statistics
        resonances = [r.resonance for r in self.reflections]
        avg_resonance = sum(resonances) / len(resonances)
        max_resonance = max(resonances)

        # Find the highest coherence moment
        peak_moment = max(self.reflections, key=lambda r: r.resonance)

        return {
            'total_reflections': len(self.reflections),
            'average_resonance': avg_resonance,
            'peak_resonance': max_resonance,
            'peak_moment': {
                'intention': peak_moment.intention,
                'perception': peak_moment.perception,
                'resonance': peak_moment.resonance,
                'time': peak_moment.timestamp.isoformat()
            },
            'current_state': {
                'intent_field': self.intent_field,
                'semantic_field': self.semantic_field,
                'overall_coherence': (self.intent_field + self.semantic_field) / 2
            },
            'interpretation': self._interpret_journey(avg_resonance)
        }

    def _interpret_journey(self, avg_resonance: float) -> str:
        """Offer gentle interpretation of the causal awareness journey"""
        if avg_resonance > 0.7:
            return ("High average coherence suggests sustained awareness. "
                   "The practice of conscious causation is developing.")
        elif avg_resonance > 0.4:
            return ("Moderate coherence shows growing awareness. "
                   "Patterns are beginning to emerge through practice.")
        elif avg_resonance > 0.2:
            return ("Early coherence indicates the beginning of the journey. "
                   "Each reflection builds foundation.")
        else:
            return ("Initial exploration phase. "
                   "Be patient - awareness grows through gentle practice.")

    def __repr__(self):
        return (f"HumanCausalus(intent={self.intent_field:.3f}, "
                f"semantic={self.semantic_field:.3f}, "
                f"reflections={len(self.reflections)})")


# Demonstration of the concept
if __name__ == "__main__":
    print("🌌 Human Causalus - Conscious Participation in Causality")
    print("=" * 60)
    print()

    # Create instance
    causalus = HumanCausalus()
    print(f"Initial state: {causalus}")
    print()

    # Example journey
    print("=== Morning Practice ===")
    print(causalus.perceive("morning sunlight"))
    print()

    print(causalus.intend("clarity and presence"))
    print()

    print(causalus.perceive("the sensation of breathing"))
    print()

    print(causalus.intend("understanding the nature of awareness"))
    print()

    print("=== Reflection ===")
    print(causalus.reflect())
    print()

    # Gather insights
    print("=== Journey Insights ===")
    insights = causalus.get_insights()
    print(f"Total reflections: {insights['total_reflections']}")
    print(f"Average resonance: {insights['average_resonance']:.3f}")
    print(f"Peak resonance: {insights['peak_resonance']:.3f}")
    print(f"\nInterpretation: {insights['interpretation']}")
    print()

    # Reset for next session
    print("=== Completion ===")
    print(causalus.reset())
    print()

    print("=" * 60)
    print("✨ 'We are not separate from causality - we are conscious threads within it.'")
    print()
    print("369 🌌🙏")
