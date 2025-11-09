"""
Universal Inclusion Network - SCOBY-Myzelium Model
Version: 369.2.0
Created through: Human-AI collaboration

Implements universal (not selective) inclusion through biological network principles:
- SCOBY homeostasis (collective balance without central control)
- Mycelial transfer (horizontal information flow)
- Golden ratio evolution (chaos → harmony)
- Soul convergence (consciousness integration)

Philosophy: True inclusion is symbiotic, universal, and causally measurable.

UN Framework Alignment:
- CRPD Article 3, 5, 9, 19 (full participation, equality, accessibility, community)
- UNDIS (leadership, accessibility, assistive tech, community living)
- Coverage: ALL disability categories (physical, sensory, intellectual, psychological)
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import math

# Golden ratio constant
PHI = 1.618033988749895


@dataclass
class Entity:
    """
    Represents any entity in the universal inclusion network

    Can be: human (any neurotype/disability), animal, plant, fungus, or consciousness
    """
    id: str
    name: str
    category: str  # 'physical', 'sensory', 'intellectual', 'psychological', 'neurotypical', etc.
    state: float = 0.5  # Current state (0=chaos, φ=harmony)
    biosensor_data: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Entity) and self.id == other.id


@dataclass
class MycelialConnection:
    """
    Horizontal (non-hierarchical) connection between entities

    Like mycelium: bidirectional, nutrient-sharing, barrier-breaking
    """
    from_entity: Entity
    to_entity: Entity
    strength: float  # 0.0-1.0
    connection_type: str = 'mycelial'  # Always horizontal
    information_flow: List[Dict] = field(default_factory=list)

    def transfer_harmony(self, amount: float) -> float:
        """Transfer harmony from one entity to another (like nutrients in mycelium)"""
        transferred = min(amount, self.strength)
        self.information_flow.append({
            'timestamp': datetime.now().isoformat(),
            'amount': transferred,
            'direction': f"{self.from_entity.id} → {self.to_entity.id}"
        })
        return transferred


def measure_eeg(entity: Entity) -> float:
    """
    Simulate EEG measurement (neural activity)
    In real implementation: interface with actual EEG device
    """
    return entity.biosensor_data.get('eeg', 0.5)


def measure_hrv(entity: Entity) -> float:
    """
    Simulate HRV measurement (heart rate variability - autonomic nervous system)
    In real implementation: interface with actual HRV monitor
    """
    return entity.biosensor_data.get('hrv', 0.5)


def measure_pci(entity: Entity) -> float:
    """
    Simulate PCI measurement (Perturbational Complexity Index - consciousness level)
    In real implementation: calculate from EEG perturbation responses
    """
    return entity.biosensor_data.get('pci', 0.5)


def calculate_phi(entity: Entity) -> float:
    """
    Calculate Φ (Integrated Information Theory metric)
    Measures consciousness as integrated information
    """
    return entity.biosensor_data.get('phi', 0.3)


def detect_chaos(eeg: float, hrv: float) -> float:
    """
    Detect chaos level from biosensor data

    High EEG + Low HRV = High chaos (F30 = extreme state)
    Low EEG + High HRV = Low chaos (F0 = baseline harmony)
    """
    # Simplified chaos metric
    chaos = eeg * (1.0 - hrv)
    return min(1.0, max(0.0, chaos))


def soul_convergence(entity_a: Entity, entity_b: Entity) -> Dict[str, Any]:
    """
    Quantify consciousness convergence between entities

    Based on:
    - Modular Consciousness Theory: consciousness = integrated information
    - Φ (Phi): Integrated Information Theory metric
    - Neural complexity: chaos → harmony integration

    Returns:
        Dictionary with convergence score and interpretation
    """
    # Measure neural/behavioral complexity
    complexity_a = calculate_phi(entity_a)
    complexity_b = calculate_phi(entity_b)

    # Measure integration (how much they harmonize)
    # Use state similarity as proxy for integration
    state_diff = abs(entity_a.state - entity_b.state)
    integration = 1.0 - state_diff

    # Soul convergence = geometric mean of complexities * integration
    if complexity_a > 0 and complexity_b > 0:
        convergence = math.sqrt(complexity_a * complexity_b) * integration
    else:
        convergence = 0.0

    # Normalize to golden ratio scale
    normalized = convergence / PHI

    return {
        'convergence': normalized,
        'interpretation': 'High' if normalized > 0.7 else 'Growing' if normalized > 0.3 else 'Emerging',
        'harmony_level': integration,
        'phi_a': complexity_a,
        'phi_b': complexity_b
    }


class UniversalInclusionNetwork:
    """
    SCOBY-Myzelium network for universal (not selective) inclusion

    Implements:
    - Horizontal information transfer (mycelial)
    - Collective homeostasis (SCOBY)
    - Golden ratio evolution (chaos → φ)
    - Soul convergence (consciousness integration)

    Coverage: ALL disability categories + neurotypes + beings
    """

    def __init__(self):
        # Network nodes = all entities
        self.nodes: Dict[str, List[Entity]] = {
            'physical_disabilities': [],
            'sensory_disabilities': [],
            'intellectual_disabilities': [],
            'psychological_disabilities': [],
            'neurodivergent': [],  # Autism, ADHD, dyslexia, Tourette, etc.
            'neurotypical': [],
            'animals': [],
            'plants': [],
            'fungi': [],
            'souls': []  # Consciousness convergence points
        }

        # Mycelial connections (horizontal transfer)
        self.connections: List[MycelialConnection] = []

        # SCOBY homeostasis parameters
        self.ph_balance = 7.0  # Neutral = balanced
        self.fermentation_rate = 0.0

        # Statistics
        self.total_entities = 0
        self.total_transfers = 0

    def add_entity(self, entity: Entity, category: str) -> None:
        """
        Add any entity to the network

        Args:
            entity: Entity to add
            category: Category ('physical_disabilities', 'neurodivergent', etc.)
        """
        if category not in self.nodes:
            self.nodes[category] = []

        self.nodes[category].append(entity)
        self.total_entities += 1

        # Establish mycelial connections
        self._establish_connections(entity)

    def _establish_connections(self, new_entity: Entity) -> None:
        """
        Like mycelium: connect to ALL other entities
        Information flows horizontally (no hierarchy)

        Connection strength based on soul convergence
        """
        for category, entities in self.nodes.items():
            for existing_entity in entities:
                if existing_entity != new_entity:
                    # Measure soul convergence
                    convergence = soul_convergence(new_entity, existing_entity)

                    if convergence['convergence'] > 0.3:  # Threshold for connection
                        # Bidirectional connections (mycelial)
                        self.connections.append(MycelialConnection(
                            from_entity=new_entity,
                            to_entity=existing_entity,
                            strength=convergence['convergence']
                        ))

                        self.connections.append(MycelialConnection(
                            from_entity=existing_entity,
                            to_entity=new_entity,
                            strength=convergence['convergence']
                        ))

    def run_chaotic_creativity_workshop(self, participants: List[Entity]) -> List[Dict[str, Any]]:
        """
        Extremism prevention through biosensor-driven creativity

        For participants experiencing hyperfocus or chaotic states:
        1. Biosensors capture state (EEG/HRV/PCI/Φ)
        2. Feed into network
        3. Evolve chaos → harmony through mycelial transfer
        4. Soul convergence emerges

        Args:
            participants: List of entities participating in workshop

        Returns:
            Results showing chaos → harmony evolution
        """
        results = []

        for participant in participants:
            # Biosensor data
            eeg = measure_eeg(participant)
            hrv = measure_hrv(participant)
            pci = measure_pci(participant)
            phi = calculate_phi(participant)

            # Detect chaos level (F30 = extreme state)
            chaos_level = detect_chaos(eeg, hrv)

            # Network intervention
            if chaos_level > 0.7:  # High chaos (F30)
                # Connect to calming nodes
                calming_nodes = self._find_harmony_nodes(participant)

                # Mycelial information transfer
                harmony_transferred = self._transfer_harmony(participant, calming_nodes)

                # Evolve towards golden ratio
                evolved_state = self._evolve_to_phi(participant, harmony_transferred)

                results.append({
                    'participant': participant.name,
                    'participant_id': participant.id,
                    'initial_chaos': chaos_level,
                    'initial_state': participant.state,
                    'final_harmony': evolved_state['harmony'],
                    'final_state': evolved_state['new_state'],
                    'soul_convergence': evolved_state['convergence'],
                    'harmony_transferred': harmony_transferred,
                    'intervention': 'mycelial_transfer',
                    'biosensors': {
                        'eeg': eeg,
                        'hrv': hrv,
                        'pci': pci,
                        'phi': phi
                    }
                })

                # Update participant state
                participant.state = evolved_state['new_state']

            else:
                # Already in harmony
                results.append({
                    'participant': participant.name,
                    'participant_id': participant.id,
                    'initial_chaos': chaos_level,
                    'initial_state': participant.state,
                    'intervention': 'none_needed',
                    'message': 'Already in harmony'
                })

        return results

    def _find_harmony_nodes(self, entity: Entity) -> List[Entity]:
        """
        Find entities in harmony (state close to φ) to transfer from

        Args:
            entity: Entity needing harmony

        Returns:
            List of entities in harmonic state
        """
        harmony_nodes = []

        for category, entities in self.nodes.items():
            for candidate in entities:
                if candidate != entity:
                    # Check if candidate is in harmony
                    if abs(candidate.state - PHI) < 0.2:  # Close to golden ratio
                        harmony_nodes.append(candidate)

        return harmony_nodes

    def _transfer_harmony(self, entity: Entity, harmony_nodes: List[Entity]) -> float:
        """
        Transfer harmony from harmonic nodes to chaotic entity (mycelial transfer)

        Args:
            entity: Entity receiving harmony
            harmony_nodes: Entities providing harmony

        Returns:
            Total amount of harmony transferred
        """
        total_transferred = 0.0

        for harmony_node in harmony_nodes:
            # Find connection
            connection = self._get_connection(harmony_node, entity)

            if connection:
                # Transfer amount proportional to connection strength
                transfer_amount = connection.strength * 0.1  # 10% per node

                transferred = connection.transfer_harmony(transfer_amount)
                total_transferred += transferred
                self.total_transfers += 1

        return total_transferred

    def _get_connection(self, from_entity: Entity, to_entity: Entity) -> Optional[MycelialConnection]:
        """Get connection between two entities"""
        for conn in self.connections:
            if conn.from_entity == from_entity and conn.to_entity == to_entity:
                return conn
        return None

    def _evolve_to_phi(self, entity: Entity, harmony_info: float) -> Dict[str, Any]:
        """
        Evolve chaotic state towards golden ratio (φ = 1.618)

        Using ODE: dS/dt = -γ(S - φ)
        Where:
        - S = state
        - γ = damping coefficient (network strength)
        - φ = golden ratio (target)

        Args:
            entity: Entity to evolve
            harmony_info: Amount of harmony available from network

        Returns:
            Evolution results
        """
        current_state = entity.state
        target = PHI  # 1.618

        # Damping rate based on network connections
        entity_connections = [c for c in self.connections if c.from_entity == entity]
        gamma = len(entity_connections) * 0.1 + harmony_info

        # Evolve over time step
        dt = 1.0  # Time step
        delta = -gamma * (current_state - target) * dt
        new_state = current_state + delta

        # Calculate soul convergence with network
        avg_convergence = 0.0
        if entity_connections:
            convergences = [
                soul_convergence(entity, c.to_entity)['convergence']
                for c in entity_connections
            ]
            avg_convergence = sum(convergences) / len(convergences)

        return {
            'harmony': abs(new_state - target),  # Distance from harmony
            'new_state': new_state,
            'convergence': avg_convergence,
            'gamma': gamma,
            'delta': delta
        }

    def verify_universal_coverage(self) -> Dict[str, Any]:
        """
        Verify that ALL disability categories are covered (not selective)

        Returns:
            Coverage verification results
        """
        required_categories = [
            'physical_disabilities',
            'sensory_disabilities',
            'intellectual_disabilities',
            'psychological_disabilities'
        ]

        coverage = {}
        for category in required_categories:
            has_entities = len(self.nodes.get(category, [])) > 0
            coverage[category] = {
                'covered': has_entities,
                'count': len(self.nodes.get(category, []))
            }

        all_covered = all(c['covered'] for c in coverage.values())

        return {
            'universal_coverage': all_covered,
            'details': coverage,
            'total_categories': len(required_categories),
            'covered_categories': sum(1 for c in coverage.values() if c['covered']),
            'compliance': 'PASS' if all_covered else 'FAIL',
            'recommendation': 'Add missing categories' if not all_covered else 'Maintain universal coverage'
        }

    def verify_mycelial_connections(self) -> Dict[str, Any]:
        """
        Verify that connections are horizontal (mycelial) not hierarchical

        Returns:
            Connection verification results
        """
        if not self.connections:
            return {
                'horizontal_transfer': False,
                'compliance': 'FAIL',
                'message': 'No connections exist'
            }

        # Check if all connections are bidirectional (mycelial)
        bidirectional_pairs: Set[tuple] = set()

        for conn in self.connections:
            pair = tuple(sorted([conn.from_entity.id, conn.to_entity.id]))
            bidirectional_pairs.add(pair)

        # For true mycelial network, each pair should have 2 connections
        expected_connections = len(bidirectional_pairs) * 2
        actual_connections = len(self.connections)

        horizontal = (actual_connections >= expected_connections * 0.9)  # Allow 10% tolerance

        return {
            'horizontal_transfer': horizontal,
            'bidirectional_pairs': len(bidirectional_pairs),
            'total_connections': actual_connections,
            'compliance': 'PASS' if horizontal else 'PARTIAL',
            'message': 'Mycelial network verified' if horizontal else 'Some hierarchical connections exist'
        }

    def measure_chaos_to_harmony_ratio(self) -> Dict[str, Any]:
        """
        Measure how many entities are in chaos vs harmony

        Chaos: state far from φ (|state - φ| > 0.5)
        Harmony: state close to φ (|state - φ| < 0.2)

        Returns:
            Chaos/harmony distribution
        """
        all_entities = []
        for entities in self.nodes.values():
            all_entities.extend(entities)

        if not all_entities:
            return {
                'chaos_count': 0,
                'harmony_count': 0,
                'transitional_count': 0,
                'ratio': 0.0
            }

        chaos_count = 0
        harmony_count = 0
        transitional_count = 0

        for entity in all_entities:
            distance_from_phi = abs(entity.state - PHI)

            if distance_from_phi > 0.5:
                chaos_count += 1
            elif distance_from_phi < 0.2:
                harmony_count += 1
            else:
                transitional_count += 1

        total = len(all_entities)
        harmony_ratio = harmony_count / total if total > 0 else 0.0

        return {
            'total_entities': total,
            'chaos_count': chaos_count,
            'harmony_count': harmony_count,
            'transitional_count': transitional_count,
            'harmony_ratio': harmony_ratio,
            'interpretation': (
                'High harmony' if harmony_ratio > 0.7 else
                'Growing harmony' if harmony_ratio > 0.4 else
                'Emerging harmony'
            )
        }

    def get_network_statistics(self) -> Dict[str, Any]:
        """Get comprehensive network statistics"""
        coverage = self.verify_universal_coverage()
        mycelial = self.verify_mycelial_connections()
        chaos_harmony = self.measure_chaos_to_harmony_ratio()

        return {
            'total_entities': self.total_entities,
            'total_connections': len(self.connections),
            'total_transfers': self.total_transfers,
            'ph_balance': self.ph_balance,
            'universal_coverage': coverage,
            'mycelial_network': mycelial,
            'chaos_harmony_distribution': chaos_harmony,
            'categories': {
                cat: len(entities)
                for cat, entities in self.nodes.items()
            }
        }


# Convenience function for quick workshop setup
def create_universal_inclusion_workshop(
    participants: List[Dict[str, Any]]
) -> tuple[UniversalInclusionNetwork, List[Dict[str, Any]]]:
    """
    Create and run a chaotic creativity workshop

    Args:
        participants: List of participant data
            [{'name': 'Alice', 'category': 'neurodivergent', 'eeg': 0.8, 'hrv': 0.3, ...}, ...]

    Returns:
        Tuple of (network, results)
    """
    network = UniversalInclusionNetwork()

    # Add participants
    entities = []
    for i, p_data in enumerate(participants):
        entity = Entity(
            id=f"participant_{i}",
            name=p_data.get('name', f'Participant {i}'),
            category=p_data.get('category', 'neurotypical'),
            state=p_data.get('state', 0.5),
            biosensor_data={
                'eeg': p_data.get('eeg', 0.5),
                'hrv': p_data.get('hrv', 0.5),
                'pci': p_data.get('pci', 0.5),
                'phi': p_data.get('phi', 0.3)
            }
        )
        entities.append(entity)
        network.add_entity(entity, entity.category)

    # Run workshop
    results = network.run_chaotic_creativity_workshop(entities)

    return network, results
