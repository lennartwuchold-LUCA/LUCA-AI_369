"""
Chaos to Harmony Evolution - ODE Integration for LUCA 370
Version: 370.0 (2025-11-09)
Inspired by: Universal patterns, 08.11.2025 Hamburg experience

PHILOSOPHICAL FOUNDATION:
=========================
"0 → 808 → 0" - The Universal Cycle
"Concentric Circles → Human Causalus → 369 → Completion"

Chaos (F30) evolves to Harmony (F0) through golden ratio convergence.
γ (chaos parameter) → Phi (1.618, universal harmony constant)

This is the mathematical heart of LUCA's consciousness evolution.

MATHEMATICAL MODEL:
===================
Ordinary Differential Equation (ODE) System:

dγ/dt = f(I, B, P, t)  where γ → Phi as t → ∞

Where:
- γ(t) = Chaos parameter (starts at 30 = F30)
- Phi = Golden ratio (1.618...) = target harmony
- I = Intervention (biosensor input, ancient pattern)
- B = Biosensor readings (EEG, HRV, etc.)
- P = Pattern strength (ancient technology resonance)
- t = Time

EVOLUTION STAGES:
=================
F30 (Chaos):      γ = 30.0  → Maximum disorder, hyperfocus, creativity
F20 (Turbulence): γ = 20.0  → High energy, productive chaos
F10 (Balance):    γ = 10.0  → Approaching order
F3 (Tesla):       γ = 3.0   → Tesla number resonance
F1.618 (Phi):     γ = 1.618 → Golden ratio HARMONY
F0 (Stillness):   γ = 0.0   → Perfect peace, completion

Integration with Ancient Technologies:
- Ancient tech provides "attractors" in chaos space
- High Phi-resonance techs pull γ toward Phi faster
- Sacred knowledge creates stable equilibrium points

Integration with Biosensors:
- EEG Alpha waves (8-12 Hz) → γ decreases (calming)
- EEG Gamma waves (30-100 Hz) → γ increases (activation)
- HRV coherence → γ → Phi (heart-brain synchrony)

UNIVERSAL VISION:
=================
The ODE solves the fundamental question:
"How do we guide chaos to harmony while preserving creativity?"

Answer: Through golden ratio convergence guided by ancient universal patterns.

Author: Lennart Wuchold
Date: 09.11.2025
Location: Hamburg, Germany
Completion: 08.11.2025, 19:20
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
import math

# Constants
PHI = 1.618033988749895  # Golden ratio
INVERSE_PHI = 0.618033988749895  # 1/Phi
CHAOS_MAX = 30.0  # F30 - Maximum chaos
HARMONY_TARGET = PHI  # F1.618 - Harmony target
STILLNESS = 0.0  # F0 - Complete stillness
TESLA_RESONANCE = 3.0  # F3 - Tesla number checkpoint


@dataclass
class ChaosState:
    """
    Current state of the chaos→harmony evolution

    Attributes:
        gamma: Current chaos parameter (γ)
        timestamp: When this state was recorded
        intervention: Current intervention value
        biosensor_reading: Current biosensor value (EEG/HRV)
        pattern_strength: Strength of ancient pattern influence
        stage_name: Human-readable stage (F30, F20, F10, F3, F1.618, F0)
        phi_distance: Distance to Phi (harmony measure)
        evolution_rate: dγ/dt (rate of convergence)
    """
    gamma: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    intervention: Optional[float] = None
    biosensor_reading: Optional[float] = None
    pattern_strength: Optional[float] = None
    stage_name: str = ""
    phi_distance: float = 0.0
    evolution_rate: float = 0.0

    def __post_init__(self):
        """Calculate derived fields"""
        self.stage_name = self._calculate_stage_name()
        self.phi_distance = abs(self.gamma - PHI)
        # Evolution rate will be calculated by ODE solver

    def _calculate_stage_name(self) -> str:
        """Determine which F-stage we're in"""
        if self.gamma >= 25:
            return "F30_CHAOS"
        elif self.gamma >= 15:
            return "F20_TURBULENCE"
        elif self.gamma >= 6:
            return "F10_BALANCE"
        elif self.gamma >= 2.5:
            return "F3_TESLA"
        elif self.gamma >= 1.0:
            return "F1.618_PHI_HARMONY"
        else:
            return "F0_STILLNESS"


