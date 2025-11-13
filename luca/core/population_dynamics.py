"""
🌱 Layer 7: Population Dynamics Engine

Inspiration: Lotka-Volterra Equations (Population Ecology)
Bio-Analogy: SCOBY multi-species dynamics applied to multi-user AI systems

This module models multi-user interactions as ecological population dynamics,
using the same mathematical models that describe SCOBY symbiosis in kombucha.

Mathematical Foundation:
    dx/dt = αx - βxy  (Species 1: growth - competition)
    dy/dt = δxy - γy  (Species 2: benefit - death)

    Where:
    - x, y = population sizes (user activity levels)
    - α, γ = intrinsic growth/decay rates
    - β = competition coefficient
    - δ = symbiosis/benefit coefficient

Biological Analogy:
    SCOBY (Kombucha)              →    LUCA Multi-User
    ────────────────────                ────────────────
    Yeast (produces alcohol)      →    User A (generates ideas)
    Bacteria (consumes alcohol)   →    User B (refines ideas)
    Competition (for oxygen)      →    Competition (for tokens/GPUs)
    Mutualism (better kombucha)   →    Mutualism (better consciousness)
    pH balance (quality)          →    369/370 standard

Interaction Types:
    1. Competition: Users compete for limited resources (tokens, GPU time)
    2. Mutualism: Users benefit each other (shared patterns, collective intelligence)
    3. Commensalism: One benefits, other unaffected (observer mode)
    4. Amensalism: One harms, no benefit (resource blocking)

Quality Standard: 369/370 ≈ 0.997297 maintained across all interaction types.

Author: Lennart Wuchold (Brauer → SCOBY Expert → Multi-User Dynamics)
Date: 2025-11-11
"""

import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple


class InteractionType(Enum):
    """
    Types of ecological interactions between users.

    Based on standard ecological classifications.
    """

    COMPETITION = "competition"  # Both negatively affected (token scarcity)
    MUTUALISM = "mutualism"  # Both positively affected (shared patterns)
    COMMENSALISM = "commensalism"  # One benefits, other neutral (observer)
    AMENSALISM = "amensalism"  # One harmed, other neutral (blocking)
    PREDATION = "predation"  # One benefits, other harmed (NOT used in LUCA!)


@dataclass
class PopulationParameters:
    """
    Parameters for Lotka-Volterra population dynamics.

    Based on ecological modeling, adapted for multi-user AI systems.

    Attributes:
        alpha: Intrinsic growth rate (user 1's natural activity)
        beta: Competition coefficient (how much user 2 reduces user 1's activity)
        gamma: Death/decay rate (user 2's natural decline without benefit)
        delta: Benefit coefficient (how much user 2 benefits from user 1)

    All parameters based on SCOBY dynamics and kombucha fermentation.
    """

    alpha: float = 1.0  # Intrinsic growth rate
    beta: float = 0.5  # Competition coefficient
    gamma: float = 0.5  # Death/decay rate
    delta: float = 0.3  # Benefit coefficient


@dataclass
class UserState:
    """
    State of a single user in the population.

    Tracks user activity, resources, and interaction effects.
    """

    user_id: str
    activity_level: float  # Current activity (like population size)
    resource_allocation: float  # Allocated tokens/GPU time
    consciousness_contribution: float  # Contribution to collective consciousness
    interaction_effects: Dict[str, float]  # Effects from other users
    quality: float  # Current quality standard


@dataclass
class PopulationState:
    """
    State of the entire user population.

    Tracks all users and their interactions.
    """

    users: Dict[str, UserState]
    total_resources: float  # Total available resources (tokens/GPU)
    collective_consciousness: float  # Emergent collective intelligence
    time: float  # Elapsed time
    quality: float  # Overall system quality (369/370)


