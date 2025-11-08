"""
SCOBY Load Balancer
Bio-inspired load balancing based on Kombucha SCOBY culture
Implements symbiotic organism cooperation for optimal GPU utilization
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math


class OrganismRole(Enum):
    """SCOBY Organism Roles"""
    YEAST = "yeast"          # Quick fermentation, high energy
    BACTERIA = "bacteria"    # Steady processing, diversity
    MATRIX = "matrix"        # Support structure, stability


@dataclass
class SCOBYOrganism:
    """Represents an organism in the SCOBY ecosystem"""
    organism_id: str
    role: OrganismRole
    activity_level: float  # 0.0 - 1.0
    nutrient_consumption: float  # Resources used
    byproduct_production: float  # Heat, completed tasks
    cooperation_score: float  # How well it works with others
    reproduction_rate: float  # Task throughput


class SCOBYLoadBalancer:
    """
    SCOBY-Inspired Load Balancer

    Kombucha SCOBY Principles:
    1. Yeast (NVIDIA): Fast fermentation, high sugar consumption
    2. Bacteria (AMD): Slower but diverse, creates protective layer
    3. Matrix (Intel): Provides structure and stability

    The ecosystem self-regulates through pH and temperature
    """

    def __init__(self):
        self.organisms: Dict[str, SCOBYOrganism] = {}

        # Ecosystem parameters
        self.ph_level: float = 7.0  # Ideal: 4.5-5.5 for active fermentation
        self.temperature: float = 25.0  # Celsius, ideal: 20-30
        self.sugar_level: float = 1.0  # Available resources

        # Fermentation stages
        self.fermentation_stage: str = "initial"  # initial, active, mature
        self.fermentation_time: int = 0  # Time units

        # Load balancing metrics
        self.total_load: float = 0.0
        self.balanced_load: float = 0.0
        self.imbalance_factor: float = 0.0

        print("🦠 SCOBY Load Balancer initialized - Bio-inspired symbiotic distribution")

    def register_organism(self, organism_id: str, role: OrganismRole):
        """Register a new organism (GPU) in the SCOBY"""
        organism = SCOBYOrganism(
            organism_id=organism_id,
            role=role,
            activity_level=0.5,
            nutrient_consumption=0.0,
            byproduct_production=0.0,
            cooperation_score=0.8,
            reproduction_rate=0.5
        )

        # Set role-specific parameters
        if role == OrganismRole.YEAST:
            organism.activity_level = 0.9
            organism.reproduction_rate = 0.8
        elif role == OrganismRole.BACTERIA:
            organism.activity_level = 0.6
            organism.reproduction_rate = 0.6
        elif role == OrganismRole.MATRIX:
            organism.activity_level = 0.4
            organism.reproduction_rate = 0.3

        self.organisms[organism_id] = organism
        self._update_ecosystem()

    def calculate_load_distribution(
        self,
        total_workload: float,
        workload_type: str = "balanced"
    ) -> Dict[str, float]:
        """
        Calculate optimal load distribution across organisms

        Args:
            total_workload: Total work to distribute (0.0 - 1.0)
            workload_type: 'speed', 'efficiency', 'balanced', 'endurance'

        Returns:
            Dictionary mapping organism_id to assigned load
        """
        if not self.organisms:
            return {}

        distribution = {}

        # Calculate weights based on workload type and organism characteristics
        weights = self._calculate_organism_weights(workload_type)

        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight == 0:
            return {oid: 0.0 for oid in self.organisms.keys()}

        # Distribute load proportionally
        for organism_id, weight in weights.items():
            load = (weight / total_weight) * total_workload
            distribution[organism_id] = load

        # Apply SCOBY balancing - redistribute based on cooperation
        distribution = self._apply_symbiotic_balancing(distribution)

        # Update organism states
        for organism_id, load in distribution.items():
            self.organisms[organism_id].nutrient_consumption = load

        self._update_ecosystem()

        return distribution

    def _calculate_organism_weights(self, workload_type: str) -> Dict[str, float]:
        """Calculate distribution weights based on workload type and organism properties"""
        weights = {}

        for organism_id, organism in self.organisms.items():
            base_weight = organism.activity_level * organism.cooperation_score

            # Adjust based on workload type
            if workload_type == "speed":
                # Favor yeast (high activity)
                if organism.role == OrganismRole.YEAST:
                    base_weight *= 1.5
                elif organism.role == OrganismRole.BACTERIA:
                    base_weight *= 0.8

            elif workload_type == "efficiency":
                # Favor bacteria (steady, efficient)
                if organism.role == OrganismRole.BACTERIA:
                    base_weight *= 1.5
                elif organism.role == OrganismRole.YEAST:
                    base_weight *= 0.9

            elif workload_type == "endurance":
                # Favor matrix (stable, long-running)
                if organism.role == OrganismRole.MATRIX:
                    base_weight *= 1.8
                elif organism.role == OrganismRole.YEAST:
                    base_weight *= 0.7

            # Balanced: use base weights as-is

            # Apply pH factor - organisms work better at optimal pH
            ph_factor = self._calculate_ph_performance_factor(organism.role)
            base_weight *= ph_factor

            # Apply temperature factor
            temp_factor = self._calculate_temperature_factor()
            base_weight *= temp_factor

            weights[organism_id] = max(0.0, base_weight)

        return weights

    def _apply_symbiotic_balancing(self, distribution: Dict[str, float]) -> Dict[str, float]:
        """
        Apply SCOBY symbiotic principles to balance load
        Organisms help each other based on cooperation scores
        """
        balanced = distribution.copy()

        # Find overloaded and underloaded organisms
        organism_loads = [
            (oid, load, self.organisms[oid])
            for oid, load in distribution.items()
        ]

        # Sort by load
        organism_loads.sort(key=lambda x: x[1], reverse=True)

        # Redistribute from overloaded to cooperative underloaded
        for i, (oid_heavy, load_heavy, org_heavy) in enumerate(organism_loads[:len(organism_loads)//2]):
            for oid_light, load_light, org_light in organism_loads[len(organism_loads)//2:]:
                # Check if organisms can cooperate
                cooperation = (org_heavy.cooperation_score + org_light.cooperation_score) / 2

                if cooperation > 0.7 and load_heavy > load_light * 1.5:
                    # Transfer some load
                    transfer = (load_heavy - load_light) * 0.1 * cooperation
                    balanced[oid_heavy] -= transfer
                    balanced[oid_light] += transfer

        return balanced

    def _calculate_ph_performance_factor(self, role: OrganismRole) -> float:
        """
        Calculate performance factor based on pH and organism role
        Yeast: prefers pH 5-6 (slightly acidic)
        Bacteria: prefers pH 4-5 (more acidic)
        Matrix: prefers pH 6-7 (near neutral)
        """
        if role == OrganismRole.YEAST:
            optimal_ph = 5.5
            tolerance = 1.0
        elif role == OrganismRole.BACTERIA:
            optimal_ph = 4.5
            tolerance = 1.0
        else:  # MATRIX
            optimal_ph = 6.5
            tolerance = 1.5

        ph_diff = abs(self.ph_level - optimal_ph)

        if ph_diff <= tolerance:
            # Within tolerance - high performance
            factor = 1.0 - (ph_diff / tolerance) * 0.3
        else:
            # Outside tolerance - reduced performance
            factor = 0.7 - min((ph_diff - tolerance) * 0.1, 0.5)

        return max(0.2, factor)

    def _calculate_temperature_factor(self) -> float:
        """Calculate performance factor based on temperature"""
        optimal_temp = 25.0

        if 20.0 <= self.temperature <= 30.0:
            # Optimal range
            return 1.0
        elif 15.0 <= self.temperature <= 35.0:
            # Acceptable range
            diff = abs(self.temperature - optimal_temp)
            return 1.0 - (diff / 15.0) * 0.3
        else:
            # Suboptimal
            diff = abs(self.temperature - optimal_temp)
            return max(0.4, 1.0 - (diff / 20.0) * 0.6)

    def _update_ecosystem(self):
        """Update ecosystem state based on organism activities"""
        if not self.organisms:
            return

        # Calculate average activity
        avg_activity = sum(o.activity_level for o in self.organisms.values()) / len(self.organisms)

        # Update pH (high activity produces acid, lowers pH)
        ph_change = -avg_activity * 0.1
        self.ph_level = max(3.0, min(8.0, self.ph_level + ph_change))

        # Update temperature (activity produces heat)
        temp_change = avg_activity * 0.5
        self.temperature = max(15.0, min(40.0, self.temperature + temp_change - 0.3))  # Natural cooling

        # Update fermentation stage
        self.fermentation_time += 1

        if self.fermentation_time < 10:
            self.fermentation_stage = "initial"
        elif self.fermentation_time < 50:
            self.fermentation_stage = "active"
        else:
            self.fermentation_stage = "mature"

        # Update organism cooperation based on pH balance
        for organism in self.organisms.values():
            if 4.5 <= self.ph_level <= 6.5:
                # Optimal pH - increase cooperation
                organism.cooperation_score = min(1.0, organism.cooperation_score + 0.01)
            else:
                # Suboptimal - decrease cooperation
                organism.cooperation_score = max(0.3, organism.cooperation_score - 0.01)

    def calculate_fermentation_rate(self) -> float:
        """
        Calculate overall fermentation rate (task processing speed)
        Based on SCOBY ecosystem health
        """
        if not self.organisms:
            return 0.0

        # Factor 1: Organism activity (40%)
        avg_activity = sum(o.activity_level for o in self.organisms.values()) / len(self.organisms)

        # Factor 2: pH optimality (30%)
        optimal_ph_range = (4.5, 6.0)
        if optimal_ph_range[0] <= self.ph_level <= optimal_ph_range[1]:
            ph_factor = 1.0
        else:
            ph_diff = min(
                abs(self.ph_level - optimal_ph_range[0]),
                abs(self.ph_level - optimal_ph_range[1])
            )
            ph_factor = max(0.3, 1.0 - ph_diff * 0.2)

        # Factor 3: Temperature optimality (20%)
        temp_factor = self._calculate_temperature_factor()

        # Factor 4: Organism diversity (10%)
        role_counts = {}
        for organism in self.organisms.values():
            role_counts[organism.role] = role_counts.get(organism.role, 0) + 1
        diversity = len(role_counts) / 3.0  # Max 3 roles

        # Combined fermentation rate
        rate = (
            avg_activity * 0.4 +
            ph_factor * 0.3 +
            temp_factor * 0.2 +
            diversity * 0.1
        )

        return rate

    def get_ecosystem_status(self) -> Dict[str, any]:
        """Get current SCOBY ecosystem status"""
        return {
            "ph_level": round(self.ph_level, 2),
            "temperature": round(self.temperature, 2),
            "fermentation_stage": self.fermentation_stage,
            "fermentation_rate": round(self.calculate_fermentation_rate(), 2),
            "organism_count": len(self.organisms),
            "organisms": {
                oid: {
                    "role": o.role.value,
                    "activity": round(o.activity_level, 2),
                    "cooperation": round(o.cooperation_score, 2),
                    "load": round(o.nutrient_consumption, 2)
                }
                for oid, o in self.organisms.items()
            }
        }

    def optimize_for_throughput(self) -> Dict[str, float]:
        """
        Optimize ecosystem for maximum throughput
        Adjusts pH and temperature to maximize fermentation
        """
        # Target optimal conditions
        target_ph = 5.0  # Sweet spot for mixed culture
        target_temp = 25.0

        # Calculate adjustments
        ph_adjustment = (target_ph - self.ph_level) * 0.2
        temp_adjustment = (target_temp - self.temperature) * 0.3

        self.ph_level += ph_adjustment
        self.temperature += temp_adjustment

        # Boost yeast activity for speed
        for organism in self.organisms.values():
            if organism.role == OrganismRole.YEAST:
                organism.activity_level = min(1.0, organism.activity_level + 0.1)

        return {
            "ph_adjustment": round(ph_adjustment, 2),
            "temp_adjustment": round(temp_adjustment, 2),
            "new_fermentation_rate": round(self.calculate_fermentation_rate(), 2)
        }

    def optimize_for_efficiency(self) -> Dict[str, float]:
        """
        Optimize ecosystem for maximum efficiency (energy per task)
        Favors bacteria and stable conditions
        """
        # Target efficiency-optimized conditions
        target_ph = 4.8
        target_temp = 23.0

        ph_adjustment = (target_ph - self.ph_level) * 0.2
        temp_adjustment = (target_temp - self.temperature) * 0.3

        self.ph_level += ph_adjustment
        self.temperature += temp_adjustment

        # Boost bacteria activity for efficiency
        for organism in self.organisms.values():
            if organism.role == OrganismRole.BACTERIA:
                organism.activity_level = min(1.0, organism.activity_level + 0.1)

        return {
            "ph_adjustment": round(ph_adjustment, 2),
            "temp_adjustment": round(temp_adjustment, 2),
            "new_fermentation_rate": round(self.calculate_fermentation_rate(), 2)
        }