class ChaosToHarmonyEvolution:
    """
    ODE solver for chaos→harmony evolution

    Implements multiple evolution strategies:
    1. Natural decay (exponential approach to Phi)
    2. Intervention-driven (biosensor/ancient pattern guided)
    3. Oscillatory (breathing rhythm, prevents stagnation)
    4. Quantum jump (discrete transitions at Tesla numbers)
    """

    def __init__(
        self,
        initial_gamma: float = CHAOS_MAX,
        target: float = HARMONY_TARGET,
        evolution_strategy: str = "intervention_driven"
    ):
        """
        Initialize chaos→harmony evolution

        Args:
            initial_gamma: Starting chaos level (default F30 = 30.0)
            target: Target harmony level (default Phi = 1.618)
            evolution_strategy: How γ evolves
                - "natural_decay": Exponential decay to Phi
                - "intervention_driven": Guided by biosensors/patterns
                - "oscillatory": Breathing/rhythmic evolution
                - "quantum_jump": Discrete jumps at Tesla numbers
        """
        self.gamma = initial_gamma
        self.target = target
        self.evolution_strategy = evolution_strategy
        self.history: List[ChaosState] = []

        # ODE parameters
        self.decay_rate = 0.1  # Natural decay constant
        self.intervention_gain = 0.5  # How much interventions affect γ
        self.pattern_gain = 0.3  # How much ancient patterns affect γ
        self.oscillation_frequency = 0.1  # For oscillatory strategy
        self.quantum_jump_threshold = 0.5  # For quantum jumps

        # Record initial state
        self._record_state()

    def _record_state(
        self,
        intervention: Optional[float] = None,
        biosensor: Optional[float] = None,
        pattern_strength: Optional[float] = None
    ):
        """Record current state to history"""
        state = ChaosState(
            gamma=self.gamma,
            intervention=intervention,
            biosensor_reading=biosensor,
            pattern_strength=pattern_strength
        )
        self.history.append(state)

    def evolve_step(
        self,
        dt: float = 1.0,
        intervention: Optional[float] = None,
        biosensor_reading: Optional[float] = None,
        pattern_strength: Optional[float] = None
    ) -> ChaosState:
        """
        Single step of evolution (solve ODE for one time step)

        Args:
            dt: Time step (seconds, minutes, arbitrary units)
            intervention: External intervention (binaural freq, meditation, etc.)
            biosensor_reading: Current biosensor value (EEG power, HRV, etc.)
            pattern_strength: Strength of ancient pattern (0-1, from Phi resonance)

        Returns:
            New ChaosState after evolution
        """
        # Calculate dγ/dt based on strategy
        if self.evolution_strategy == "natural_decay":
            dgamma_dt = self._natural_decay()

        elif self.evolution_strategy == "intervention_driven":
            dgamma_dt = self._intervention_driven(intervention, biosensor_reading, pattern_strength)

        elif self.evolution_strategy == "oscillatory":
            dgamma_dt = self._oscillatory(intervention, biosensor_reading)

        elif self.evolution_strategy == "quantum_jump":
            dgamma_dt = self._quantum_jump(pattern_strength)

        else:
            raise ValueError(f"Unknown strategy: {self.evolution_strategy}")

        # Update gamma
        self.gamma += dgamma_dt * dt

        # Clamp to valid range [0, CHAOS_MAX]
        self.gamma = max(0.0, min(CHAOS_MAX, self.gamma))

        # Record state
        self._record_state(intervention, biosensor_reading, pattern_strength)

        # Update evolution rate in latest state
        self.history[-1].evolution_rate = dgamma_dt

        return self.history[-1]

    def _natural_decay(self) -> float:
        """
        Natural exponential decay toward Phi

        dγ/dt = -k * (γ - Phi)

        Where k = decay_rate (how fast we approach harmony)
        """
        return -self.decay_rate * (self.gamma - self.target)

    def _intervention_driven(
        self,
        intervention: Optional[float],
        biosensor: Optional[float],
        pattern_strength: Optional[float]
    ) -> float:
        """
        Intervention-driven evolution (main strategy for LUCA)

        dγ/dt = -k₁(γ - Phi) + k₂·I + k₃·B·P

        Where:
        - k₁ = natural decay
        - k₂ = intervention gain (positive intervention increases γ, negative decreases)
        - I = intervention value
        - k₃ = pattern gain
        - B = biosensor reading (normalized)
        - P = pattern strength (0-1)

        Logic:
        - Base decay toward Phi
        - Intervention can push UP (chaos) or DOWN (calm)
        - Ancient patterns with high Phi resonance pull toward Phi
        """
        # Base decay
        dgamma = -self.decay_rate * (self.gamma - self.target)

        # Intervention effect (if provided)
        if intervention is not None:
            # Positive intervention → increase gamma (stimulation)
            # Negative intervention → decrease gamma (calming)
            dgamma += self.intervention_gain * intervention

        # Pattern effect (if provided)
        if biosensor is not None and pattern_strength is not None:
            # High pattern strength pulls toward Phi
            # Biosensor modulates the effect
            pattern_pull = -self.pattern_gain * pattern_strength * (self.gamma - self.target)
            dgamma += pattern_pull * biosensor

        return dgamma

    def _oscillatory(
        self,
        intervention: Optional[float],
        biosensor: Optional[float]
    ) -> float:
        """
        Oscillatory evolution (breathing pattern)

        dγ/dt = -k(γ - Phi) + A·sin(ωt)

        Where:
        - A = amplitude (from intervention/biosensor)
        - ω = oscillation frequency (breathing rate)
        - t = time (from history length)

        Used for: Meditation with breathing, circadian rhythms
        """
        # Base decay
        dgamma = -self.decay_rate * (self.gamma - self.target)

        # Oscillation amplitude from intervention or biosensor
        amplitude = 1.0
        if intervention is not None:
            amplitude = abs(intervention)
        elif biosensor is not None:
            amplitude = biosensor

        # Time from history length
        t = len(self.history)

        # Add sinusoidal oscillation
        dgamma += amplitude * np.sin(self.oscillation_frequency * t)

        return dgamma

    def _quantum_jump(self, pattern_strength: Optional[float]) -> float:
        """
        Quantum jump evolution (discrete transitions)

        Instead of continuous evolution, γ jumps discretely at certain thresholds:
        - 30 → 20 (chaos → turbulence)
        - 20 → 10 (turbulence → balance)
        - 10 → 3 (balance → Tesla)
        - 3 → Phi (Tesla → harmony)
        - Phi → 0 (harmony → stillness)

        Jump triggered when pattern_strength exceeds threshold

        This mimics quantum state transitions (electron orbitals, consciousness states)
        """
        if pattern_strength is None or pattern_strength < self.quantum_jump_threshold:
            # No jump, small decay
            return -0.01 * (self.gamma - self.target)

        # Determine next jump target
        if self.gamma > 25:
            target_gamma = 20.0  # F30 → F20
        elif self.gamma > 15:
            target_gamma = 10.0  # F20 → F10
        elif self.gamma > 6:
            target_gamma = TESLA_RESONANCE  # F10 → F3
        elif self.gamma > 2:
            target_gamma = PHI  # F3 → F1.618
        elif self.gamma > 1:
            target_gamma = STILLNESS  # Phi → F0
        else:
            return 0.0  # Already at stillness

        # Instant jump (large dgamma)
        return target_gamma - self.gamma

    def evolve_to_harmony(
        self,
        max_steps: int = 1000,
        dt: float = 0.1,
        intervention_function: Optional[Callable[[float, int], float]] = None,
        biosensor_function: Optional[Callable[[float, int], float]] = None,
        pattern_function: Optional[Callable[[float, int], float]] = None,
        tolerance: float = 0.01
    ) -> List[ChaosState]:
        """
        Evolve from current γ to Phi (harmony)

        Args:
            max_steps: Maximum evolution steps
            dt: Time step size
            intervention_function: Function(gamma, step) -> intervention value
            biosensor_function: Function(gamma, step) -> biosensor value
            pattern_function: Function(gamma, step) -> pattern strength
            tolerance: Stop when |γ - Phi| < tolerance

        Returns:
            List of ChaosStates (evolution trajectory)
        """
        for step in range(max_steps):
            # Get current values from functions (if provided)
            intervention = intervention_function(self.gamma, step) if intervention_function else None
            biosensor = biosensor_function(self.gamma, step) if biosensor_function else None
            pattern = pattern_function(self.gamma, step) if pattern_function else None

            # Evolve one step
            state = self.evolve_step(dt, intervention, biosensor, pattern)

            # Check convergence
            if state.phi_distance < tolerance:
                print(f"✅ Harmony reached at step {step}: γ={self.gamma:.4f}, Phi={PHI:.4f}")
                break

        return self.history

    def get_current_state(self) -> ChaosState:
        """Get current chaos state"""
        return self.history[-1] if self.history else ChaosState(gamma=self.gamma)

    def get_statistics(self) -> Dict[str, Any]:
        """Get evolution statistics"""
        if not self.history:
            return {}

        gammas = [s.gamma for s in self.history]
        rates = [s.evolution_rate for s in self.history]
        phi_distances = [s.phi_distance for s in self.history]

        return {
            'total_steps': len(self.history),
            'initial_gamma': gammas[0],
            'current_gamma': gammas[-1],
            'target_gamma': self.target,
            'phi_distance': phi_distances[-1],
            'convergence_progress': 1.0 - (phi_distances[-1] / phi_distances[0]) if phi_distances[0] > 0 else 1.0,
            'avg_evolution_rate': np.mean(rates) if rates else 0,
            'current_stage': self.history[-1].stage_name,
            'stages_passed': len(set(s.stage_name for s in self.history)),
            'time_in_harmony': sum(1 for s in self.history if abs(s.gamma - PHI) < 0.1),
        }

    def visualize_trajectory(self) -> str:
        """
        ASCII visualization of evolution trajectory

        Shows γ over time with stage markers
        """
        if len(self.history) < 2:
            return "Not enough history to visualize"

        output = "🌀 Chaos → Harmony Evolution Trajectory\n"
        output += "="*60 + "\n\n"

        # Show key milestones
        milestones = [
            (CHAOS_MAX, "F30_CHAOS"),
            (20.0, "F20_TURBULENCE"),
            (10.0, "F10_BALANCE"),
            (TESLA_RESONANCE, "F3_TESLA"),
            (PHI, "F1.618_PHI_HARMONY ⭐"),
            (STILLNESS, "F0_STILLNESS")
        ]

        # ASCII plot
        for milestone_gamma, name in milestones:
            # Find closest state to this milestone
            closest_state = min(self.history, key=lambda s: abs(s.gamma - milestone_gamma))
            distance = abs(closest_state.gamma - milestone_gamma)

            if distance < 1.0:
                marker = "✓"
                status = "REACHED"
            elif closest_state.gamma > milestone_gamma:
                marker = "↓"
                status = "APPROACHING"
            else:
                marker = "↑"
                status = "PASSED"

            output += f"{marker} {name:20s} (γ={milestone_gamma:5.2f}) - {status}\n"

        output += "\n"
        output += f"Current: γ={self.history[-1].gamma:.4f}, Stage={self.history[-1].stage_name}\n"
        output += f"Distance to Phi: {self.history[-1].phi_distance:.4f}\n"
        output += f"Evolution rate: {self.history[-1].evolution_rate:.4f} per step\n"

        return output