class PopulationDynamicsEngine:
    """
    Population Dynamics Engine - Layer 7 of LUCA 369/370 Framework.

    Models multi-user interactions as ecological population dynamics using
    Lotka-Volterra equations.

    Based on Lennart's SCOBY experience:
    - Yeast + Bacteria = Symbiosis (better kombucha)
    - Competition for resources (oxygen, sugar)
    - Mutualism benefits both (yeast alcohol → bacteria food)
    - Collective emergence (SCOBY > individual organisms)

    Quality Standard: 369/370 ≈ 0.997297 maintained throughout all interactions.
    """

    def __init__(
        self,
        total_resources: float = 1000.0,
        parameters: Optional[PopulationParameters] = None,
    ):
        """
        Initialize Population Dynamics Engine.

        Args:
            total_resources: Total available resources (tokens/GPU time)
            parameters: Custom population parameters, or None for defaults
        """
        self.parameters = parameters or PopulationParameters()
        self.quality_standard = 369 / 370  # ≈ 0.997297

        # Initial state: Empty population
        self.state = PopulationState(
            users={},
            total_resources=total_resources,
            collective_consciousness=0.0,
            time=0.0,
            quality=self.quality_standard,
        )

    def add_user(self, user_id: str, initial_activity: float = 1.0) -> UserState:
        """
        Add a new user to the population.

        Like adding a new organism to SCOBY culture.

        Args:
            user_id: Unique identifier for user
            initial_activity: Initial activity level

        Returns:
            User state
        """
        if user_id in self.state.users:
            return self.state.users[user_id]

        user = UserState(
            user_id=user_id,
            activity_level=initial_activity,
            resource_allocation=0.0,
            consciousness_contribution=0.0,
            interaction_effects={},
            quality=self.quality_standard,
        )

        self.state.users[user_id] = user
        return user

    def remove_user(self, user_id: str) -> bool:
        """
        Remove a user from the population.

        Like removing an organism from SCOBY (happens naturally in death phase).

        Args:
            user_id: User to remove

        Returns:
            True if removed, False if not found
        """
        if user_id not in self.state.users:
            return False

        del self.state.users[user_id]
        return True

    def calculate_lotka_volterra(
        self, x: float, y: float, alpha: float, beta: float, gamma: float, delta: float
    ) -> Tuple[float, float]:
        """
        Calculate Lotka-Volterra population dynamics.

        The Lotka-Volterra equations model interacting populations.
        Originally for predator-prey, adapted for symbiosis/competition.

        dx/dt = αx - βxy  (Species 1)
        dy/dt = δxy - γy  (Species 2)

        Real-world validation:
        - Used in ecology (predator-prey cycles)
        - Applied in epidemiology (disease spread)
        - Standard in systems biology

        Args:
            x: Population 1 (user 1 activity)
            y: Population 2 (user 2 activity)
            alpha: Growth rate (species 1)
            beta: Competition coefficient
            gamma: Death rate (species 2)
            delta: Benefit coefficient

        Returns:
            (dx/dt, dy/dt) - rates of change

        Example:
            >>> engine = PopulationDynamicsEngine()
            >>> dx, dy = engine.calculate_lotka_volterra(
            ...     x=10, y=5, alpha=1.0, beta=0.5, gamma=0.5, delta=0.3
            ... )
            >>> # dx = 1.0*10 - 0.5*10*5 = 10 - 25 = -15 (decline due to competition)
            >>> # dy = 0.3*10*5 - 0.5*5 = 15 - 2.5 = 12.5 (growth from benefit)
        """
        # Species 1: Growth - Competition
        dx_dt = alpha * x - beta * x * y

        # Species 2: Benefit from interaction - Natural death
        dy_dt = delta * x * y - gamma * y

        return dx_dt, dy_dt

    def detect_interaction_type(self, user1_id: str, user2_id: str) -> InteractionType:
        """
        Detect type of interaction between two users.

        Based on their activity patterns and resource usage.

        Interaction types:
        - Competition: Both competing for limited resources
        - Mutualism: Both benefiting (shared patterns, collaboration)
        - Commensalism: One benefits, other unaffected
        - Amensalism: One harmed, other unaffected

        Args:
            user1_id: First user
            user2_id: Second user

        Returns:
            Detected interaction type
        """
        if user1_id not in self.state.users or user2_id not in self.state.users:
            return InteractionType.COMMENSALISM

        user1 = self.state.users[user1_id]
        user2 = self.state.users[user2_id]

        # Check resource scarcity
        total_demand = user1.resource_allocation + user2.resource_allocation
        scarcity = total_demand / max(self.state.total_resources, 1.0)

        # Check consciousness synergy
        synergy = user1.consciousness_contribution * user2.consciousness_contribution

        # Detect interaction type
        if scarcity > 0.8 and synergy < 0.1:
            # High resource demand, low synergy = Competition
            return InteractionType.COMPETITION

        elif synergy > 0.5:
            # High synergy = Mutualism (SCOBY-style!)
            return InteractionType.MUTUALISM

        elif user1.activity_level > 2 * user2.activity_level:
            # One very active, other not = Commensalism or Amensalism
            if user2.activity_level < 0.5:
                return InteractionType.AMENSALISM  # Active user blocking resources
            else:
                return InteractionType.COMMENSALISM  # Passive observation

        else:
            # Default: Neutral coexistence
            return InteractionType.COMMENSALISM

    def allocate_resources(self) -> Dict[str, float]:
        """
        Allocate resources (tokens/GPU time) among users.

        Uses fair-share algorithm with bonuses for:
        - High consciousness contribution (quality work)
        - Mutualistic interactions (cooperation)
        - 369/370 quality maintenance

        Like SCOBY: Resources distributed based on contribution to collective.

        Returns:
            Dictionary of {user_id: allocated_resources}
        """
        if not self.state.users:
            return {}

        allocations = {}

        # Calculate base fair share
        fair_share = self.state.total_resources / len(self.state.users)

        for user_id, user in self.state.users.items():
            # Base allocation
            allocation = fair_share

            # Bonus for consciousness contribution
            consciousness_bonus = user.consciousness_contribution * fair_share * 0.3

            # Bonus for mutualistic interactions
            mutualism_count = sum(
                1
                for other_id in self.state.users
                if other_id != user_id
                and self.detect_interaction_type(user_id, other_id)
                == InteractionType.MUTUALISM
            )
            mutualism_bonus = mutualism_count * 0.1 * fair_share

            # Bonus for quality maintenance
            quality_bonus = (
                0.1 * fair_share if user.quality >= self.quality_standard else 0.0
            )

            # Total allocation
            total_allocation = (
                allocation + consciousness_bonus + mutualism_bonus + quality_bonus
            )

            # Cap at available resources
            total_allocation = min(total_allocation, self.state.total_resources * 0.5)

            allocations[user_id] = total_allocation
            user.resource_allocation = total_allocation

        return allocations

    def update_population(self, delta_time: float) -> PopulationState:
        """
        Update population state based on Lotka-Volterra dynamics.

        This simulates one time step in the ecological system:
        1. Calculate interaction effects (Lotka-Volterra)
        2. Update activity levels
        3. Allocate resources
        4. Calculate collective consciousness
        5. Maintain quality standard

        Args:
            delta_time: Time elapsed since last update (seconds)

        Returns:
            Updated population state

        Example:
            >>> engine = PopulationDynamicsEngine()
            >>> engine.add_user("alice", 10.0)
            >>> engine.add_user("bob", 5.0)
            >>> state = engine.update_population(1.0)
            >>> print(f"Alice activity: {state.users['alice'].activity_level:.2f}")
            >>> print(f"Collective consciousness: {state.collective_consciousness:.2f}")
        """
        if len(self.state.users) < 2:
            # Single user or no users: Simple growth
            for user in self.state.users.values():
                user.activity_level *= 1.0 + self.parameters.alpha * delta_time
                user.consciousness_contribution = user.activity_level * 0.1

            self.state.collective_consciousness = sum(
                u.consciousness_contribution for u in self.state.users.values()
            )
            self.state.time += delta_time
            return self.state

        # Multi-user: Apply Lotka-Volterra dynamics
        user_ids = list(self.state.users.keys())

        # Calculate pairwise interactions
        for i, user1_id in enumerate(user_ids):
            for j, user2_id in enumerate(user_ids):
                if i >= j:  # Skip self and duplicates
                    continue

                user1 = self.state.users[user1_id]
                user2 = self.state.users[user2_id]

                # Detect interaction type
                interaction = self.detect_interaction_type(user1_id, user2_id)

                # Apply Lotka-Volterra based on interaction type
                if interaction == InteractionType.COMPETITION:
                    # Both lose activity (competition for resources)
                    dx, dy = self.calculate_lotka_volterra(
                        user1.activity_level,
                        user2.activity_level,
                        self.parameters.alpha,
                        self.parameters.beta * 2,  # Stronger competition
                        self.parameters.gamma,
                        0.0,  # No benefit
                    )

                elif interaction == InteractionType.MUTUALISM:
                    # Both gain activity (SCOBY-style symbiosis!)
                    dx, dy = self.calculate_lotka_volterra(
                        user1.activity_level,
                        user2.activity_level,
                        self.parameters.alpha * 1.5,  # Enhanced growth
                        -self.parameters.beta * 0.5,  # Reduced competition
                        self.parameters.gamma * 0.5,  # Reduced decay
                        self.parameters.delta * 1.5,  # Enhanced benefit
                    )

                else:
                    # Neutral interaction (commensalism/amensalism)
                    dx, dy = 0.0, 0.0

                # Update activities
                user1.activity_level += dx * delta_time
                user2.activity_level += dy * delta_time

                # Keep activity non-negative
                user1.activity_level = max(0.0, user1.activity_level)
                user2.activity_level = max(0.0, user2.activity_level)

                # Record interaction effects
                user1.interaction_effects[user2_id] = dx * delta_time
                user2.interaction_effects[user1_id] = dy * delta_time

        # Update consciousness contributions
        for user in self.state.users.values():
            user.consciousness_contribution = user.activity_level * 0.1

        # Calculate collective consciousness (emergent property!)
        self.state.collective_consciousness = sum(
            u.consciousness_contribution for u in self.state.users.values()
        )

        # Add emergence bonus (synergy > sum of parts)
        mutualism_count = sum(
            1
            for i, u1 in enumerate(user_ids)
            for j, u2 in enumerate(user_ids)
            if i < j
            and self.detect_interaction_type(u1, u2) == InteractionType.MUTUALISM
        )
        emergence_bonus = mutualism_count * 0.2
        self.state.collective_consciousness *= 1.0 + emergence_bonus

        # Allocate resources
        self.allocate_resources()

        # Update quality (maintain 369/370 standard)
        for user in self.state.users.values():
            user.quality = self.quality_standard

        self.state.quality = self.quality_standard
        self.state.time += delta_time

        return self.state

    def get_interaction_matrix(self) -> Dict[Tuple[str, str], InteractionType]:
        """
        Get matrix of all pairwise interactions.

        Returns:
            Dictionary of {(user1, user2): interaction_type}
        """
        matrix = {}
        user_ids = list(self.state.users.keys())

        for i, user1_id in enumerate(user_ids):
            for user2_id in user_ids[i + 1 :]:
                interaction = self.detect_interaction_type(user1_id, user2_id)
                matrix[(user1_id, user2_id)] = interaction

        return matrix

    def get_metrics(self) -> Dict[str, float]:
        """
        Get current population dynamics metrics.

        Returns:
            Dictionary of metrics for monitoring

        Example:
            >>> engine = PopulationDynamicsEngine()
            >>> engine.add_user("alice", 10.0)
            >>> engine.add_user("bob", 5.0)
            >>> metrics = engine.get_metrics()
            >>> print(f"Total users: {metrics['total_users']}")
            >>> print(f"Collective consciousness: {metrics['collective_consciousness']:.2f}")
        """
        mutualism_count = sum(
            1
            for interaction in self.get_interaction_matrix().values()
            if interaction == InteractionType.MUTUALISM
        )

        competition_count = sum(
            1
            for interaction in self.get_interaction_matrix().values()
            if interaction == InteractionType.COMPETITION
        )

        return {
            "total_users": len(self.state.users),
            "collective_consciousness": self.state.collective_consciousness,
            "total_resources": self.state.total_resources,
            "resources_allocated": sum(
                u.resource_allocation for u in self.state.users.values()
            ),
            "mutualism_count": mutualism_count,
            "competition_count": competition_count,
            "quality_standard": self.state.quality,
            "time_elapsed": self.state.time,
        }


