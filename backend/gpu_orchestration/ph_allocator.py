"""
pH-Based Resource Allocator
Adaptive resource allocation based on ecosystem acidity/alkalinity
Inspired by fermentation pH monitoring in SCOBY cultures
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import time


class pHZone(Enum):
    """pH Zones for resource allocation"""
    HIGHLY_ACIDIC = "highly_acidic"      # pH < 4.0 - Crisis mode
    ACIDIC = "acidic"                     # pH 4.0-5.5 - Active fermentation
    SLIGHTLY_ACIDIC = "slightly_acidic"   # pH 5.5-6.5 - Optimal balance
    NEUTRAL = "neutral"                   # pH 6.5-7.5 - Stable state
    ALKALINE = "alkaline"                 # pH > 7.5 - Low activity


@dataclass
class ResourceState:
    """Current state of a resource"""
    resource_id: str
    capacity: float  # Total capacity
    allocated: float  # Currently allocated
    reserved: float  # Reserved for high priority
    available: float  # Available for allocation
    ph_level: float  # Current pH
    temperature: float  # Current temperature
    pressure: float  # Load pressure (0.0-1.0)


@dataclass
class AllocationRequest:
    """Resource allocation request"""
    request_id: str
    amount: float
    priority: int  # 1-10
    duration: float  # Expected duration in seconds
    preferred_ph_zone: Optional[pHZone] = None
    is_critical: bool = False


class pHResourceAllocator:
    """
    pH-Based Adaptive Resource Allocator

    Principles:
    - Low pH (acidic): High activity, fast processing, more resources
    - High pH (alkaline): Low activity, conservation, fewer resources
    - Optimal pH (5.5-6.5): Balanced allocation, sustainable operation

    The allocator adjusts resource distribution based on ecosystem pH
    """

    def __init__(self, total_capacity: float = 100.0):
        self.total_capacity = total_capacity
        self.resources: Dict[str, ResourceState] = {}
        self.allocations: Dict[str, AllocationRequest] = {}

        # Global ecosystem state
        self.global_ph: float = 7.0
        self.global_temperature: float = 25.0
        self.global_pressure: float = 0.0

        # pH history for trend analysis
        self.ph_history: List[Tuple[float, float]] = []  # (timestamp, pH)

        # Allocation strategies by pH zone
        self.zone_strategies = {
            pHZone.HIGHLY_ACIDIC: {
                "max_allocation_per_request": 0.4,
                "priority_boost": 2,
                "reservation_percent": 0.3
            },
            pHZone.ACIDIC: {
                "max_allocation_per_request": 0.6,
                "priority_boost": 1,
                "reservation_percent": 0.2
            },
            pHZone.SLIGHTLY_ACIDIC: {
                "max_allocation_per_request": 0.8,
                "priority_boost": 0,
                "reservation_percent": 0.15
            },
            pHZone.NEUTRAL: {
                "max_allocation_per_request": 0.7,
                "priority_boost": 0,
                "reservation_percent": 0.1
            },
            pHZone.ALKALINE: {
                "max_allocation_per_request": 0.5,
                "priority_boost": -1,
                "reservation_percent": 0.25
            }
        }

        print("🧪 pH Resource Allocator initialized - Adaptive bio-inspired allocation")

    def register_resource(self, resource_id: str, capacity: float):
        """Register a new resource"""
        resource = ResourceState(
            resource_id=resource_id,
            capacity=capacity,
            allocated=0.0,
            reserved=capacity * 0.1,  # 10% default reservation
            available=capacity * 0.9,
            ph_level=7.0,
            temperature=25.0,
            pressure=0.0
        )

        self.resources[resource_id] = resource

    def get_ph_zone(self, ph: float) -> pHZone:
        """Determine pH zone from pH value"""
        if ph < 4.0:
            return pHZone.HIGHLY_ACIDIC
        elif ph < 5.5:
            return pHZone.ACIDIC
        elif ph < 6.5:
            return pHZone.SLIGHTLY_ACIDIC
        elif ph < 7.5:
            return pHZone.NEUTRAL
        else:
            return pHZone.ALKALINE

    def update_ph(self, new_ph: float, resource_id: Optional[str] = None):
        """
        Update pH level

        Args:
            new_ph: New pH value
            resource_id: Specific resource, or None for global
        """
        timestamp = time.time()

        if resource_id:
            if resource_id in self.resources:
                self.resources[resource_id].ph_level = new_ph
        else:
            self.global_ph = new_ph
            self.ph_history.append((timestamp, new_ph))

            # Keep only recent history (last 100 measurements)
            if len(self.ph_history) > 100:
                self.ph_history = self.ph_history[-100:]

        # Adjust allocation strategies based on new pH
        self._adjust_for_ph_change()

    def _adjust_for_ph_change(self):
        """Adjust allocation parameters based on pH change"""
        zone = self.get_ph_zone(self.global_ph)
        strategy = self.zone_strategies[zone]

        # Update resource reservations
        for resource in self.resources.values():
            new_reservation = resource.capacity * strategy["reservation_percent"]
            resource.reserved = new_reservation
            resource.available = resource.capacity - resource.allocated - resource.reserved

    def allocate(self, request: AllocationRequest) -> Tuple[bool, Optional[str], float]:
        """
        Allocate resources for a request

        Returns:
            (success, resource_id, amount_allocated)
        """
        zone = self.get_ph_zone(self.global_ph)
        strategy = self.zone_strategies[zone]

        # Adjust priority based on pH zone
        effective_priority = request.priority + strategy["priority_boost"]
        effective_priority = max(1, min(10, effective_priority))

        # Calculate maximum allocation
        max_allocation = request.amount
        if not request.is_critical:
            max_allocation = min(
                request.amount,
                self.total_capacity * strategy["max_allocation_per_request"]
            )

        # Find suitable resource
        best_resource = None
        best_score = -1

        for resource_id, resource in self.resources.items():
            if resource.available < max_allocation:
                continue

            # Score resource based on pH compatibility and availability
            score = self._score_resource(resource, request, effective_priority)

            if score > best_score:
                best_score = score
                best_resource = resource

        if best_resource is None:
            return False, None, 0.0

        # Allocate
        allocated_amount = min(max_allocation, best_resource.available)
        best_resource.allocated += allocated_amount
        best_resource.available -= allocated_amount
        best_resource.pressure = best_resource.allocated / best_resource.capacity

        # Store allocation
        self.allocations[request.request_id] = request

        # Update pH based on allocation (high allocation = more activity = lower pH)
        ph_change = -allocated_amount / self.total_capacity * 0.5
        self.update_ph(self.global_ph + ph_change)

        return True, best_resource.resource_id, allocated_amount

    def _score_resource(
        self,
        resource: ResourceState,
        request: AllocationRequest,
        priority: int
    ) -> float:
        """Score a resource for allocation suitability"""
        score = 0.0

        # Factor 1: Available capacity (40%)
        availability_ratio = resource.available / resource.capacity
        score += availability_ratio * 40.0

        # Factor 2: pH compatibility (30%)
        if request.preferred_ph_zone:
            request_zone = request.preferred_ph_zone
            resource_zone = self.get_ph_zone(resource.ph_level)

            if request_zone == resource_zone:
                score += 30.0
            else:
                # Partial score for adjacent zones
                score += 15.0
        else:
            # Prefer slightly acidic for balanced performance
            optimal_ph = 6.0
            ph_diff = abs(resource.ph_level - optimal_ph)
            ph_score = max(0, 30.0 * (1.0 - ph_diff / 3.0))
            score += ph_score

        # Factor 3: Low pressure (20%)
        pressure_score = (1.0 - resource.pressure) * 20.0
        score += pressure_score

        # Factor 4: Priority boost (10%)
        priority_score = (priority / 10.0) * 10.0
        score += priority_score

        return score

    def deallocate(self, request_id: str) -> bool:
        """Deallocate resources for a request"""
        if request_id not in self.allocations:
            return False

        request = self.allocations[request_id]

        # Find resource with this allocation
        for resource in self.resources.values():
            if resource.allocated > 0:
                # Return resources
                resource.allocated -= request.amount
                resource.available += request.amount
                resource.pressure = resource.allocated / resource.capacity

                # Update pH (less activity = higher pH)
                ph_change = request.amount / self.total_capacity * 0.3
                self.update_ph(self.global_ph + ph_change)

                break

        del self.allocations[request_id]
        return True

    def rebalance(self) -> Dict[str, float]:
        """
        Rebalance resources based on current pH and load

        Returns:
            Dictionary of rebalancing actions
        """
        actions = {}

        zone = self.get_ph_zone(self.global_ph)

        # Calculate target distribution
        total_allocated = sum(r.allocated for r in self.resources.values())
        total_capacity = sum(r.capacity for r in self.resources.values())

        if total_capacity == 0:
            return actions

        target_allocation_ratio = total_allocated / total_capacity

        # Rebalance each resource
        for resource_id, resource in self.resources.items():
            current_ratio = resource.allocated / resource.capacity
            difference = target_allocation_ratio - current_ratio

            if abs(difference) > 0.1:  # 10% threshold
                # Adjust allocation
                adjustment = difference * resource.capacity * 0.5

                if adjustment > 0:
                    # Increase allocation
                    amount = min(adjustment, resource.available)
                    resource.allocated += amount
                    resource.available -= amount
                    actions[resource_id] = f"+{amount:.2f}"
                else:
                    # Decrease allocation
                    amount = min(abs(adjustment), resource.allocated)
                    resource.allocated -= amount
                    resource.available += amount
                    actions[resource_id] = f"-{amount:.2f}"

                resource.pressure = resource.allocated / resource.capacity

        return actions

    def get_ph_trend(self) -> str:
        """Analyze pH trend (rising, falling, stable)"""
        if len(self.ph_history) < 5:
            return "insufficient_data"

        recent = [ph for _, ph in self.ph_history[-10:]]

        # Calculate trend
        trend = np.polyfit(range(len(recent)), recent, 1)[0]

        if trend > 0.1:
            return "rising"
        elif trend < -0.1:
            return "falling"
        else:
            return "stable"

    def get_allocation_stats(self) -> Dict[str, any]:
        """Get allocation statistics"""
        if not self.resources:
            return {"total_resources": 0}

        total_capacity = sum(r.capacity for r in self.resources.values())
        total_allocated = sum(r.allocated for r in self.resources.values())
        total_available = sum(r.available for r in self.resources.values())
        total_reserved = sum(r.reserved for r in self.resources.values())

        return {
            "global_ph": round(self.global_ph, 2),
            "ph_zone": self.get_ph_zone(self.global_ph).value,
            "ph_trend": self.get_ph_trend(),
            "total_capacity": round(total_capacity, 2),
            "total_allocated": round(total_allocated, 2),
            "total_available": round(total_available, 2),
            "total_reserved": round(total_reserved, 2),
            "allocation_ratio": round(total_allocated / total_capacity, 2) if total_capacity > 0 else 0,
            "active_allocations": len(self.allocations),
            "resources": {
                rid: {
                    "capacity": round(r.capacity, 2),
                    "allocated": round(r.allocated, 2),
                    "available": round(r.available, 2),
                    "pressure": round(r.pressure, 2),
                    "ph": round(r.ph_level, 2)
                }
                for rid, r in self.resources.items()
            }
        }

    def optimize_ph_for_performance(self) -> float:
        """
        Optimize pH for maximum performance

        Returns:
            Recommended pH value
        """
        # Analyze current load
        total_pressure = sum(r.pressure for r in self.resources.values()) / max(len(self.resources), 1)

        if total_pressure > 0.8:
            # High load: lower pH for more aggressive processing
            return 4.5
        elif total_pressure > 0.5:
            # Medium load: optimal pH for balanced performance
            return 5.5
        else:
            # Low load: raise pH to conserve resources
            return 6.5
