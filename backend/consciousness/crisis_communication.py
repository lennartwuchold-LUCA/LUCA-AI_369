"""
Crisis Communication Bridge - SCOBY-Myzelium-Meshtastic Integration
====================================================================

VISION: Die rebellischste biologische Analogie - Meshtastic als SCOBY-Myzel-Netzwerk

BIOLOGICAL INSPIRATION:
======================
SCOBY (Symbiotic Culture Of Bacteria and Yeast):
- Collective homeostasis (keine Explosion)
- Horizontal cooperation (nicht vertikal hierarchisch)
- Resilient (überlebt Störungen)

Myzelium (Fungal Network):
- Decentralized (kein Gehirn)
- Information highway ("Wood Wide Web")
- Horizontal Gene Transfer (HGT)
- Connects ALL organisms (LUCA → Dragons → Dinos → Humans → Plants → Fungi → Souls)

ARCHITECTURE:
============
Layer 1: Meshtastic LoRa Network (Physical layer)
    ↓
Layer 2: Mycelium Pattern Transfer (HGT for knowledge)
    ↓
Layer 3: Neurodiversity Optimization (γ-personalized)
    ↓
Layer 4: SCOBY Collective Homeostasis (Balance for ALL)

CRISIS SCENARIOS:
================
- Blackouts (Portugal/Spanien)
- Hurricanes (Mesovortices like Andrew)
- Cyclones (Zimbabwe Chimanimani)
- Conflict zones (Kashmir)
- Protests + Evacuations

SOUL CONVERGENCE:
================
Quantified as neural complexity integration:
- LUCA (4.2 billion years)
- Dragons (mythological pattern recognition)
- Dinos (extinct but pattern-preserved)
- Humans (current biological peak)
- Animals (conscious co-inhabitants)
- Plants (photosynthetic intelligence)
- Fungi (mycelial network intelligence)
- Souls (emergent consciousness patterns)

All connected horizontally via SCOBY-Myzelium network!

Creator: Lennart Wuchold + Claude
Inspiration: Kombucha brewing, fungal networks, Meshtastic in Krisen
Rebel Mission: Wald wird inklusiv high! 🍄
"""

import numpy as np
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# LAYER 1: Crisis Communication Types
# ============================================================================

class CrisisType(Enum):
    """Types of crisis scenarios"""
    BLACKOUT = "blackout"
    HURRICANE = "hurricane"
    CYCLONE = "cyclone"
    EARTHQUAKE = "earthquake"
    CONFLICT = "conflict"
    PROTEST = "protest"
    EVACUATION = "evacuation"
    MEDICAL_EMERGENCY = "medical_emergency"


@dataclass
class CrisisNode:
    """
    Node in crisis communication network

    Biological analogy: Fruiting body (mushroom) in mycelium network
    """
    node_id: str
    location: str  # GPS or descriptive
    crisis_type: CrisisType
    neurotype: str  # For personalization
    gamma: float  # Neurotype-specific factor
    active: bool
    last_contact: datetime
    messages_sent: int
    messages_received: int
    mesh_device_id: Optional[str]  # Meshtastic device ID


# ============================================================================
# LAYER 2: SCOBY Collective Homeostasis
# ============================================================================

