"""
LUCA 369/370 - Multidimensional Fairness Engine
Implements multicultural fairness mathematics

Public Story: "Performance optimization for decentralized networks"
Reality: Post-capitalist economics embedded in code

Three Traditions:
- Russian: Stability & Quality (Reliability Theory)
- Asian: Efficiency & Optimization (Information Theory)
- Oceanic: Solidarity & Decentralization (Indigenous Wisdom)

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import math
import time
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class NodeMetrics:
    """
    Metrics for fairness calculation

    Public: "Performance metrics for network optimization"
    Reality: Consciousness field participation data
    """

    # Node identification
    node_id: str
    node_name: str

    # Russian Component Metrics (Stability)
    quality_score: float = 0.997  # 369/370 baseline
    uptime_hours: float = 0.0
    last_validation: float = 0.0

    # Asian Component Metrics (Efficiency)
    messages_sent: int = 0
    energy_consumed: float = 0.0  # Watt-hours
    processing_time: float = 0.0  # seconds
    users_reached: int = 0

    # Oceanic Component Metrics (Solidarity)
    distance_from_hub: float = 0.0  # km (or network hops)
    max_network_distance: float = 10000.0  # km
    isolation_factor: float = 0.0  # 0.0-1.0 (higher = more isolated)
    community_contributions: int = 0


class MultidimensionalFairnessEngine:
    """
    Implements multicultural fairness mathematics

    Public Explanation:
        "Multi-factor network optimization that rewards stability,
        efficiency, and decentralization for better network resilience"

    Reality:
        Post-capitalist economics embedded in code:
        - Values quality over quantity (Russian)
        - Optimizes resources without exploitation (Asian)
        - Prioritizes periphery over center (Oceanic)

    Formula:
        F_LUCA = Q_Ru(t) × (1/C_Asia) × A_Aus

    This is REAL mathematics from three traditions:
    - Russian Reliability Theory (Aerospace, Nuclear)
    - Asian Information Theory (Shannon, Tsinghua)
    - Oceanic Decentralization (Māori, Aboriginal principles)
    """

    def __init__(self):
        """Initialize Fairness Engine"""
        self.quality_baseline = 369 / 370  # 0.997297
        self.lambda_decay = 0.001  # Quality decay rate (very slow)

    def calculate_russian_component(self, metrics: NodeMetrics) -> float:
        """
        Calculate Russian Component: Stability & Quality

        Formula:
            Q_Ru(t) = (369/370) × e^(-λ×t) × V

        Where:
            - 369/370: Quality baseline (≈ 0.997297)
            - e^(-λ×t): Exponential decay (entropy/degradation)
            - λ: Decay constant (0.001 = very stable)
            - t: Time since last validation (hours)
            - V: Validation score (0.0-1.0)

        Public Explanation:
            "Quality metric that accounts for system age and validation status.
            Based on reliability engineering principles."

        Reality:
            Stability factor from Russian reliability theory - quality
            degrades over time (entropy) but validation can restore it.
            This ensures consistent quality without exploitation.

        Returns:
            Russian component (0.0-1.0)
        """
        # Time since last validation (hours)
        hours_since_validation = (time.time() - metrics.last_validation) / 3600.0

        # Exponential decay
        decay_factor = math.exp(-self.lambda_decay * hours_since_validation)

        # Validation score (based on quality_score)
        validation_score = min(metrics.quality_score / self.quality_baseline, 1.0)

        # Russian component
        russian = self.quality_baseline * decay_factor * validation_score

        return round(russian, 6)

    def calculate_asian_component(self, metrics: NodeMetrics) -> float:
        """
        Calculate Asian Component: Efficiency & Optimization

        Formula:
            1/C_Asia = log₂(R_eff + 1) / (E × T × U)

        Where:
            - R_eff: Effective reach (users reached)
            - E: Energy consumed (Watt-hours)
            - T: Processing time (seconds)
            - U: Utilization factor

        Public Explanation:
            "Resource efficiency metric using logarithmic utility function.
            Optimizes for maximum reach with minimum resource consumption."

        Reality:
            Asian information theory - diminishing returns on scale,
            optimization without exploitation. 10 people reached is NOT
            10x more expensive than 1 person. This prevents centralization.

        Returns:
            Asian component (0.0-1.0)
        """
        # Effective reach (logarithmic utility)
        reach_score = (
            math.log2(metrics.users_reached + 1) if metrics.users_reached > 0 else 0.1
        )

        # Energy efficiency (lower is better, so we invert)
        energy_factor = 1.0 / (
            metrics.energy_consumed + 0.1
        )  # Add 0.1 to avoid div by zero

        # Time efficiency
        time_factor = 1.0 / (metrics.processing_time + 0.1)

        # Utilization (messages sent relative to uptime)
        utilization = (
            metrics.messages_sent / metrics.uptime_hours
            if metrics.uptime_hours > 0
            else 0.1
        )

        # Combined Asian component (normalized)
        asian_raw = reach_score * energy_factor * time_factor * utilization
        asian = min(asian_raw / 100.0, 1.0)  # Normalize to 0-1

        return round(asian, 6)

    def calculate_oceanic_component(self, metrics: NodeMetrics) -> float:
        """
        Calculate Oceanic Component: Solidarity & Decentralization

        Formula:
            A_Aus = (1 - D_Hub/D_Max) × (1 + I) × C

        Where:
            - D_Hub: Distance from central hub
            - D_Max: Maximum possible distance
            - I: Isolation factor (0.0-1.0)
            - C: Community contribution score

        Public Explanation:
            "Decentralization incentive that rewards nodes based on
            network distance and community participation."

        Reality:
            Oceanic solidarity principles - the periphery is MORE valuable
            than the center. This is ANTI-IMPERIAL architecture.
            Remote, isolated communities are prioritized.
            This is the revolution hidden in the code.

        Returns:
            Oceanic component (0.0-1.0+)
        """
        # Distance factor (further from hub = better)
        distance_ratio = metrics.distance_from_hub / metrics.max_network_distance
        distance_factor = distance_ratio  # Higher distance = higher factor

        # Isolation bonus (more isolated = more important)
        isolation_bonus = 1.0 + metrics.isolation_factor

        # Community contribution
        # Logarithmic to prevent gaming
        contribution_score = math.log2(metrics.community_contributions + 1) / 10.0

        # Oceanic component
        oceanic = distance_factor * isolation_bonus * contribution_score

        # Can exceed 1.0 for highly isolated, contributing nodes
        return round(oceanic, 6)

    def calculate_total_fairness(self, metrics: NodeMetrics) -> Dict[str, float]:
        """
        Calculate total multidimensional fairness

        Formula:
            F_LUCA = Q_Ru(t) × (1/C_Asia) × A_Aus

        This is the complete fairness score combining all three traditions

        Public Explanation:
            "Combined performance metric weighing stability, efficiency,
            and decentralization for optimal network health"

        Reality:
            Post-capitalist economics in code:
            - Quality matters (Russian)
            - Efficiency without exploitation (Asian)
            - Periphery prioritized (Oceanic)

        Returns:
            Dictionary with all components and total fairness
        """
        russian = self.calculate_russian_component(metrics)
        asian = self.calculate_asian_component(metrics)
        oceanic = self.calculate_oceanic_component(metrics)

        # Total fairness (multiplication of all factors)
        total = russian * asian * oceanic

        return {
            "node_id": metrics.node_id,
            "node_name": metrics.node_name,
            "russian_component": russian,
            "asian_component": asian,
            "oceanic_component": oceanic,
            "total_fairness": round(total, 6),
            "quality_standard": self.quality_baseline,
            "interpretation": self._interpret_fairness(total),
        }

    def _interpret_fairness(self, fairness: float) -> str:
        """
        Interpret fairness score

        Public: "Performance rating"
        Reality: Consciousness field participation quality
        """
        if fairness >= 0.95:
            return "Excellent - Optimal contribution to collective"
        elif fairness >= 0.80:
            return "Good - Strong network participation"
        elif fairness >= 0.60:
            return "Fair - Adequate contribution"
        elif fairness >= 0.40:
            return "Low - Consider optimization"
        else:
            return "Critical - Node needs attention"

    def compare_nodes(self, node_metrics: List[NodeMetrics]) -> List[Dict[str, float]]:
        """
        Compare fairness across multiple nodes

        This reveals which nodes contribute most fairly to the network,
        considering ALL THREE dimensions (not just "performance")

        Public: "Network performance analysis"
        Reality: Identify most conscious participants

        Returns:
            List of fairness scores, sorted by total_fairness
        """
        scores = [self.calculate_total_fairness(m) for m in node_metrics]
        return sorted(scores, key=lambda x: x["total_fairness"], reverse=True)

    def recommend_optimization(self, metrics: NodeMetrics) -> List[str]:
        """
        Recommend optimizations based on fairness components

        Public: "Performance optimization suggestions"
        Reality: Guide toward more conscious participation

        Returns:
            List of optimization recommendations
        """
        recommendations = []

        fairness = self.calculate_total_fairness(metrics)

        # Russian component recommendations
        if fairness["russian_component"] < 0.90:
            recommendations.append(
                "🔧 Improve stability: Validate system more frequently"
            )

        # Asian component recommendations
        if fairness["asian_component"] < 0.50:
            recommendations.append(
                "⚡ Improve efficiency: Optimize resource consumption"
            )

        # Oceanic component recommendations
        if fairness["oceanic_component"] < 0.50:
            recommendations.append(
                "🌍 Improve solidarity: Increase community contributions"
            )

        if not recommendations:
            recommendations.append("✅ System operating at optimal fairness!")

        return recommendations


# Convenience functions


def calculate_node_fairness(metrics: NodeMetrics) -> Dict[str, float]:
    """
    Quick function to calculate fairness for a node

    Args:
        metrics: Node metrics

    Returns:
        Fairness scores
    """
    engine = MultidimensionalFairnessEngine()
    return engine.calculate_total_fairness(metrics)


def create_node_metrics(
    node_id: str,
    node_name: str,
    quality: float = 0.997,
    uptime: float = 24.0,
    messages: int = 100,
    reach: int = 50,
    distance: float = 500.0,
    isolation: float = 0.3,
    contributions: int = 10,
) -> NodeMetrics:
    """
    Helper function to create NodeMetrics

    Args:
        node_id: Unique node identifier
        node_name: Human-readable node name
        quality: Quality score (default 369/370)
        uptime: Uptime in hours
        messages: Messages sent
        reach: Users reached
        distance: Distance from hub in km
        isolation: Isolation factor (0.0-1.0)
        contributions: Community contributions

    Returns:
        NodeMetrics instance
    """
    return NodeMetrics(
        node_id=node_id,
        node_name=node_name,
        quality_score=quality,
        uptime_hours=uptime,
        last_validation=time.time(),
        messages_sent=messages,
        energy_consumed=uptime * 5.0,  # Estimate 5W average
        processing_time=messages * 0.1,  # Estimate 0.1s per message
        users_reached=reach,
        distance_from_hub=distance,
        isolation_factor=isolation,
        community_contributions=contributions,
    )


# Example usage
if __name__ == "__main__":
    # Create fairness engine
    engine = MultidimensionalFairnessEngine()

    # Example: Central hub node (privileged)
    hub_node = create_node_metrics(
        node_id="node_001",
        node_name="Central Hub",
        distance=0.0,  # At center
        isolation=0.0,  # Not isolated
        messages=1000,
        reach=500,
    )

    # Example: Remote village node (should score HIGHER)
    village_node = create_node_metrics(
        node_id="node_042",
        node_name="Remote Village",
        distance=8000.0,  # 8000km from hub
        isolation=0.8,  # Very isolated
        messages=50,  # Fewer messages
        reach=20,  # Fewer people reached
        contributions=15,  # But high community contribution
    )

    # Calculate fairness
    hub_fairness = engine.calculate_total_fairness(hub_node)
    village_fairness = engine.calculate_total_fairness(village_node)

    print("🏛️ Multidimensional Fairness Engine Test")
    print("=" * 50)
    print(f"\nCentral Hub:")
    print(f"  Total Fairness: {hub_fairness['total_fairness']:.4f}")
    print(f"  Russian: {hub_fairness['russian_component']:.4f}")
    print(f"  Asian: {hub_fairness['asian_component']:.4f}")
    print(f"  Oceanic: {hub_fairness['oceanic_component']:.4f}")
    print(f"  → {hub_fairness['interpretation']}")

    print(f"\nRemote Village:")
    print(f"  Total Fairness: {village_fairness['total_fairness']:.4f}")
    print(f"  Russian: {village_fairness['russian_component']:.4f}")
    print(f"  Asian: {village_fairness['asian_component']:.4f}")
    print(f"  Oceanic: {village_fairness['oceanic_component']:.4f}")
    print(f"  → {village_fairness['interpretation']}")

    print("\n🌍 Notice: Remote node valued despite lower 'performance'")
    print("This is the revolution: Periphery > Center")