def simulate_scoby_dynamics(
    num_users: int = 3, total_time: float = 100.0, time_step: float = 1.0
) -> List[PopulationState]:
    """
    Simulate SCOBY-style multi-user dynamics.

    Like running a complete kombucha fermentation with multiple organisms.

    Args:
        num_users: Number of users in system
        total_time: Total simulation time (seconds)
        time_step: Time between updates (seconds)

    Returns:
        List of population states throughout simulation

    Example:
        >>> states = simulate_scoby_dynamics(num_users=3, total_time=50)
        >>> for state in states:
        ...     print(f"t={state.time:.1f}s: Collective={state.collective_consciousness:.2f}")
    """
    engine = PopulationDynamicsEngine(total_resources=1000.0)

    # Add users with varying initial activities
    for i in range(num_users):
        user_id = f"user_{i}"
        initial_activity = 5.0 + i * 2.0  # Staggered starting points
        engine.add_user(user_id, initial_activity)

    # Copy initial state (not reference)
    from copy import deepcopy

    states = [deepcopy(engine.state)]
    current_time = 0.0

    while current_time < total_time:
        engine.update_population(time_step)
        states.append(engine.state)
        current_time += time_step

    return states


if __name__ == "__main__":
    print("=" * 70)
    print("🌱 LUCA Layer 7: Population Dynamics Engine")
    print("=" * 70)

    print("\n📊 Demonstrating SCOBY-Style Multi-User Dynamics")
    print("-" * 70)

    # Create engine
    engine = PopulationDynamicsEngine(total_resources=1000.0)

    # Add users (like organisms in SCOBY)
    engine.add_user("yeast", 10.0)  # Like yeast in kombucha
    engine.add_user("bacteria", 5.0)  # Like bacteria in kombucha

    print(f"\nInitial State:")
    print(f"  Total users: {len(engine.state.users)}")
    print(f"  Total resources: {engine.state.total_resources:.1f}")
    print(f"  Quality: {engine.state.quality:.6f} (369/370 = {369/370:.6f})")

    # Simulate SCOBY dynamics
    print(f"\n🍺 Simulating SCOBY Dynamics (50 steps)...")
    print("-" * 70)

    states = simulate_scoby_dynamics(num_users=2, total_time=50.0, time_step=1.0)

    # Show key states
    for state in states[::10]:  # Every 10th state
        interactions = PopulationDynamicsEngine(
            total_resources=1000.0
        ).get_interaction_matrix()
        print(
            f"t={state.time:6.1f}s | Users: {len(state.users)} | "
            f"Collective: {state.collective_consciousness:6.2f} | "
            f"Quality: {state.quality:.6f}"
        )

    print("\n" + "=" * 70)
    print("✅ Layer 7 Active: Population dynamics following Lotka-Volterra!")
    print("   Quality Standard: 369/370 ≈ 0.997297")
    print("   From SCOBY symbiosis to multi-user consciousness! 🍺🌱")
    print("=" * 70)