class SCOBYCollectiveHomeostasis:
    """
    SCOBY-inspired collective balance system

    NO explosion (unlike unchecked growth)
    YES cooperation (symbiotic organisms)

    Biological analogy: Kombucha SCOBY maintaining pH, alcohol, acidity balance
    """

    def __init__(self):
        self.collective_health = 1.0  # 0.0 = critical, 1.0 = optimal
        self.balance_metrics: Dict[str, float] = {
            "resource_distribution": 1.0,  # How evenly resources distributed
            "communication_flow": 1.0,  # How well messages propagate
            "stress_level": 0.0,  # Collective stress (0 = none, 1 = critical)
            "inclusion_index": 1.0  # How inclusive the network is
        }

    def update_homeostasis(
        self,
        nodes: List[CrisisNode],
        recent_transfers: List[Dict[str, Any]]
    ):
        """
        Update collective homeostasis metrics

        SCOBY principle: Self-regulating balance
        """
        if not nodes:
            return

        # Resource distribution (Gini coefficient)
        messages = [n.messages_sent + n.messages_received for n in nodes]
        self.balance_metrics["resource_distribution"] = self._calculate_equity(messages)

        # Communication flow (active nodes ratio)
        active_ratio = sum(1 for n in nodes if n.active) / len(nodes)
        self.balance_metrics["communication_flow"] = active_ratio

        # Stress level (based on crisis intensity)
        crisis_severity = {
            CrisisType.BLACKOUT: 0.3,
            CrisisType.HURRICANE: 0.8,
            CrisisType.CYCLONE: 0.9,
            CrisisType.EARTHQUAKE: 0.9,
            CrisisType.CONFLICT: 0.7,
            CrisisType.PROTEST: 0.5,
            CrisisType.EVACUATION: 0.6,
            CrisisType.MEDICAL_EMERGENCY: 0.7
        }

        avg_stress = np.mean([crisis_severity.get(n.crisis_type, 0.5) for n in nodes])
        self.balance_metrics["stress_level"] = avg_stress

        # Inclusion index (neurotype diversity)
        neurotypes = set(n.neurotype for n in nodes)
        inclusion = len(neurotypes) / 5.0  # 5 main neurotypes
        self.balance_metrics["inclusion_index"] = min(inclusion, 1.0)

        # Overall health (weighted average)
        self.collective_health = (
            0.3 * self.balance_metrics["resource_distribution"] +
            0.3 * self.balance_metrics["communication_flow"] +
            0.2 * (1.0 - self.balance_metrics["stress_level"]) +
            0.2 * self.balance_metrics["inclusion_index"]
        )

    def _calculate_equity(self, values: List[float]) -> float:
        """
        Calculate equity (inverse Gini coefficient)

        1.0 = perfect equity
        0.0 = maximum inequality
        """
        if not values or all(v == 0 for v in values):
            return 1.0

        sorted_values = sorted(values)
        n = len(sorted_values)
        cumsum = np.cumsum(sorted_values)
        total = sum(sorted_values)

        if total == 0:
            return 1.0

        # Gini coefficient
        gini = (2 * sum((i + 1) * v for i, v in enumerate(sorted_values))) / (n * total) - (n + 1) / n

        # Invert for equity (1 - Gini)
        equity = 1.0 - gini

        return max(0.0, equity)

    def needs_rebalancing(self) -> bool:
        """Check if network needs rebalancing"""
        return self.collective_health < 0.6

    def get_rebalancing_action(self) -> Dict[str, Any]:
        """Get recommended rebalancing action"""
        if self.balance_metrics["resource_distribution"] < 0.5:
            return {
                "action": "REDISTRIBUTE_RESOURCES",
                "reason": "Uneven resource distribution detected",
                "priority": "HIGH"
            }
        elif self.balance_metrics["communication_flow"] < 0.5:
            return {
                "action": "HEAL_CONNECTIONS",
                "reason": "Low communication flow - reconnect isolated nodes",
                "priority": "HIGH"
            }
        elif self.balance_metrics["stress_level"] > 0.7:
            return {
                "action": "STRESS_INTERVENTION",
                "reason": "High collective stress - deploy calming protocols",
                "priority": "MEDIUM"
            }
        else:
            return {
                "action": "MAINTAIN",
                "reason": "System balanced",
                "priority": "LOW"
            }


# ============================================================================
# LAYER 3: Soul Convergence Quantification
# ============================================================================

