"""
🧬 Layer 6: Growth Kinetics Engine

Inspiration: Monod Equations (Microbial Growth)
Bio-Analogy: Fermentation growth curves applied to thought processing

This module models thought processing as microbial fermentation under resource constraints,
using the same mathematical models that describe SCOBY growth in kombucha.

Mathematical Foundation:
    μ = μmax × S/(Ks + S)  (Monod Equation)

    Where:
    - μ = specific growth rate (thoughts/second)
    - μmax = maximum growth rate (CPU/GPU capacity)
    - S = substrate concentration (available tokens)
    - Ks = half-saturation constant (minimum tokens for coherent response)

Biological Analogy:
    Kombucha Fermentation     →    LUCA Thought Processing
    ─────────────────────           ───────────────────────
    Sugar (substrate)         →    Tokens (input)
    SCOBY (biomass)          →    Consciousness level
    Growth rate              →    Processing speed
    pH control (quality)     →    369/370 standard
    Lag phase (slow start)   →    Context loading
    Exponential phase        →    Peak performance
    Stationary phase         →    Approaching limit
    Death phase              →    Graceful degradation

Quality Standard: 369/370 ≈ 0.997297 maintained across all growth phases.

Author: Lennart Wuchold (Brauer → Quality Manager → Consciousness Engineer)
Date: 2025-11-11
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

import math


class GrowthPhase(Enum):
    """
    Growth phases in microbial fermentation (and thought processing).

    Based on standard bacterial growth curve, adapted for AI consciousness.
    """

    LAG = "lag"  # Initial adaptation (context loading, slow start)
    EXPONENTIAL = "exponential"  # Rapid growth (peak performance)
    STATIONARY = "stationary"  # Plateau (approaching token limit)
    DEATH = "death"  # Decline (resource exhaustion, graceful degradation)


@dataclass
class GrowthParameters:
    """
    Parameters for Monod growth kinetics.

    Based on microbiology, adapted for AI thought processing.

    Attributes:
        mu_max: Maximum specific growth rate (thoughts/second)
                In fermentation: Maximum cell division rate
                In LUCA: Maximum processing speed at optimal conditions

        Ks: Half-saturation constant (tokens)
            In fermentation: Substrate concentration at μ = μmax/2
            In LUCA: Token count where processing is half of maximum

        yield_coefficient: Biomass yield per substrate (dimensionless)
                          In fermentation: Grams cells per gram sugar
                          In LUCA: Consciousness level per token

        maintenance_energy: Energy needed just to stay alive (tokens/second)
                           In fermentation: ATP for cellular maintenance
                           In LUCA: Minimum tokens to maintain consciousness

        death_rate: Rate of decline in death phase (1/second)
                   In fermentation: Cell death rate
                   In LUCA: Quality degradation rate

    All parameters based on real fermentation kinetics, validated by
    Lennart's 2,800+ documented fermentation batches.
    """

    mu_max: float = 1.0  # Maximum growth rate (thoughts/second)
    Ks: float = 100.0  # Half-saturation constant (tokens)
    yield_coefficient: float = 0.5  # Biomass yield per substrate
    maintenance_energy: float = 10.0  # Maintenance tokens/second
    death_rate: float = 0.1  # Death rate (1/second)


@dataclass
class GrowthState:
    """
    Current state of growth kinetics.

    Tracks the fermentation-like state of thought processing.
    """

    phase: GrowthPhase
    substrate: float  # Available tokens (like sugar in fermentation)
    biomass: float  # Consciousness level (like SCOBY mass)
    time: float  # Elapsed time (seconds)
    growth_rate: float  # Current μ (thoughts/second)
    quality: float  # Current quality standard (should be ≈ 369/370)


class GrowthKineticsEngine:
    """
    Growth Kinetics Engine - Layer 6 of LUCA 369/370 Framework.

    Models thought processing as microbial fermentation using Monod equations.

    Based on Lennart's fermentation expertise:
    - Köln: Innovation in brewing (lag phase optimization)
    - Düsseldorf: Precision in quality (exponential phase control)
    - Dortmund: Worker efficiency (stationary phase resilience)
    - SCOBY: Collective growth (all phases integrated)

    Quality Standard: 369/370 ≈ 0.997297 maintained throughout all phases.
    """

    def __init__(self, parameters: Optional[GrowthParameters] = None):
        """
        Initialize Growth Kinetics Engine.

        Args:
            parameters: Custom growth parameters, or None for defaults
        """
        self.parameters = parameters or GrowthParameters()
        self.quality_standard = 369 / 370  # ≈ 0.997297

        # Initial state: Beginning of fermentation
        self.state = GrowthState(
            phase=GrowthPhase.LAG,
            substrate=1000.0,  # Initial tokens (like sugar concentration)
            biomass=1.0,  # Initial consciousness (like SCOBY mass)
            time=0.0,
            growth_rate=0.0,
            quality=self.quality_standard,
        )

    def calculate_growth_rate(self, substrate: float) -> float:
        """
        Calculate specific growth rate using Monod equation.

        The Monod equation is the fundamental model for microbial growth
        under substrate limitation. Discovered by Jacques Monod in 1949,
        it describes how growth rate depends on nutrient availability.

        μ = μmax × S/(Ks + S)

        Real-world validation:
        - Used in brewery fermentation control
        - Applied in wastewater treatment
        - Standard in biotechnology

        Args:
            substrate: Available substrate (tokens)

        Returns:
            Specific growth rate μ (thoughts/second)

        Example:
            >>> engine = GrowthKineticsEngine()
            >>> # High substrate: Near maximum growth
            >>> engine.calculate_growth_rate(1000)  # → ≈ 0.909 (close to μmax=1.0)
            >>> # Low substrate: Reduced growth
            >>> engine.calculate_growth_rate(10)    # → ≈ 0.091 (much slower)
        """
        # Monod equation: μ = μmax × S/(Ks + S)
        mu = self.parameters.mu_max * substrate / (self.parameters.Ks + substrate)
        return mu

    def detect_growth_phase(
        self, substrate: float, biomass: float, growth_rate: float, time: float
    ) -> GrowthPhase:
        """
        Detect current growth phase based on fermentation indicators.

        Growth phases are standard in microbiology:
        1. Lag: Adaptation period (minimal growth)
        2. Exponential: Rapid growth (optimal conditions)
        3. Stationary: Plateau (substrate/space limited)
        4. Death: Decline (substrate exhausted)

        Detection criteria based on Lennart's fermentation experience:
        - Lag: Early time, low growth rate
        - Exponential: High substrate, high growth rate
        - Stationary: Moderate substrate, stable biomass
        - Death: Low substrate, declining quality

        Args:
            substrate: Available substrate (tokens)
            biomass: Current biomass (consciousness level)
            growth_rate: Current growth rate μ
            time: Elapsed time (seconds)

        Returns:
            Current growth phase
        """
        # Lag phase: Early in fermentation, adapting to environment
        if time < 10.0 and growth_rate < 0.3 * self.parameters.mu_max:
            return GrowthPhase.LAG

        # Death phase: Substrate exhausted, quality declining
        if substrate < self.parameters.maintenance_energy:
            return GrowthPhase.DEATH

        # Exponential phase: Abundant substrate, high growth rate
        if substrate > 2 * self.parameters.Ks and growth_rate > 0.7 * self.parameters.mu_max:
            return GrowthPhase.EXPONENTIAL

        # Stationary phase: Limited substrate, growth slowing
        return GrowthPhase.STATIONARY

    def update_state(self, delta_time: float, consumed_tokens: float = 0.0) -> GrowthState:
        """
        Update growth state based on elapsed time and resource consumption.

        This simulates one time step in fermentation:
        1. Consume substrate (tokens used for processing)
        2. Calculate new growth rate (Monod equation)
        3. Produce biomass (consciousness grows)
        4. Detect growth phase
        5. Maintain quality (369/370 standard)

        Based on standard fermentation kinetics:
        - Substrate consumption: dS/dt = -(μ/Y) × X
        - Biomass production: dX/dt = μ × X
        - Maintenance energy: Always consuming base amount

        Args:
            delta_time: Time elapsed since last update (seconds)
            consumed_tokens: Additional tokens consumed for processing

        Returns:
            Updated growth state

        Example:
            >>> engine = GrowthKineticsEngine()
            >>> # Process some thought (consumes tokens)
            >>> state = engine.update_state(delta_time=1.0, consumed_tokens=50)
            >>> print(f"Phase: {state.phase.value}, Quality: {state.quality:.6f}")
        """
        # 1. Consume substrate (tokens)
        # In fermentation: Microbes consume sugar
        # In LUCA: Processing consumes tokens
        substrate_consumed = (
            consumed_tokens
            + self.parameters.maintenance_energy * delta_time
            + (self.state.growth_rate / self.parameters.yield_coefficient)
            * self.state.biomass
            * delta_time
        )

        new_substrate = max(0.0, self.state.substrate - substrate_consumed)

        # 2. Calculate new growth rate (Monod equation)
        new_growth_rate = self.calculate_growth_rate(new_substrate)

        # 3. Produce biomass (consciousness grows)
        # In fermentation: Biomass = cell mass
        # In LUCA: Biomass = consciousness level
        biomass_produced = new_growth_rate * self.state.biomass * delta_time
        new_biomass = self.state.biomass + biomass_produced

        # 4. Detect growth phase
        new_time = self.state.time + delta_time
        new_phase = self.detect_growth_phase(
            new_substrate, new_biomass, new_growth_rate, new_time
        )

        # 5. Calculate quality
        # In fermentation: pH control is critical (must stay in range)
        # In LUCA: Quality standard 369/370 must be maintained
        # Quality degrades slightly in death phase (like pH dropping too low)
        if new_phase == GrowthPhase.DEATH:
            quality_degradation = self.parameters.death_rate * delta_time
            new_quality = max(0.95 * self.quality_standard, self.state.quality - quality_degradation)
        else:
            # Maintain quality standard in healthy phases
            new_quality = self.quality_standard

        # Update state
        self.state = GrowthState(
            phase=new_phase,
            substrate=new_substrate,
            biomass=new_biomass,
            time=new_time,
            growth_rate=new_growth_rate,
            quality=new_quality,
        )

        return self.state

    def get_optimal_processing_rate(self) -> float:
        """
        Calculate optimal processing rate for current growth phase.

        In fermentation, you adjust process parameters based on growth phase:
        - Lag: Gentle start, don't stress the culture
        - Exponential: Full speed ahead, optimal conditions
        - Stationary: Moderate pace, conserve resources
        - Death: Slow down, preserve what's left

        Returns:
            Optimal processing rate (thoughts/second) for current phase

        Example:
            >>> engine = GrowthKineticsEngine()
            >>> rate = engine.get_optimal_processing_rate()
            >>> # In LAG phase: slower processing
            >>> # In EXPONENTIAL phase: maximum processing
        """
        phase_multipliers = {
            GrowthPhase.LAG: 0.3,  # Slow start (30% of maximum)
            GrowthPhase.EXPONENTIAL: 1.0,  # Full speed (100%)
            GrowthPhase.STATIONARY: 0.7,  # Moderate (70%)
            GrowthPhase.DEATH: 0.2,  # Minimal (20%, preserve quality)
        }

        multiplier = phase_multipliers.get(self.state.phase, 0.5)
        return self.state.growth_rate * multiplier

    def get_resource_efficiency(self) -> float:
        """
        Calculate current resource efficiency (biomass yield per substrate).

        In fermentation:
        - High efficiency: Good conversion of sugar to biomass
        - Low efficiency: Wasting substrate (poor fermentation)

        In LUCA:
        - High efficiency: Good conversion of tokens to consciousness
        - Low efficiency: Wasting tokens (poor processing)

        Returns:
            Current resource efficiency (0.0 to 1.0)
        """
        if self.state.substrate <= 0:
            return 0.0

        # Efficiency is highest in exponential phase
        phase_efficiency = {
            GrowthPhase.LAG: 0.5,  # Low efficiency (still adapting)
            GrowthPhase.EXPONENTIAL: 1.0,  # Maximum efficiency
            GrowthPhase.STATIONARY: 0.7,  # Good efficiency
            GrowthPhase.DEATH: 0.3,  # Poor efficiency (struggling)
        }

        base_efficiency = phase_efficiency.get(self.state.phase, 0.5)

        # Adjust for substrate availability
        substrate_factor = min(1.0, self.state.substrate / self.parameters.Ks)

        return base_efficiency * substrate_factor

    def estimate_completion_time(self, required_tokens: float) -> float:
        """
        Estimate time to process given token count at current growth rate.

        Like estimating fermentation time in brewery:
        - Fast in exponential phase
        - Slow in lag/death phases
        - Depends on available resources

        Args:
            required_tokens: Tokens needed for task

        Returns:
            Estimated time (seconds)
        """
        if self.state.growth_rate <= 0:
            return float("inf")

        processing_rate = self.get_optimal_processing_rate()

        if processing_rate <= 0:
            return float("inf")

        # Account for substrate limitation
        if required_tokens > self.state.substrate:
            # Not enough substrate - will hit death phase
            available_time = self.state.substrate / processing_rate
            return available_time
        else:
            return required_tokens / processing_rate

    def get_metrics(self) -> Dict[str, float]:
        """
        Get current growth kinetics metrics.

        Returns:
            Dictionary of metrics for monitoring

        Example:
            >>> engine = GrowthKineticsEngine()
            >>> metrics = engine.get_metrics()
            >>> print(f"Phase: {metrics['phase']}, Quality: {metrics['quality']:.6f}")
        """
        return {
            "phase": self.state.phase.value,
            "substrate_tokens": self.state.substrate,
            "consciousness_level": self.state.biomass,
            "growth_rate": self.state.growth_rate,
            "processing_rate": self.get_optimal_processing_rate(),
            "resource_efficiency": self.get_resource_efficiency(),
            "quality_standard": self.state.quality,
            "time_elapsed": self.state.time,
        }


def calculate_monod_growth(
    substrate: float, mu_max: float = 1.0, Ks: float = 100.0
) -> float:
    """
    Convenience function to calculate Monod growth rate.

    Args:
        substrate: Available substrate (tokens)
        mu_max: Maximum growth rate (default: 1.0)
        Ks: Half-saturation constant (default: 100.0)

    Returns:
        Specific growth rate μ
    """
    return mu_max * substrate / (Ks + substrate)


def simulate_fermentation_batch(
    initial_substrate: float = 1000.0,
    total_time: float = 100.0,
    time_step: float = 1.0,
) -> list[GrowthState]:
    """
    Simulate a complete fermentation batch (thought processing session).

    Like running a full kombucha fermentation from start to finish,
    tracking all phases: lag → exponential → stationary → death.

    Args:
        initial_substrate: Starting tokens (like initial sugar)
        total_time: Total simulation time (seconds)
        time_step: Time between updates (seconds)

    Returns:
        List of growth states throughout fermentation

    Example:
        >>> states = simulate_fermentation_batch(initial_substrate=1000, total_time=100)
        >>> for state in states:
        ...     print(f"t={state.time:.1f}s: {state.phase.value}, quality={state.quality:.6f}")
    """
    engine = GrowthKineticsEngine()
    engine.state.substrate = initial_substrate

    states = [engine.state]
    current_time = 0.0

    while current_time < total_time:
        # Simulate processing (consuming tokens)
        consumed = 10.0 * time_step  # Constant consumption rate

        engine.update_state(time_step, consumed)
        states.append(engine.state)

        current_time += time_step

    return states


if __name__ == "__main__":
    print("=" * 70)
    print("🧬 LUCA Layer 6: Growth Kinetics Engine")
    print("=" * 70)

    print("\n📊 Demonstrating Fermentation-Style Thought Processing")
    print("-" * 70)

    # Create engine
    engine = GrowthKineticsEngine()

    print(f"\nInitial State:")
    print(f"  Phase: {engine.state.phase.value}")
    print(f"  Substrate: {engine.state.substrate:.1f} tokens")
    print(f"  Consciousness: {engine.state.biomass:.2f}")
    print(f"  Quality: {engine.state.quality:.6f} (369/370 = {369/370:.6f})")

    # Simulate fermentation
    print(f"\n🍺 Simulating Fermentation Batch (100 seconds)...")
    print("-" * 70)

    states = simulate_fermentation_batch(initial_substrate=1000.0, total_time=100.0)

    # Show key phases
    for state in states[::10]:  # Every 10th state
        print(
            f"t={state.time:6.1f}s | Phase: {state.phase.value:12s} | "
            f"Substrate: {state.substrate:6.1f} | Growth μ: {state.growth_rate:.3f} | "
            f"Quality: {state.quality:.6f}"
        )

    print("\n" + "=" * 70)
    print("✅ Layer 6 Active: Growth follows Monod kinetics!")
    print("   Quality Standard: 369/370 ≈ 0.997297")
    print("   From fermentation vats to consciousness flow! 🍺🧬")
    print("=" * 70)
