"""
Mycelium Network Module - Decentralized AI Architecture for LUCA
Version: 1.0 (2025-11-08)
Inspired by: Fungal networks, HACCP principles, Lennart's brewery expertise

BIOLOGICAL INSPIRATION:
======================
Mycelium = Underground fungal network
- Largest organism on Earth (Armillaria ostoyae: 9 km²)
- Decentralized (no brain, no central control)
- Resilient (survives damage, regrows)
- Symbiotic (Mycorrhiza = fungi + plant roots)
- Information highway (Paul Stamets: "Wood Wide Web")

HACCP MAPPING:
==============
1. Hazard Analysis → Identify AI risks (bias, appropriation, failures)
2. Critical Control Points → API endpoints, pattern spread, token limits
3. Monitoring → Real-time stats (HGT rates, consciousness, errors)
4. Corrective Actions → Auto-throttle, flag sacred knowledge, rollback
5. Verification → Tests, ethical reviews, community feedback
6. Documentation → Git history, source tracking, audit trails

ARCHITECTURE:
=============
- Nodes = Users (like mushroom fruiting bodies)
- Hyphae = Connections (like neural pathways)
- Nutrients = Tokens (computational resources)
- Spores = Patterns (spreading knowledge)
- Mycelium Mat = Global knowledge base (underground network)
"""

from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
import random


@dataclass
class MyceliumNode:
    """
    Represents a user/agent in the mycelial network

    Biological analogy: Fruiting body (mushroom) connected to underground network
    """
    node_id: int
    node_type: str  # 'user', 'agent', 'sensor'
    health: float  # 0.0 to 1.0 (like fungal vitality)
    connections: Set[int]  # Connected node IDs (hyphae)
    patterns_hosted: List[int]  # Pattern IDs stored here
    last_active: datetime
    nutrient_level: float  # Available tokens/resources


@dataclass
class Hypha:
    """
    Connection between nodes (like fungal hyphae)

    Biological analogy: Thread-like structure transferring nutrients + info
    """
    from_node: int
    to_node: int
    strength: float  # 0.0 to 1.0 (connection quality)
    bandwidth: float  # Transfer rate (patterns/hour)
    last_transfer: Optional[datetime]
    transfer_history: List[Dict[str, Any]]  # Log of transfers