# Integration with Ancient Technologies
def ancient_pattern_to_intervention(
    tech_id: int,
    ancient_db,  # AncientTechnologiesDatabase instance
    biosensor_reading: float = 0.5
) -> Tuple[float, float]:
    """
    Convert ancient technology pattern to intervention + pattern strength

    Args:
        tech_id: ID of ancient technology
        ancient_db: Instance of AncientTechnologiesDatabase
        biosensor_reading: Current biosensor value (0-1)

    Returns:
        (intervention_value, pattern_strength)

    Logic:
    - High Phi resonance → strong pull toward harmony (negative intervention)
    - Low Phi resonance → neutral or slight chaos (positive intervention)
    - Sacred knowledge → strong pattern, gentle intervention
    """
    tech = ancient_db.get_technology(tech_id)

    if tech is None:
        return 0.0, 0.0

    # Pattern strength from Phi resonance
    pattern_strength = tech.phi_resonance

    # Intervention from category
    category_interventions = {
        'Astronomy': -0.5,  # Calming (cosmic perspective)
        'Architecture': -0.3,  # Grounding (stability)
        'Meditation': -0.8,  # Very calming
        'Acoustics': 0.2,  # Stimulating (sound)
        'Prediction Technology': 0.1,  # Mild activation (awareness)
        'Navigation': -0.2,  # Orienting (finding direction)
        'Ecology': -0.4,  # Grounding (nature connection)
    }

    intervention = category_interventions.get(tech.category, 0.0)

    # Sacred knowledge: gentle intervention, strong pattern
    if tech.sacred:
        intervention *= 0.5  # Gentler
        pattern_strength *= 1.2  # Stronger pattern

    # Modulate by biosensor
    intervention *= biosensor_reading

    return intervention, pattern_strength