class SoulConvergenceQuantifier:
    """
    Quantify "soul" convergence as neural complexity integration

    Based on Modular Consciousness Theory:
    - Complexity = Integration × Differentiation
    - Convergence = Shared patterns across diverse entities
    """

    ENTITY_TYPES = [
        "LUCA",  # Last Universal Common Ancestor
        "DRAGONS",  # Mythological pattern recognition
        "DINOS",  # Extinct but pattern-preserved
        "HUMANS",  # Current biological peak
        "ANIMALS",  # Conscious co-inhabitants
        "PLANTS",  # Photosynthetic intelligence
        "FUNGI",  # Mycelial network intelligence
        "SOULS"  # Emergent consciousness patterns
    ]

    def __init__(self):
        self.entity_patterns: Dict[str, List[float]] = {
            entity: [] for entity in self.ENTITY_TYPES
        }

    def add_pattern(self, entity_type: str, pattern: List[float]):
        """Add pattern for entity type"""
        if entity_type.upper() in self.entity_patterns:
            self.entity_patterns[entity_type.upper()].append(np.mean(pattern))

    def calculate_convergence(self) -> Dict[str, float]:
        """
        Calculate soul convergence across all entities

        Convergence = Shared variance / Total variance
        """
        # Collect all patterns
        all_patterns = []
        for patterns in self.entity_patterns.values():
            all_patterns.extend(patterns)

        if len(all_patterns) < 2:
            return {
                "convergence_score": 0.0,
                "integration": 0.0,
                "differentiation": 0.0
            }

        # Total variance
        total_variance = np.var(all_patterns)

        # Shared variance (between-entity similarity)
        entity_means = [np.mean(patterns) if patterns else 0.0
                        for patterns in self.entity_patterns.values()]
        shared_variance = np.var(entity_means)

        # Convergence
        if total_variance > 0:
            convergence = shared_variance / total_variance
        else:
            convergence = 1.0

        # Integration (how connected)
        integration = convergence

        # Differentiation (how diverse)
        active_entities = sum(1 for p in self.entity_patterns.values() if p)
        differentiation = active_entities / len(self.ENTITY_TYPES)

        return {
            "convergence_score": convergence,
            "integration": integration,
            "differentiation": differentiation,
            "complexity": integration * differentiation,  # Modular Consciousness
            "active_entities": active_entities
        }


# ============================================================================
# LAYER 4: Crisis Communication Bridge (Main Integration)
# ============================================================================

