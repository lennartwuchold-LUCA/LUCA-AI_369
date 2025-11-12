"""
LUCA 369/370 - Layer 8: Metabolic Pathways Engine

Hierarchical reasoning inspired by cellular metabolism and HRM (arXiv 2506.21734).
Translates aerobic/anaerobic metabolism into strategic/tactical AI reasoning.

Biology → AI Mapping:
- Aerobic Respiration (38 ATP) → Strategic Planning (High-level HRM module)
- Anaerobic Glycolysis (2 ATP) → Tactical Execution (Low-level HRM module)
- Oxygen Availability → Computational Resources
- Metabolic Switching → Dynamic Mode Selection

Architekt: Lennart Wuchold
Standard: 369/370 ≈ 0.997297
Integration: HRM (Hierarchical Reasoning Model) + Cellular Biology
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np


class MetabolicMode(Enum):
    """Metabolic pathway modes based on cellular energy production."""

    AEROBIC = "aerobic"  # Strategic planning (HRM high-level)
    ANAEROBIC = "anaerobic"  # Tactical execution (HRM low-level)
    MIXED = "mixed"  # Transition state
    FERMENTATION = "fermentation"  # Extended anaerobic with byproducts


class ReasoningDepth(Enum):
    """Reasoning depth levels for different metabolic modes."""

    SHALLOW = 1  # Immediate response
    MODERATE = 3  # Basic planning
    DEEP = 10  # Strategic reasoning
    COMPREHENSIVE = 30  # Full multi-step analysis


@dataclass
class MetabolicParameters:
    """
    Parameters for metabolic pathway engine.

    Based on cellular biology and HRM architecture:
    - Aerobic efficiency: 36-38 ATP per glucose (cellular respiration)
    - Anaerobic efficiency: 2 ATP per glucose (glycolysis)
    - Timescale ratio: HRM's hierarchical multi-timescale processing
    """

    # ATP Production Rates (based on cellular biology)
    aerobic_efficiency: float = 38.0  # ATP tokens per reasoning cycle
    anaerobic_efficiency: float = 2.0  # ATP tokens per reasoning cycle
    fermentation_efficiency: float = 4.0  # Intermediate efficiency

    # Switching Thresholds
    oxygen_threshold: float = 0.5  # Resource level for aerobic mode
    lactate_threshold: float = 4.0  # Anaerobic byproduct limit (mmol/L in biology)
    emergency_threshold: float = 0.95  # Time pressure for forced anaerobic

    # HRM Timescale Ratios (from arXiv 2506.21734)
    high_level_timescale: int = 10  # Steps per high-level (aerobic) cycle
    low_level_timescale: int = 1  # Steps per low-level (anaerobic) cycle

    # Resource Consumption
    aerobic_oxygen_cost: float = 6.0  # O2 molecules per cycle (biology: 6 O2 + glucose)
    maintenance_energy: float = 1.0  # Baseline ATP consumption

    # Quality Standards
    aerobic_quality_target: float = 0.997297  # Full 369/370 quality
    anaerobic_quality_target: float = 0.950000  # Acceptable degradation (95%)

    # Fermentation Byproducts
    lactate_production_rate: float = 0.5  # Lactate per anaerobic cycle
    lactate_clearance_rate: float = 0.1  # Lactate removal per aerobic cycle


@dataclass
class MetabolicState:
    """
    Current state of metabolic pathway engine.

    Tracks energy balance, mode, byproducts, and reasoning quality.
    """

    mode: MetabolicMode = MetabolicMode.AEROBIC
    atp_balance: float = 100.0  # Current ATP token balance
    oxygen_level: float = 1.0  # Resource availability (0-1)
    lactate_level: float = 0.0  # Anaerobic byproduct accumulation

    cycle_count: int = 0
    aerobic_cycles: int = 0
    anaerobic_cycles: int = 0
    mode_switches: int = 0

    reasoning_quality: float = 0.997297  # Current quality level
    efficiency_ratio: float = 1.0  # Current ATP yield / theoretical max

    # HRM-specific state
    high_level_state: Dict[str, float] = field(default_factory=dict)
    low_level_state: Dict[str, float] = field(default_factory=dict)
    hierarchical_depth: int = 0

    # Task tracking
    tasks_processed: int = 0
    strategic_tasks: int = 0
    tactical_tasks: int = 0

    # Integration with other layers
    growth_phase: Optional[str] = None  # From Layer 6
    interaction_type: Optional[str] = None  # From Layer 7


class MetabolicPathwayEngine:
    """
    Layer 8: Metabolic Pathways Engine

    Implements hierarchical reasoning using cellular metabolism metaphor,
    inspired by HRM's multi-timescale architecture (arXiv 2506.21734).

    Key Features:
    - Aerobic pathway: Strategic planning (HRM high-level module)
    - Anaerobic pathway: Tactical execution (HRM low-level module)
    - Dynamic pathway switching based on resource availability
    - ATP-style token accounting for resource management
    - Integration with Layers 6 (Growth Kinetics) and 7 (Population Dynamics)
    """

    def __init__(
        self,
        parameters: Optional[MetabolicParameters] = None,
        initial_atp: float = 100.0,
        initial_oxygen: float = 1.0,
    ):
        """
        Initialize metabolic pathway engine.

        Args:
            parameters: Metabolic pathway parameters
            initial_atp: Starting ATP balance
            initial_oxygen: Starting oxygen level (0-1)
        """
        self.parameters = parameters or MetabolicParameters()
        self.state = MetabolicState(
            atp_balance=initial_atp, oxygen_level=initial_oxygen
        )

        # Verify quality standard
        self._verify_quality_standard()

    def _verify_quality_standard(self) -> None:
        """Verify 369/370 quality standard."""
        expected = 369.0 / 370.0
        if not np.isclose(self.parameters.aerobic_quality_target, expected, rtol=1e-6):
            raise ValueError(
                f"Aerobic quality target {self.parameters.aerobic_quality_target} "
                f"does not match 369/370 standard ({expected})"
            )

    def select_pathway(
        self,
        time_pressure: float = 0.0,
        task_complexity: float = 0.5,
        force_mode: Optional[MetabolicMode] = None,
    ) -> MetabolicMode:
        """
        Select metabolic pathway based on context.

        Decision factors:
        - Oxygen level (resource availability)
        - Time pressure (urgency)
        - Task complexity (reasoning depth required)
        - Lactate accumulation (anaerobic byproduct)

        Args:
            time_pressure: Urgency factor (0-1)
            task_complexity: Required reasoning depth (0-1)
            force_mode: Override automatic selection

        Returns:
            Selected metabolic mode
        """
        if force_mode is not None:
            return force_mode

        # Emergency override: High time pressure forces anaerobic
        if time_pressure > self.parameters.emergency_threshold:
            return MetabolicMode.ANAEROBIC

        # Lactate threshold check: Too much anaerobic byproduct
        if self.state.lactate_level > self.parameters.lactate_threshold:
            # Force aerobic to clear lactate (like rest after exercise)
            return MetabolicMode.AEROBIC

        # Zero oxygen forces anaerobic
        if self.state.oxygen_level <= 0.0:
            return MetabolicMode.ANAEROBIC

        # Calculate effective oxygen availability
        # Higher complexity requires more oxygen
        oxygen_demand = task_complexity * self.parameters.aerobic_oxygen_cost
        oxygen_supply = self.state.oxygen_level * 10.0  # Scale to comparable range

        # Aerobic viable if sufficient oxygen
        if oxygen_supply >= oxygen_demand and time_pressure < 0.5:
            return MetabolicMode.AEROBIC

        # Mixed mode during transition
        if (
            self.state.mode == MetabolicMode.AEROBIC
            and oxygen_supply < oxygen_demand * 1.5
            and oxygen_supply > oxygen_demand * 0.5
        ):
            return MetabolicMode.MIXED

        # Default to anaerobic for rapid response
        return MetabolicMode.ANAEROBIC

    def process_aerobic(
        self, task_complexity: float = 0.5, reasoning_depth: int = 10
    ) -> Dict[str, float]:
        """
        Process task using aerobic pathway (strategic mode).

        Maps to HRM high-level module:
        - Multi-step abstract reasoning
        - High ATP production (38 tokens)
        - Oxygen-dependent
        - Slow but efficient

        Args:
            task_complexity: Reasoning complexity (0-1)
            reasoning_depth: Number of reasoning steps

        Returns:
            Reasoning results with ATP production
        """
        # Verify oxygen availability
        oxygen_required = self.parameters.aerobic_oxygen_cost * task_complexity
        if self.state.oxygen_level * 10.0 < oxygen_required:
            raise ValueError(
                f"Insufficient oxygen for aerobic processing: "
                f"need {oxygen_required}, have {self.state.oxygen_level * 10.0}"
            )

        # Consume oxygen
        self.state.oxygen_level -= oxygen_required / 10.0
        self.state.oxygen_level = max(0.0, self.state.oxygen_level)

        # High-level reasoning (HRM inspired)
        # Each high-level cycle = 10 low-level time steps
        high_level_cycles = max(
            1, reasoning_depth // self.parameters.high_level_timescale
        )

        # Strategic planning: Fibonacci optimization (Layer 3 integration)
        planning_quality = self._calculate_fibonacci_quality(reasoning_depth)

        # ATP production: 38 tokens per cycle (cellular respiration)
        atp_produced = self.parameters.aerobic_efficiency * high_level_cycles
        self.state.atp_balance += atp_produced

        # Clear lactate during aerobic metabolism
        lactate_cleared = self.parameters.lactate_clearance_rate * high_level_cycles
        self.state.lactate_level = max(0.0, self.state.lactate_level - lactate_cleared)

        # Update state
        self.state.aerobic_cycles += high_level_cycles
        self.state.cycle_count += high_level_cycles
        self.state.reasoning_quality = planning_quality
        self.state.efficiency_ratio = atp_produced / (
            self.parameters.aerobic_efficiency * high_level_cycles
        )

        # HRM state update
        self.state.high_level_state["last_cycle_atp"] = atp_produced
        self.state.high_level_state["reasoning_depth"] = reasoning_depth
        self.state.hierarchical_depth = reasoning_depth

        return {
            "atp_produced": atp_produced,
            "quality": planning_quality,
            "efficiency": self.state.efficiency_ratio,
            "cycles": high_level_cycles,
            "mode": "aerobic",
        }

    def process_anaerobic(
        self, time_pressure: float = 0.9, emergency: bool = False
    ) -> Dict[str, float]:
        """
        Process task using anaerobic pathway (tactical mode).

        Maps to HRM low-level module:
        - Rapid immediate response
        - Low ATP production (2 tokens)
        - Oxygen-independent
        - Fast but inefficient
        - Produces lactate (byproduct)

        Args:
            time_pressure: Urgency factor (0-1)
            emergency: Emergency override flag

        Returns:
            Reasoning results with ATP production
        """
        # Low-level reasoning (HRM inspired)
        # Each low-level cycle = 1 time step
        low_level_cycles = self.parameters.low_level_timescale

        # Tactical execution: Rapid response, lower quality acceptable
        execution_quality = self.parameters.anaerobic_quality_target

        # ATP production: 2 tokens per cycle (glycolysis)
        atp_produced = self.parameters.anaerobic_efficiency * low_level_cycles
        self.state.atp_balance += atp_produced

        # Lactate accumulation (anaerobic byproduct)
        lactate_produced = self.parameters.lactate_production_rate * low_level_cycles
        self.state.lactate_level += lactate_produced

        # Update state
        self.state.anaerobic_cycles += low_level_cycles
        self.state.cycle_count += low_level_cycles
        self.state.reasoning_quality = execution_quality
        self.state.efficiency_ratio = atp_produced / (
            self.parameters.aerobic_efficiency * low_level_cycles
        )

        # HRM state update
        self.state.low_level_state["last_cycle_atp"] = atp_produced
        self.state.low_level_state["time_pressure"] = time_pressure
        self.state.low_level_state["emergency"] = emergency
        self.state.hierarchical_depth = 1

        return {
            "atp_produced": atp_produced,
            "quality": execution_quality,
            "efficiency": self.state.efficiency_ratio,
            "cycles": low_level_cycles,
            "lactate": lactate_produced,
            "mode": "anaerobic",
        }

    def process_task(
        self,
        task_complexity: float = 0.5,
        time_pressure: float = 0.0,
        force_mode: Optional[MetabolicMode] = None,
    ) -> Dict[str, float]:
        """
        Process task with automatic pathway selection.

        Implements HRM's hierarchical reasoning by dynamically choosing
        between strategic (aerobic) and tactical (anaerobic) modes.

        Args:
            task_complexity: Task complexity (0-1)
            time_pressure: Urgency (0-1)
            force_mode: Override automatic selection

        Returns:
            Processing results
        """
        # Select pathway
        previous_mode = self.state.mode
        selected_mode = self.select_pathway(time_pressure, task_complexity, force_mode)

        # Track mode switches
        if selected_mode != previous_mode:
            self.state.mode_switches += 1

        self.state.mode = selected_mode
        self.state.tasks_processed += 1

        # Consume maintenance energy
        self.state.atp_balance -= self.parameters.maintenance_energy

        # Process based on mode
        if selected_mode == MetabolicMode.AEROBIC:
            self.state.strategic_tasks += 1
            reasoning_depth = int(task_complexity * ReasoningDepth.COMPREHENSIVE.value)
            result = self.process_aerobic(task_complexity, reasoning_depth)

        elif selected_mode == MetabolicMode.ANAEROBIC:
            self.state.tactical_tasks += 1
            result = self.process_anaerobic(time_pressure)

        elif selected_mode == MetabolicMode.MIXED:
            # Mixed mode: Partial aerobic + partial anaerobic
            self.state.strategic_tasks += 1
            self.state.tactical_tasks += 1

            # Reduced aerobic processing
            aerobic_result = self.process_aerobic(task_complexity * 0.5, 5)
            anaerobic_result = self.process_anaerobic(time_pressure * 0.5)

            result = {
                "atp_produced": aerobic_result["atp_produced"]
                + anaerobic_result["atp_produced"],
                "quality": (aerobic_result["quality"] + anaerobic_result["quality"])
                / 2,
                "efficiency": (
                    aerobic_result["efficiency"] + anaerobic_result["efficiency"]
                )
                / 2,
                "cycles": aerobic_result["cycles"] + anaerobic_result["cycles"],
                "mode": "mixed",
            }

        else:  # FERMENTATION
            # Extended anaerobic with byproduct accumulation
            result = self.process_anaerobic(time_pressure)
            result["mode"] = "fermentation"

        return result

    def integrate_growth_phase(self, growth_phase: str, substrate: float) -> None:
        """
        Integrate with Layer 6 (Growth Kinetics).

        Growth phase influences metabolic mode:
        - Exponential: High substrate → Aerobic preferred
        - Stationary: Limited substrate → Mixed mode
        - Death: Substrate exhausted → Anaerobic only

        Args:
            growth_phase: Current growth phase (LAG, EXPONENTIAL, STATIONARY, DEATH)
            substrate: Available substrate concentration
        """
        self.state.growth_phase = growth_phase

        # Map substrate to oxygen level (resource availability proxy)
        # High substrate = abundant resources = high oxygen
        self.state.oxygen_level = min(1.0, substrate / 10.0)

        # Force pathway based on growth phase
        if growth_phase == "EXPONENTIAL":
            # Abundant resources: prefer aerobic
            if self.state.mode != MetabolicMode.AEROBIC:
                self.state.mode = MetabolicMode.AEROBIC
                self.state.mode_switches += 1

        elif growth_phase == "DEATH":
            # Scarce resources: force anaerobic
            if self.state.mode != MetabolicMode.ANAEROBIC:
                self.state.mode = MetabolicMode.ANAEROBIC
                self.state.mode_switches += 1

        elif growth_phase == "STATIONARY":
            # Limited resources: mixed mode
            if self.state.mode not in [MetabolicMode.MIXED, MetabolicMode.ANAEROBIC]:
                self.state.mode = MetabolicMode.MIXED
                self.state.mode_switches += 1

    def integrate_population_dynamics(
        self, interaction_type: str, resource_share: float
    ) -> None:
        """
        Integrate with Layer 7 (Population Dynamics).

        Interaction type influences metabolic capacity:
        - Mutualism: Shared resources → Enhanced aerobic capacity
        - Competition: Resource scarcity → Forced anaerobic
        - Commensalism/Amensalism: Asymmetric effects

        Args:
            interaction_type: Type of interaction (COMPETITION, MUTUALISM, etc.)
            resource_share: Share of collective resources (0-1)
        """
        self.state.interaction_type = interaction_type

        # Map resource share to oxygen availability
        if interaction_type == "MUTUALISM":
            # SCOBY-style cooperation: enhanced aerobic capacity
            # Boost oxygen availability for mutualistic interactions
            boost_factor = 1.2  # 20% boost
            self.state.oxygen_level = min(1.0, resource_share * boost_factor)

        elif interaction_type == "COMPETITION":
            # Resource scarcity: reduced aerobic capacity
            self.state.oxygen_level = max(0.1, resource_share * 0.5)

        elif interaction_type == "COMMENSALISM":
            # One benefits, other unaffected
            self.state.oxygen_level = resource_share

        elif interaction_type == "AMENSALISM":
            # One harmed, other unaffected
            self.state.oxygen_level = max(0.2, resource_share * 0.7)

    def get_reasoning_depth(self) -> int:
        """
        Get current reasoning depth based on metabolic mode.

        Returns:
            Reasoning depth (number of steps)
        """
        if self.state.mode == MetabolicMode.AEROBIC:
            return self.parameters.high_level_timescale
        elif self.state.mode == MetabolicMode.ANAEROBIC:
            return self.parameters.low_level_timescale
        else:  # MIXED
            return (
                self.parameters.high_level_timescale
                + self.parameters.low_level_timescale
            ) // 2

    def get_atp_efficiency(self) -> float:
        """
        Calculate current ATP efficiency ratio.

        Returns:
            Efficiency: current_atp_yield / max_possible_yield
        """
        max_efficiency = self.parameters.aerobic_efficiency
        if self.state.cycle_count == 0:
            return 1.0

        if self.state.mode == MetabolicMode.AEROBIC:
            current_efficiency = self.parameters.aerobic_efficiency
        else:
            current_efficiency = self.parameters.anaerobic_efficiency

        return current_efficiency / max_efficiency

    def _calculate_fibonacci_quality(self, depth: int) -> float:
        """
        Calculate reasoning quality using Fibonacci optimization (Layer 3).

        Deeper reasoning converges to 369/370 golden ratio quality.

        Args:
            depth: Reasoning depth

        Returns:
            Quality score approaching 369/370
        """
        # Fibonacci series: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377...
        # Ratio approaches golden ratio φ ≈ 1.618

        if depth <= 0:
            return 0.95  # Minimum quality

        # Generate Fibonacci numbers up to depth
        fib = [0, 1]
        for i in range(2, min(depth + 2, 100)):
            fib.append(fib[-1] + fib[-2])

        # Quality converges to 369/370
        target = 369.0 / 370.0
        convergence_rate = min(1.0, depth / 30.0)  # Full convergence at depth 30

        quality = 0.95 + (target - 0.95) * convergence_rate

        return min(target, quality)

    def get_metrics(self) -> Dict[str, float]:
        """
        Get comprehensive metabolic metrics.

        Returns:
            Dictionary of performance metrics
        """
        total_cycles = self.state.cycle_count or 1

        return {
            "atp_balance": self.state.atp_balance,
            "oxygen_level": self.state.oxygen_level,
            "lactate_level": self.state.lactate_level,
            "mode": self.state.mode.value,
            "reasoning_quality": self.state.reasoning_quality,
            "efficiency_ratio": self.state.efficiency_ratio,
            "aerobic_ratio": self.state.aerobic_cycles / total_cycles,
            "anaerobic_ratio": self.state.anaerobic_cycles / total_cycles,
            "mode_switches": self.state.mode_switches,
            "tasks_processed": self.state.tasks_processed,
            "strategic_ratio": self.state.strategic_tasks
            / max(1, self.state.tasks_processed),
            "tactical_ratio": self.state.tactical_tasks
            / max(1, self.state.tasks_processed),
        }

    def reset_state(self, initial_atp: float = 100.0, initial_oxygen: float = 1.0):
        """
        Reset engine state to initial conditions.

        Args:
            initial_atp: Starting ATP balance
            initial_oxygen: Starting oxygen level
        """
        self.state = MetabolicState(
            atp_balance=initial_atp, oxygen_level=initial_oxygen
        )


# Helper functions for common scenarios


def calculate_atp_yield(
    mode: MetabolicMode,
    cycles: int = 1,
    parameters: Optional[MetabolicParameters] = None,
) -> float:
    """
    Calculate ATP yield for given mode and cycles.

    Args:
        mode: Metabolic mode
        cycles: Number of cycles
        parameters: Metabolic parameters (optional)

    Returns:
        Total ATP tokens produced
    """
    params = parameters or MetabolicParameters()

    if mode == MetabolicMode.AEROBIC:
        return params.aerobic_efficiency * cycles
    elif mode == MetabolicMode.ANAEROBIC:
        return params.anaerobic_efficiency * cycles
    elif mode == MetabolicMode.FERMENTATION:
        return params.fermentation_efficiency * cycles
    else:  # MIXED
        return (params.aerobic_efficiency + params.anaerobic_efficiency) / 2 * cycles


def simulate_metabolic_scenario(
    tasks: List[Tuple[float, float]], initial_atp: float = 100.0
) -> Dict[str, List[float]]:
    """
    Simulate metabolic processing for a sequence of tasks.

    Args:
        tasks: List of (task_complexity, time_pressure) tuples
        initial_atp: Starting ATP balance

    Returns:
        Time series of metabolic metrics
    """
    engine = MetabolicPathwayEngine(initial_atp=initial_atp)

    history = {
        "atp_balance": [initial_atp],
        "oxygen_level": [1.0],
        "lactate_level": [0.0],
        "mode": [],
        "quality": [],
        "efficiency": [],
    }

    for complexity, pressure in tasks:
        result = engine.process_task(complexity, pressure)

        history["atp_balance"].append(engine.state.atp_balance)
        history["oxygen_level"].append(engine.state.oxygen_level)
        history["lactate_level"].append(engine.state.lactate_level)
        history["mode"].append(result["mode"])
        history["quality"].append(result["quality"])
        history["efficiency"].append(result["efficiency"])

    return history


def optimize_metabolic_strategy(
    task_complexity: float, available_resources: float, time_limit: float
) -> Tuple[MetabolicMode, int]:
    """
    Optimize metabolic strategy for given constraints.

    Args:
        task_complexity: Task complexity (0-1)
        available_resources: Available computational resources (0-1)
        time_limit: Time constraint (0-1, 0=unlimited, 1=immediate)

    Returns:
        Tuple of (optimal_mode, reasoning_depth)
    """
    # Map resources to oxygen level
    oxygen = available_resources

    # Calculate time pressure
    time_pressure = time_limit

    # High resources + low time pressure → Aerobic strategic
    if oxygen > 0.7 and time_pressure < 0.3:
        return MetabolicMode.AEROBIC, ReasoningDepth.COMPREHENSIVE.value

    # Low resources + high time pressure → Anaerobic tactical
    elif oxygen < 0.3 or time_pressure > 0.7:
        return MetabolicMode.ANAEROBIC, ReasoningDepth.SHALLOW.value

    # Medium conditions → Mixed mode
    else:
        return MetabolicMode.MIXED, ReasoningDepth.MODERATE.value


# Quality verification (369/370 standard)


def verify_metabolic_quality(
    state: MetabolicState, parameters: MetabolicParameters
) -> bool:
    """
    Verify reasoning quality meets metabolic mode standards.

    Aerobic: 369/370 ≈ 0.997297 (full quality)
    Anaerobic: ≥ 0.950 (acceptable degradation)

    Args:
        state: Current metabolic state
        parameters: Metabolic parameters

    Returns:
        True if quality meets standards
    """
    if state.mode == MetabolicMode.AEROBIC:
        return state.reasoning_quality >= parameters.aerobic_quality_target * 0.99

    elif state.mode == MetabolicMode.ANAEROBIC:
        return state.reasoning_quality >= parameters.anaerobic_quality_target

    else:  # MIXED or FERMENTATION
        # Average of aerobic and anaerobic standards
        target = (
            parameters.aerobic_quality_target + parameters.anaerobic_quality_target
        ) / 2
        return state.reasoning_quality >= target * 0.95