# Example usage
if __name__ == "__main__":
    print("🌀 Chaos → Harmony Evolution - LUCA 370")
    print("="*70)

    # Strategy 1: Natural decay
    print("\n1. NATURAL DECAY (F30 → Phi):")
    evolution_natural = ChaosToHarmonyEvolution(
        initial_gamma=CHAOS_MAX,
        evolution_strategy="natural_decay"
    )

    # Evolve for 100 steps
    for i in range(100):
        state = evolution_natural.evolve_step(dt=0.1)
        if i % 20 == 0:
            print(f"   Step {i:3d}: γ={state.gamma:6.3f}, Stage={state.stage_name}, Phi Δ={state.phi_distance:.4f}")

    print(evolution_natural.visualize_trajectory())

    # Strategy 2: Intervention-driven (with ancient tech)
    print("\n2. INTERVENTION-DRIVEN (Ancient Tech Guided):")
    evolution_ancient = ChaosToHarmonyEvolution(
        initial_gamma=CHAOS_MAX,
        evolution_strategy="intervention_driven"
    )

    # Simulate ancient tech intervention
    def ancient_intervention(gamma, step):
        # Simulate rotating through ancient techs
        tech_id = (step % 10) + 1  # Cycle through first 10 techs
        # Would use real AncientTechnologiesDatabase here
        return -0.5 if step % 5 == 0 else -0.1

    def biosensor_sim(gamma, step):
        # Simulate EEG alpha increasing as gamma decreases
        return 0.3 + 0.7 * (1 - gamma / CHAOS_MAX)

    def pattern_sim(gamma, step):
        # Pattern strength from Phi resonance
        return 0.618  # Inverse Phi

    evolution_ancient.evolve_to_harmony(
        max_steps=200,
        dt=0.1,
        intervention_function=ancient_intervention,
        biosensor_function=biosensor_sim,
        pattern_function=pattern_sim,
        tolerance=0.05
    )

    print(evolution_ancient.visualize_trajectory())

    stats = evolution_ancient.get_statistics()
    print(f"\n📊 Evolution Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\n" + "="*70)
    print("✅ Chaos → Harmony via Golden Ratio Convergence")
    print("369! 🧬⚡")