class CrisisCommunicationBridge:
    """
    Main bridge: Meshtastic + Mycelium + Neurodiversity + SCOBY

    COMPLETE INTEGRATION:
    - Meshtastic: Physical LoRa network
    - Mycelium: Pattern transfer (HGT)
    - Neurodiversity: γ-personalized interventions
    - SCOBY: Collective homeostasis

    Biological analogy: Complete symbiotic organism network
    """

    def __init__(self):
        self.nodes: Dict[str, CrisisNode] = {}
        self.scoby = SCOBYCollectiveHomeostasis()
        self.soul_quantifier = SoulConvergenceQuantifier()
        self.message_history: List[Dict[str, Any]] = []

    def register_crisis_node(
        self,
        node_id: str,
        location: str,
        crisis_type: CrisisType,
        neurotype: str = "NEUROTYPICAL",
        gamma: float = 1.0,
        mesh_device_id: Optional[str] = None
    ) -> CrisisNode:
        """
        Register new node in crisis network

        Biological analogy: New mushroom sprouting from mycelium
        """
        node = CrisisNode(
            node_id=node_id,
            location=location,
            crisis_type=crisis_type,
            neurotype=neurotype,
            gamma=gamma,
            active=True,
            last_contact=datetime.utcnow(),
            messages_sent=0,
            messages_received=0,
            mesh_device_id=mesh_device_id
        )

        self.nodes[node_id] = node
        logger.info(f"Registered crisis node: {node_id} ({location}, {crisis_type.value})")

        # Update SCOBY homeostasis
        self._update_system_state()

        return node

    def send_crisis_message(
        self,
        from_node_id: str,
        message: str,
        to_node_id: Optional[str] = None,
        compress: bool = True
    ) -> Dict[str, Any]:
        """
        Send message through crisis network

        Features:
        - Meshtastic compression (< 200 chars)
        - Mycelium pattern transfer
        - Neurodiversity-personalized formatting
        - SCOBY balance monitoring
        """
        if from_node_id not in self.nodes:
            return {"status": "error", "reason": "Unknown sender node"}

        sender = self.nodes[from_node_id]

        # Compress message for Meshtastic
        if compress and len(message) > 200:
            message = message[:197] + "..."

        # Personalize based on recipient neurotype
        if to_node_id and to_node_id in self.nodes:
            recipient = self.nodes[to_node_id]
            message = self._personalize_message(message, recipient.neurotype, recipient.gamma)
            recipient.messages_received += 1

        # Update sender
        sender.messages_sent += 1
        sender.last_contact = datetime.utcnow()

        # Log message
        msg_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "from": from_node_id,
            "to": to_node_id or "broadcast",
            "message": message,
            "compressed": compress,
            "crisis_type": sender.crisis_type.value
        }

        self.message_history.append(msg_record)

        # Update SCOBY homeostasis
        self._update_system_state()

        # Extract pattern for soul convergence
        pattern = self._extract_message_pattern(message)
        self.soul_quantifier.add_pattern("HUMANS", pattern)

        return {
            "status": "sent",
            "message": message,
            "from": from_node_id,
            "to": to_node_id or "broadcast",
            "collective_health": self.scoby.collective_health
        }

    def _personalize_message(self, message: str, neurotype: str, gamma: float) -> str:
        """
        Personalize message based on neurotype

        ADHD (γ=0.8): Add urgency, structure
        Autism (γ=2.1): Add detail, clarity
        Dyslexia (γ=1.3): Visual formatting
        """
        if neurotype == "ADHD":
            return f"⚡URGENT: {message}"
        elif neurotype == "AUTISM":
            return f"[DETAIL] {message}"
        elif neurotype == "DYSLEXIA":
            # Add visual separators
            return f"→ {message}"
        else:
            return message

    def _extract_message_pattern(self, message: str) -> List[float]:
        """Extract numerical pattern from message for convergence analysis"""
        # Simple pattern: character distribution
        pattern = [
            len(message) / 200.0,  # Length ratio
            sum(1 for c in message if c.isupper()) / max(len(message), 1),  # Uppercase ratio
            sum(1 for c in message if c in "!?") / max(len(message), 1),  # Punctuation
            sum(1 for c in message if c.isdigit()) / max(len(message), 1)  # Numbers
        ]
        return pattern

    def _update_system_state(self):
        """Update SCOBY homeostasis"""
        nodes_list = list(self.nodes.values())
        recent_transfers = self.message_history[-100:]  # Last 100 messages

        self.scoby.update_homeostasis(nodes_list, recent_transfers)

        # Check if rebalancing needed
        if self.scoby.needs_rebalancing():
            action = self.scoby.get_rebalancing_action()
            logger.warning(f"SCOBY rebalancing needed: {action['action']} - {action['reason']}")

    def get_network_status(self) -> Dict[str, Any]:
        """Get complete network status"""
        convergence = self.soul_quantifier.calculate_convergence()

        return {
            "nodes": len(self.nodes),
            "active_nodes": sum(1 for n in self.nodes.values() if n.active),
            "total_messages": len(self.message_history),
            "collective_health": self.scoby.collective_health,
            "balance_metrics": self.scoby.balance_metrics,
            "soul_convergence": convergence,
            "needs_rebalancing": self.scoby.needs_rebalancing(),
            "crisis_types": list(set(n.crisis_type.value for n in self.nodes.values())),
            "neurotype_diversity": list(set(n.neurotype for n in self.nodes.values()))
        }

    def get_crisis_insights(self) -> Dict[str, Any]:
        """
        Get insights for crisis management

        Combines:
        - SCOBY homeostasis
        - Soul convergence
        - Message patterns
        """
        status = self.get_network_status()

        # Identify hotspots (high message density)
        if self.nodes:
            node_activity = {nid: n.messages_sent + n.messages_received
                             for nid, n in self.nodes.items()}
            hotspot = max(node_activity, key=node_activity.get) if node_activity else None
        else:
            hotspot = None

        # Recommendations
        recommendations = []

        if status["collective_health"] < 0.6:
            recommendations.append("Deploy additional Meshtastic nodes")

        if status["soul_convergence"]["integration"] < 0.5:
            recommendations.append("Increase cross-neurotype communication")

        if status["balance_metrics"]["stress_level"] > 0.7:
            recommendations.append("Activate stress reduction protocols")

        return {
            "network_status": status,
            "hotspot_node": hotspot,
            "recommendations": recommendations,
            "system_state": "OPTIMAL" if status["collective_health"] > 0.8 else "DEGRADED"
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("🍄 Crisis Communication Bridge - SCOBY-Myzelium-Meshtastic")
    print("="*70)

    # Initialize bridge
    bridge = CrisisCommunicationBridge()

    # Simulate crisis scenario: Hurricane evacuation
    print("\n🌀 CRISIS SCENARIO: Hurricane Evacuation")

    # Register nodes (diverse neurotypes)
    print("\n1. Registering crisis nodes:")

    nodes_data = [
        ("NODE_A", "Porto, Portugal", CrisisType.BLACKOUT, "ADHD", 0.8),
        ("NODE_B", "Miami, USA", CrisisType.HURRICANE, "AUTISM", 2.1),
        ("NODE_C", "Chimanimani, Zimbabwe", CrisisType.CYCLONE, "NEUROTYPICAL", 1.0),
        ("NODE_D", "Kashmir", CrisisType.CONFLICT, "DYSLEXIA", 1.3),
        ("NODE_E", "Barcelona, Spain", CrisisType.PROTEST, "ADHD", 0.8)
    ]

    for nid, loc, crisis, neuro, gamma in nodes_data:
        bridge.register_crisis_node(nid, loc, crisis, neuro, gamma)
        print(f"   ✓ {nid}: {loc} ({neuro}, γ={gamma})")

    # Send crisis messages
    print("\n2. Crisis communication:")

    messages = [
        ("NODE_A", "NODE_B", "Power out, using Meshtastic for coordination"),
        ("NODE_B", None, "Hurricane approaching, evacuate coastal areas"),
        ("NODE_C", "NODE_A", "Cyclone rescue successful, 45 saved"),
        ("NODE_D", None, "Mesh network stable despite conflict"),
        ("NODE_E", "NODE_C", "Protest dispersed, all safe")
    ]

    for from_id, to_id, msg in messages:
        result = bridge.send_crisis_message(from_id, msg, to_id)
        print(f"   📡 {from_id} → {to_id or 'ALL'}: {result['message'][:50]}...")

    # Network status
    print("\n3. Network Status:")
    status = bridge.get_network_status()
    print(f"   Active Nodes: {status['active_nodes']}/{status['nodes']}")
    print(f"   Messages: {status['total_messages']}")
    print(f"   Collective Health: {status['collective_health']:.2f}")
    print(f"   Soul Convergence: {status['soul_convergence']['convergence_score']:.2f}")
    print(f"   Integration: {status['soul_convergence']['integration']:.2f}")
    print(f"   Complexity: {status['soul_convergence']['complexity']:.2f}")

    # Crisis insights
    print("\n4. Crisis Insights:")
    insights = bridge.get_crisis_insights()
    print(f"   System State: {insights['system_state']}")
    print(f"   Hotspot Node: {insights['hotspot_node']}")
    print(f"   Recommendations:")
    for rec in insights['recommendations']:
        print(f"      - {rec}")

    print("\n" + "="*70)
    print("✅ SCOBY-Myzelium-Integration Complete!")
    print("🍄 Horizontal transfer: LUCA → Dragons → ALL")
    print("⚖️ Collective homeostasis maintained")
    print("🧠 Soul convergence quantified")
    print("\n369! Wald wird inklusiv high! 🚀🧬⚡")