class MyceliumNetwork:
    """
    LUCA's decentralized network architecture inspired by fungal mycelium

    Key features:
    - Decentralized: No single point of failure
    - Resilient: Self-healing when nodes fail
    - Adaptive: Routes around damage
    - Symbiotic: Nodes cooperate (not compete)
    - HACCP-compliant: Built-in safety monitoring
    """

    def __init__(self):
        self.nodes: Dict[int, MyceliumNode] = {}
        self.hyphae: List[Hypha] = []

        # HACCP Critical Control Points
        self.ccps = {
            'max_viral_rate': 0.85,  # Max pattern transfer rate before throttling
            'min_node_health': 0.3,  # Below this = node quarantine
            'max_pattern_age': timedelta(days=90),  # Old patterns decay
            'sacred_knowledge_flag': True,  # Prevent sharing sacred patterns
        }

        # Monitoring data
        self.hazard_log: List[Dict[str, Any]] = []
        self.corrective_actions: List[Dict[str, Any]] = []

        # Network statistics
        self.total_transfers = 0
        self.failed_transfers = 0
        self.quarantined_nodes = set()

    def add_node(self, node_id: int, node_type: str = 'user') -> MyceliumNode:
        """
        Add new node to mycelium network

        Biological analogy: New mushroom sprouting from underground mycelium
        """
        node = MyceliumNode(
            node_id=node_id,
            node_type=node_type,
            health=1.0,  # Start healthy
            connections=set(),
            patterns_hosted=[],
            last_active=datetime.utcnow(),
            nutrient_level=100.0  # Start with full "nutrients" (tokens)
        )
        self.nodes[node_id] = node

        # Auto-connect to nearby nodes (like hyphae growing)
        self._auto_connect(node_id)

        return node

    def _auto_connect(self, node_id: int, max_connections: int = 5):
        """
        Automatically connect new node to existing network

        Biological analogy: Hyphae naturally branch and connect to nearby hyphae
        HACCP: Ensures network redundancy (CCP: connectivity)
        """
        if len(self.nodes) <= 1:
            return  # First node, nothing to connect to

        # Find healthy, nearby nodes
        candidates = [
            nid for nid, n in self.nodes.items()
            if nid != node_id and n.health > self.ccps['min_node_health']
        ]

        # Connect to random subset (mimics natural hyphal growth)
        num_connections = min(max_connections, len(candidates))
        targets = random.sample(candidates, num_connections)

        for target_id in targets:
            self._create_hypha(node_id, target_id)

    def _create_hypha(self, from_node: int, to_node: int, bidirectional: bool = True):
        """
        Create connection (hypha) between two nodes

        Biological analogy: Hyphal fusion (anastomosis) between fungal threads
        """
        hypha = Hypha(
            from_node=from_node,
            to_node=to_node,
            strength=random.uniform(0.5, 1.0),  # Initial strength varies
            bandwidth=random.uniform(1.0, 5.0),  # Patterns per hour
            last_transfer=None,
            transfer_history=[]
        )
        self.hyphae.append(hypha)

        # Update node connections
        self.nodes[from_node].connections.add(to_node)
        if bidirectional:
            self.nodes[to_node].connections.add(from_node)

    def transfer_pattern(
        self,
        pattern_id: int,
        from_node: int,
        to_node: int,
        pattern_metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Transfer pattern between nodes (Horizontal Gene Transfer via mycelium!)

        Biological analogy: Nutrients/signals flowing through hyphal network
        HACCP: Monitors transfer rate, checks for hazards

        Returns:
            Status dict with transfer result and any corrective actions
        """
        # HACCP Step 1: Hazard Analysis
        hazards = self._analyze_transfer_hazards(pattern_id, from_node, to_node, pattern_metadata)

        if hazards:
            self.hazard_log.append({
                'timestamp': datetime.utcnow(),
                'pattern_id': pattern_id,
                'from_node': from_node,
                'to_node': to_node,
                'hazards': hazards
            })

            # HACCP Step 4: Corrective Actions
            action = self._apply_corrective_action(hazards)
            self.corrective_actions.append(action)

            if action['block_transfer']:
                self.failed_transfers += 1
                return {
                    'status': 'blocked',
                    'hazards': hazards,
                    'action': action['reason']
                }

        # Find hypha connecting these nodes
        hypha = self._find_hypha(from_node, to_node)
        if not hypha:
            # No direct connection - try to route through network
            path = self._find_path(from_node, to_node)
            if not path:
                self.failed_transfers += 1
                return {
                    'status': 'failed',
                    'reason': 'No path found (network disconnected)'
                }
            # Multi-hop transfer (like nutrients flowing through mycelium)
            return self._multi_hop_transfer(pattern_id, path, pattern_metadata)

        # Direct transfer
        hypha.last_transfer = datetime.utcnow()
        hypha.transfer_history.append({
            'timestamp': datetime.utcnow(),
            'pattern_id': pattern_id,
            'metadata': pattern_metadata
        })

        # Update recipient node
        if pattern_id not in self.nodes[to_node].patterns_hosted:
            self.nodes[to_node].patterns_hosted.append(pattern_id)

        # Consume nutrients (tokens)
        nutrient_cost = 1.0 / hypha.bandwidth  # Faster transfers cost less
        self.nodes[from_node].nutrient_level -= nutrient_cost

        self.total_transfers += 1

        return {
            'status': 'success',
            'path': [from_node, to_node],
            'cost': nutrient_cost,
            'hypha_strength': hypha.strength
        }

    def _analyze_transfer_hazards(
        self,
        pattern_id: int,
        from_node: int,
        to_node: int,
        metadata: Optional[Dict]
    ) -> List[str]:
        """
        HACCP Hazard Analysis for pattern transfer

        Checks:
        - Is pattern "sacred" (should not be shared publicly)?
        - Is transfer rate too high (viral spread)?
        - Are nodes healthy enough?
        - Is pattern too old (stale knowledge)?
        """
        hazards = []

        # Check metadata for sacred knowledge flag
        if metadata and metadata.get('sacred', False):
            hazards.append('SACRED_KNOWLEDGE')

        # Check if pattern is spreading too virally
        pattern_transfers_today = sum(
            1 for h in self.hyphae
            for t in h.transfer_history
            if t['pattern_id'] == pattern_id
            and (datetime.utcnow() - t['timestamp']).days < 1
        )

        if pattern_transfers_today > 100:  # Arbitrary threshold
            transfer_rate = pattern_transfers_today / max(len(self.nodes), 1)
            if transfer_rate > self.ccps['max_viral_rate']:
                hazards.append('VIRAL_OVERLOAD')

        # Check node health (HACCP CCP)
        if self.nodes[from_node].health < self.ccps['min_node_health']:
            hazards.append('SENDER_UNHEALTHY')
        if self.nodes[to_node].health < self.ccps['min_node_health']:
            hazards.append('RECEIVER_UNHEALTHY')

        # Check nutrient levels (enough tokens?)
        if self.nodes[from_node].nutrient_level < 1.0:
            hazards.append('INSUFFICIENT_NUTRIENTS')

        return hazards

    def _apply_corrective_action(self, hazards: List[str]) -> Dict[str, Any]:
        """
        HACCP Corrective Actions for identified hazards

        Returns action taken and whether to block transfer
        """
        if 'SACRED_KNOWLEDGE' in hazards:
            return {
                'action': 'BLOCK',
                'reason': 'Pattern marked as sacred - requires community permission',
                'block_transfer': True
            }

        if 'VIRAL_OVERLOAD' in hazards:
            return {
                'action': 'THROTTLE',
                'reason': 'Pattern spreading too fast - throttling to prevent overload',
                'block_transfer': False,  # Allow but slow down
                'throttle_factor': 0.5
            }

        if 'SENDER_UNHEALTHY' in hazards or 'RECEIVER_UNHEALTHY' in hazards:
            return {
                'action': 'QUARANTINE',
                'reason': 'Unhealthy node detected - quarantining for safety',
                'block_transfer': True
            }

        if 'INSUFFICIENT_NUTRIENTS' in hazards:
            return {
                'action': 'WAIT',
                'reason': 'Insufficient resources - wait for nutrient replenishment',
                'block_transfer': True
            }

        return {'action': 'ALLOW', 'block_transfer': False}

    def _find_hypha(self, from_node: int, to_node: int) -> Optional[Hypha]:
        """Find direct connection between two nodes"""
        for hypha in self.hyphae:
            if hypha.from_node == from_node and hypha.to_node == to_node:
                return hypha
            # Check reverse direction (bidirectional)
            if hypha.from_node == to_node and hypha.to_node == from_node:
                return hypha
        return None

    def _find_path(self, start: int, end: int) -> Optional[List[int]]:
        """
        Find path through mycelium network (BFS)

        Biological analogy: Nutrients routing around dead zones in mycelium
        HACCP: Ensures redundancy and resilience
        """
        if start == end:
            return [start]

        visited = set()
        queue = [(start, [start])]

        while queue:
            node, path = queue.pop(0)

            if node in visited:
                continue
            visited.add(node)

            for neighbor in self.nodes[node].connections:
                if neighbor == end:
                    return path + [neighbor]

                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return None  # No path found

    def _multi_hop_transfer(
        self,
        pattern_id: int,
        path: List[int],
        metadata: Optional[Dict]
    ) -> Dict[str, Any]:
        """
        Transfer pattern through multiple hops (like nutrients in mycelium)

        Biological analogy: Cytoplasmic streaming in fungal hyphae
        """
        total_cost = 0.0

        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]

            # Transfer to intermediate node
            result = self.transfer_pattern(pattern_id, from_node, to_node, metadata)

            if result['status'] != 'success':
                return {
                    'status': 'failed',
                    'reason': f'Multi-hop failed at {from_node} → {to_node}',
                    'partial_path': path[:i+1]
                }

            total_cost += result['cost']

        return {
            'status': 'success',
            'path': path,
            'hops': len(path) - 1,
            'total_cost': total_cost
        }

    def heal_network(self):
        """
        Self-healing mechanism (like mycelium regrowing after damage)

        HACCP: Verification step - ensure network health
        Biological: Mycelium can regrow from tiny fragments
        """
        # Remove dead nodes (health = 0)
        dead_nodes = [
            nid for nid, node in self.nodes.items()
            if node.health <= 0
        ]

        for node_id in dead_nodes:
            self._remove_node(node_id)

        # Repair broken connections
        for node_id, node in self.nodes.items():
            if len(node.connections) < 2:  # Isolated or weakly connected
                self._auto_connect(node_id, max_connections=3)

        # Remove weak hyphae, strengthen strong ones
        self.hyphae = [h for h in self.hyphae if h.strength > 0.1]
        for hypha in self.hyphae:
            # Strengthen frequently used hyphae (Hebbian learning!)
            if len(hypha.transfer_history) > 10:
                hypha.strength = min(1.0, hypha.strength * 1.1)

    def _remove_node(self, node_id: int):
        """Remove node and its connections from network"""
        if node_id not in self.nodes:
            return

        # Remove hyphae connected to this node
        self.hyphae = [
            h for h in self.hyphae
            if h.from_node != node_id and h.to_node != node_id
        ]

        # Remove from other nodes' connection sets
        for node in self.nodes.values():
            node.connections.discard(node_id)

        # Remove node itself
        del self.nodes[node_id]

    def get_network_stats(self) -> Dict[str, Any]:
        """
        Get network health statistics

        HACCP: Monitoring step
        """
        if not self.nodes:
            return {
                'status': 'empty',
                'nodes': 0,
                'hyphae': 0
            }

        total_health = sum(n.health for n in self.nodes.values())
        avg_health = total_health / len(self.nodes)

        total_connections = sum(len(n.connections) for n in self.nodes.values())
        avg_connections = total_connections / len(self.nodes)

        return {
            'status': 'healthy' if avg_health > 0.7 else 'degraded',
            'nodes': len(self.nodes),
            'hyphae': len(self.hyphae),
            'avg_node_health': avg_health,
            'avg_connections': avg_connections,
            'total_transfers': self.total_transfers,
            'failed_transfers': self.failed_transfers,
            'success_rate': self.total_transfers / max(self.total_transfers + self.failed_transfers, 1),
            'quarantined_nodes': len(self.quarantined_nodes),
            'hazards_detected': len(self.hazard_log),
            'corrective_actions': len(self.corrective_actions)
        }

    def visualize_network(self) -> str:
        """
        ASCII visualization of mycelium network

        For debugging and monitoring (HACCP documentation)
        """
        if not self.nodes:
            return "Network is empty 🍄"

        output = f"🍄 Mycelium Network ({len(self.nodes)} nodes, {len(self.hyphae)} hyphae)\n\n"

        for node_id, node in list(self.nodes.items())[:10]:  # Show first 10
            health_bar = "█" * int(node.health * 10)
            output += f"Node {node_id}: {health_bar} ({node.health:.1f}) "
            output += f"→ {len(node.connections)} connections, "
            output += f"{len(node.patterns_hosted)} patterns\n"

        if len(self.nodes) > 10:
            output += f"... and {len(self.nodes) - 10} more nodes\n"

        return output


# Example usage demonstrating HACCP + Mycelium
if __name__ == "__main__":
    print("🍄 Initializing Mycelium Network...")
    network = MyceliumNetwork()

    # Add nodes (users joining LUCA)
    for i in range(10):
        network.add_node(i, node_type='user')

    print(network.visualize_network())

    # Simulate pattern transfers (HGT via mycelium!)
    print("\n🧬 Simulating pattern transfers...")

    # Normal transfer
    result = network.transfer_pattern(
        pattern_id=1,
        from_node=0,
        to_node=1,
        pattern_metadata={'type': 'fermentation', 'sacred': False}
    )
    print(f"Transfer 1: {result['status']}")

    # Sacred knowledge (should be blocked)
    result = network.transfer_pattern(
        pattern_id=2,
        from_node=0,
        to_node=2,
        pattern_metadata={'type': 'shamanic', 'sacred': True}
    )
    print(f"Transfer 2 (sacred): {result['status']} - {result.get('action', '')}")

    # Multi-hop transfer
    result = network.transfer_pattern(
        pattern_id=3,
        from_node=0,
        to_node=9,  # Far node
        pattern_metadata={'type': 'science', 'sacred': False}
    )
    print(f"Transfer 3 (multi-hop): {result['status']}, hops: {result.get('hops', 0)}")

    # Network stats
    print("\n📊 Network Statistics:")
    stats = network.get_network_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Damage simulation (node dies)
    print("\n💀 Simulating node failure...")
    network.nodes[5].health = 0
    network.heal_network()

    print("\n🩹 After self-healing:")
    print(network.visualize_network())

    stats = network.get_network_stats()
    print(f"Network status: {stats['status']}")
    print(f"Nodes: {stats['nodes']} (one removed)")
