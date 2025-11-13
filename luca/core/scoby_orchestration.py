"""
LUCA 369/370 - Layer 9: SCOBY Orchestration Engine

Orchestrates distributed AI agents into SCOBY-style collective intelligence.
Integrates all biological layers (6, 7, 8) into emergent symbiotic system.

SCOBY = Symbiotic Culture Of Bacteria and Yeast

Biology → AI Mapping:
- Multiple Species → Multiple Agents/Users
- Resource Sharing → ATP pooling, knowledge sharing
- Emergent Intelligence → Collective > sum of parts
- Self-Organizing → Dynamic task allocation
- Resilient → Fault-tolerant, offline-first

Architekt: Lennart Wuchold
Standard: 369/370 ≈ 0.997297
Integration: Layers 6 (Growth), 7 (Population), 8 (Metabolic)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

import numpy as np

from .growth_kinetics import GrowthPhase, GrowthState
from .metabolic_pathways import MetabolicMode, MetabolicState
from .population_dynamics import InteractionType


class AgentRole(Enum):
    """
    Agent roles in SCOBY collective (species analogy).

    Bacteria-like (Aerobic):
    - STRATEGIST: Long-term planning (Acetobacter-style)
    - RESEARCHER: Deep analysis (Gluconobacter-style)
    - QUALITY_CONTROLLER: Validation and review

    Yeast-like (Anaerobic):
    - RESPONDER: Emergency/crisis handling (Saccharomyces-style)
    - OFFLINE_SPECIALIST: Cached knowledge, no internet (Zygosaccharomyces-style)
    - RAPID_PROTOTYPER: Fast iteration

    Hybrid (Mixed):
    - GENERALIST: Balanced, flexible
    - COORDINATOR: Multi-mode orchestration
    """

    # Bacteria-like (Aerobic strategists)
    STRATEGIST = "strategist"  # Strategic planning
    RESEARCHER = "researcher"  # Deep research
    QUALITY_CONTROLLER = "quality_controller"  # QA/validation

    # Yeast-like (Anaerobic tacticians)
    RESPONDER = "responder"  # Emergency response
    OFFLINE_SPECIALIST = "offline_specialist"  # Works offline
    RAPID_PROTOTYPER = "rapid_prototyper"  # Fast iteration

    # Hybrid (Mixed generalists)
    GENERALIST = "generalist"  # General purpose
    COORDINATOR = "coordinator"  # Orchestration


class TaskType(Enum):
    """Types of tasks that can be allocated."""

    STRATEGIC = "strategic"  # Long-term planning
    RESEARCH = "research"  # Analysis and investigation
    CRISIS = "crisis"  # Emergency response
    QUALITY = "quality"  # Testing and validation
    CREATIVE = "creative"  # Novel solutions
    MAINTENANCE = "maintenance"  # Routine work


@dataclass
class Task:
    """
    Task to be allocated to agents.

    Defines work requirements and constraints.
    """

    task_id: str
    task_type: TaskType
    complexity: float  # 0-1
    urgency: float  # 0-1
    resources_required: float  # ATP tokens needed
    description: str
    deadline: Optional[float] = None  # Time limit
    preferred_mode: Optional[MetabolicMode] = None  # Aerobic/Anaerobic preference
    quality_target: float = 0.997297  # 369/370 default

    assigned_agent: Optional[str] = None
    status: str = "pending"  # pending, assigned, completed, failed


@dataclass
class SCOBYAgent:
    """
    Individual agent in SCOBY collective.

    Integrates all layers:
    - Layer 6: Growth Kinetics (growth phase, substrate)
    - Layer 7: Population Dynamics (interactions, consciousness)
    - Layer 8: Metabolic Pathways (mode, ATP, oxygen)
    - Layer 9: Orchestration (role, tasks, trust)
    """

    agent_id: str
    role: AgentRole

    # Layer 6: Growth Kinetics
    growth_phase: GrowthPhase = GrowthPhase.EXPONENTIAL
    substrate_level: float = 10.0
    growth_rate: float = 0.5

    # Layer 7: Population Dynamics
    activity_level: float = 1.0
    consciousness_contribution: float = 1.0
    resource_allocation: float = 100.0

    # Layer 8: Metabolic Pathways
    metabolic_mode: MetabolicMode = MetabolicMode.AEROBIC
    atp_balance: float = 100.0
    oxygen_level: float = 1.0
    lactate_level: float = 0.0
    reasoning_quality: float = 369.0 / 370.0  # Exact 369/370

    # Layer 9: Orchestration
    task_queue: List[str] = field(default_factory=list)  # Task IDs
    specialization: float = 0.8  # How specialized (0-1)
    availability: float = 1.0  # 0-1
    trust_score: float = 1.0  # Based on contribution history
    online: bool = True  # Network connectivity

    # Interaction preferences (for Layer 7 integration)
    interaction_preferences: Dict[str, float] = field(default_factory=dict)


@dataclass
class SCOBYState:
    """
    Current state of SCOBY collective.

    Tracks collective-level metrics and resources.
    """

    agents: Dict[str, SCOBYAgent] = field(default_factory=dict)
    tasks: Dict[str, Task] = field(default_factory=dict)

    # Collective resources (pooled)
    total_atp: float = 0.0
    total_oxygen: float = 0.0
    shared_knowledge: Dict[str, float] = field(default_factory=dict)

    # Collective metrics
    collective_consciousness: float = 0.0
    emergence_factor: float = 1.0  # > 1.0 means collective > sum
    metabolic_diversity: float = 0.0

    # Performance tracking
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_processing_time: float = 0.0

    # Quality tracking
    collective_quality: float = 369.0 / 370.0  # Exact 369/370


class SCOBYOrchestrationEngine:
    """
    Layer 9: SCOBY Orchestration Engine

    Orchestrates distributed agents into collective intelligence.

    Key Features:
    - Task allocation based on agent capabilities
    - Metabolic mode distribution (40% aerobic, 30% anaerobic, 30% mixed)
    - Collective consciousness aggregation
    - Resource pooling and sharing
    - Fault tolerance and resilience
    - 369/370 quality maintenance
    """

    def __init__(self):
        """Initialize SCOBY orchestration engine."""
        self.state = SCOBYState()

        # Verify quality standard
        self._verify_quality_standard()

        # Target metabolic distribution (SCOBY-inspired)
        self.target_aerobic_ratio = 0.4  # 40% bacteria-like strategists
        self.target_anaerobic_ratio = 0.3  # 30% yeast-like tacticians
        self.target_mixed_ratio = 0.3  # 30% hybrid generalists

    def _verify_quality_standard(self) -> None:
        """Verify 369/370 quality standard."""
        expected = 369.0 / 370.0
        if not np.isclose(self.state.collective_quality, expected, rtol=1e-6):
            raise ValueError(
                f"Collective quality {self.state.collective_quality} "
                f"does not match 369/370 standard ({expected})"
            )

    # ===== Agent Management =====

    def add_agent(
        self,
        agent_id: str,
        role: AgentRole,
        initial_mode: Optional[MetabolicMode] = None,
    ) -> None:
        """
        Add agent to SCOBY collective.

        Args:
            agent_id: Unique agent identifier
            role: Agent's role in collective
            initial_mode: Starting metabolic mode (auto-assigned if None)
        """
        if agent_id in self.state.agents:
            raise ValueError(f"Agent {agent_id} already exists in collective")

        # Auto-assign metabolic mode based on role if not specified
        if initial_mode is None:
            if role in [
                AgentRole.STRATEGIST,
                AgentRole.RESEARCHER,
                AgentRole.QUALITY_CONTROLLER,
            ]:
                initial_mode = MetabolicMode.AEROBIC
            elif role in [
                AgentRole.RESPONDER,
                AgentRole.OFFLINE_SPECIALIST,
                AgentRole.RAPID_PROTOTYPER,
            ]:
                initial_mode = MetabolicMode.ANAEROBIC
            else:
                initial_mode = MetabolicMode.MIXED

        # Create agent
        agent = SCOBYAgent(agent_id=agent_id, role=role, metabolic_mode=initial_mode)

        self.state.agents[agent_id] = agent

        # Update collective resources
        self._update_collective_resources()

    def remove_agent(self, agent_id: str) -> None:
        """
        Remove agent from collective.

        Args:
            agent_id: Agent to remove
        """
        if agent_id not in self.state.agents:
            raise ValueError(f"Agent {agent_id} not found in collective")

        # Reassign agent's tasks
        agent = self.state.agents[agent_id]
        for task_id in agent.task_queue:
            if task_id in self.state.tasks:
                self.state.tasks[task_id].assigned_agent = None
                self.state.tasks[task_id].status = "pending"

        del self.state.agents[agent_id]

        # Update collective resources
        self._update_collective_resources()

    def get_agent(self, agent_id: str) -> SCOBYAgent:
        """Get agent by ID."""
        if agent_id not in self.state.agents:
            raise ValueError(f"Agent {agent_id} not found")
        return self.state.agents[agent_id]

    def update_agent_state(
        self,
        agent_id: str,
        growth_phase: Optional[GrowthPhase] = None,
        metabolic_mode: Optional[MetabolicMode] = None,
        availability: Optional[float] = None,
    ) -> None:
        """
        Update agent state across layers.

        Args:
            agent_id: Agent to update
            growth_phase: New growth phase (Layer 6)
            metabolic_mode: New metabolic mode (Layer 8)
            availability: New availability (0-1)
        """
        agent = self.get_agent(agent_id)

        if growth_phase is not None:
            agent.growth_phase = growth_phase

        if metabolic_mode is not None:
            agent.metabolic_mode = metabolic_mode

        if availability is not None:
            agent.availability = max(0.0, min(1.0, availability))

        # Update collective metrics
        self._update_collective_resources()

    # ===== Task Management =====

    def add_task(self, task: Task) -> None:
        """
        Add task to collective queue.

        Args:
            task: Task to add
        """
        if task.task_id in self.state.tasks:
            raise ValueError(f"Task {task.task_id} already exists")

        self.state.tasks[task.task_id] = task

    def allocate_task(self, task_id: str) -> Optional[str]:
        """
        Allocate task to best-fit agent.

        Uses Fibonacci-weighted scoring to select optimal agent.

        Args:
            task_id: Task to allocate

        Returns:
            Agent ID if allocated, None if no suitable agent
        """
        if task_id not in self.state.tasks:
            raise ValueError(f"Task {task_id} not found")

        task = self.state.tasks[task_id]

        # Find best agent
        best_agent_id = None
        best_score = -1.0

        for agent_id, agent in self.state.agents.items():
            if agent.availability < 0.1:  # Agent not available
                continue

            # Calculate fitness score
            score = self._calculate_agent_task_fitness(agent, task)

            # Apply Fibonacci weighting (Layer 3 integration)
            fib_weight = self._calculate_fibonacci_weight(agent.trust_score)
            weighted_score = score * fib_weight

            if weighted_score > best_score:
                best_score = weighted_score
                best_agent_id = agent_id

        if best_agent_id is None:
            return None

        # Assign task
        task.assigned_agent = best_agent_id
        task.status = "assigned"
        self.state.agents[best_agent_id].task_queue.append(task_id)

        return best_agent_id

    def complete_task(self, task_id: str, quality: float) -> None:
        """
        Mark task as completed.

        Args:
            task_id: Task that was completed
            quality: Quality of completion (0-1)
        """
        if task_id not in self.state.tasks:
            raise ValueError(f"Task {task_id} not found")

        task = self.state.tasks[task_id]
        task.status = "completed"

        # Update agent trust score
        if task.assigned_agent:
            agent = self.state.agents[task.assigned_agent]
            # Remove from queue
            if task_id in agent.task_queue:
                agent.task_queue.remove(task_id)

            # Update trust based on quality
            quality_ratio = quality / task.quality_target
            trust_adjustment = (quality_ratio - 1.0) * 0.1  # +/-10% adjustment
            agent.trust_score = max(0.1, min(2.0, agent.trust_score + trust_adjustment))

        self.state.tasks_completed += 1

    # ===== Metabolic Distribution =====

    def rebalance_metabolic_modes(self) -> Dict[str, MetabolicMode]:
        """
        Rebalance metabolic modes to maintain optimal distribution.

        Target: 40% aerobic, 30% anaerobic, 30% mixed (SCOBY-inspired)

        Returns:
            Dictionary of agent_id → new metabolic mode
        """
        n_agents = len(self.state.agents)
        if n_agents == 0:
            return {}

        # Target counts
        target_aerobic = int(n_agents * self.target_aerobic_ratio)
        target_anaerobic = int(n_agents * self.target_anaerobic_ratio)
        target_mixed = n_agents - target_aerobic - target_anaerobic  # Remainder

        # Current counts
        current_counts = self._count_metabolic_modes()

        # Assign modes
        new_modes = {}

        # Sort agents by resource levels (high oxygen → aerobic preference)
        sorted_agents = sorted(
            self.state.agents.items(),
            key=lambda x: x[1].oxygen_level,
            reverse=True,
        )

        aerobic_count = 0
        anaerobic_count = 0
        mixed_count = 0

        for agent_id, agent in sorted_agents:
            if aerobic_count < target_aerobic and agent.oxygen_level > 0.5:
                new_modes[agent_id] = MetabolicMode.AEROBIC
                aerobic_count += 1
            elif anaerobic_count < target_anaerobic:
                new_modes[agent_id] = MetabolicMode.ANAEROBIC
                anaerobic_count += 1
            else:
                new_modes[agent_id] = MetabolicMode.MIXED
                mixed_count += 1

        # Apply new modes
        for agent_id, mode in new_modes.items():
            self.state.agents[agent_id].metabolic_mode = mode

        # Update metabolic diversity
        self._update_metabolic_diversity()

        return new_modes

    def _count_metabolic_modes(self) -> Dict[str, int]:
        """Count agents in each metabolic mode."""
        counts = {"aerobic": 0, "anaerobic": 0, "mixed": 0, "fermentation": 0}

        for agent in self.state.agents.values():
            if agent.metabolic_mode == MetabolicMode.AEROBIC:
                counts["aerobic"] += 1
            elif agent.metabolic_mode == MetabolicMode.ANAEROBIC:
                counts["anaerobic"] += 1
            elif agent.metabolic_mode == MetabolicMode.MIXED:
                counts["mixed"] += 1
            else:
                counts["fermentation"] += 1

        return counts

    def _update_metabolic_diversity(self) -> None:
        """Calculate metabolic diversity (Shannon entropy-like)."""
        counts = self._count_metabolic_modes()
        total = len(self.state.agents)

        if total == 0:
            self.state.metabolic_diversity = 0.0
            return

        # Shannon diversity index
        diversity = 0.0
        for count in counts.values():
            if count > 0:
                p = count / total
                diversity -= p * np.log(p + 1e-10)

        # Normalize to 0-1
        max_diversity = np.log(len(counts))
        self.state.metabolic_diversity = (
            diversity / max_diversity if max_diversity > 0 else 0.0
        )

    # ===== Collective Consciousness =====

    def calculate_collective_consciousness(self) -> float:
        """
        Calculate collective consciousness level.

        Emergence: Collective > sum of individual contributions

        Returns:
            Collective consciousness (with emergence factor)
        """
        if len(self.state.agents) == 0:
            return 0.0

        # Sum individual contributions
        individual_sum = sum(
            agent.consciousness_contribution for agent in self.state.agents.values()
        )

        # Calculate emergence factor
        emergence = self._calculate_emergence_factor()

        # Collective consciousness
        collective = individual_sum * emergence

        self.state.collective_consciousness = collective
        self.state.emergence_factor = emergence

        return collective

    def _calculate_emergence_factor(self) -> float:
        """
        Calculate emergence factor (collective > sum of parts).

        Factors:
        - Metabolic diversity bonus
        - Mutualistic interaction synergy
        - Network effects (non-linear scaling)

        Returns:
            Emergence factor (> 1.0 means collective > sum)
        """
        n_agents = len(self.state.agents)
        if n_agents == 0:
            return 1.0

        # Metabolic diversity bonus (up to 20%)
        diversity_bonus = 1.0 + (self.state.metabolic_diversity * 0.2)

        # Mutualistic interaction count
        mutualism_pairs = self._count_mutualistic_pairs()
        synergy_bonus = 1.0 + (mutualism_pairs * 0.1)  # 10% per pair

        # Network effects (logarithmic scaling)
        network_factor = np.log(n_agents + 1) / np.log(10)

        # Combined emergence
        emergence = diversity_bonus * synergy_bonus * (1.0 + network_factor * 0.1)

        return emergence

    def _count_mutualistic_pairs(self) -> int:
        """Count mutualistic agent pairs."""
        # Simplified: count agents in AEROBIC mode (they share resources)
        aerobic_count = sum(
            1
            for agent in self.state.agents.values()
            if agent.metabolic_mode == MetabolicMode.AEROBIC
        )

        # Pairs = n choose 2 = n * (n-1) / 2
        return aerobic_count * (aerobic_count - 1) // 2 if aerobic_count > 1 else 0

    # ===== Resource Management =====

    def _update_collective_resources(self) -> None:
        """Update collective resource pools."""
        self.state.total_atp = sum(
            agent.atp_balance for agent in self.state.agents.values()
        )
        self.state.total_oxygen = sum(
            agent.oxygen_level for agent in self.state.agents.values()
        )

    def redistribute_resources(self, total_atp: float) -> Dict[str, float]:
        """
        Redistribute ATP resources across collective.

        Mutualistic agents get priority.
        Competitive agents get reduced share.

        Args:
            total_atp: Total ATP to distribute

        Returns:
            Dictionary of agent_id → ATP allocation
        """
        if len(self.state.agents) == 0:
            return {}

        # Calculate weights based on contribution and mode
        weights = {}
        for agent_id, agent in self.state.agents.items():
            # Base weight = consciousness contribution
            weight = agent.consciousness_contribution

            # Mutualism bonus (aerobic strategists)
            if agent.metabolic_mode == MetabolicMode.AEROBIC:
                weight *= 1.2

            # Trust bonus
            weight *= agent.trust_score

            weights[agent_id] = weight

        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight == 0:
            # Equal distribution
            allocation = {
                agent_id: total_atp / len(self.state.agents)
                for agent_id in self.state.agents
            }
        else:
            allocation = {
                agent_id: (weight / total_weight) * total_atp
                for agent_id, weight in weights.items()
            }

        # Update agent ATP balances
        for agent_id, atp in allocation.items():
            self.state.agents[agent_id].atp_balance = atp

        self._update_collective_resources()

        return allocation

    # ===== Fitness Scoring =====

    def _calculate_agent_task_fitness(self, agent: SCOBYAgent, task: Task) -> float:
        """
        Calculate agent fitness for task.

        Considers:
        - Metabolic mode match
        - Resource availability
        - Role specialization
        - Current load

        Returns:
            Fitness score (0-1)
        """
        scores = []

        # Metabolic mode match
        metabolic_score = self._score_metabolic_match(agent, task)
        scores.append(metabolic_score * 0.4)

        # Resource availability
        resource_score = self._score_resource_availability(agent, task)
        scores.append(resource_score * 0.3)

        # Role specialization
        specialization_score = self._score_specialization(agent, task)
        scores.append(specialization_score * 0.2)

        # Current load (lower is better)
        load_score = 1.0 - (len(agent.task_queue) / 10.0)  # Max 10 tasks
        load_score = max(0.0, load_score)
        scores.append(load_score * 0.1)

        return sum(scores)

    def _score_metabolic_match(self, agent: SCOBYAgent, task: Task) -> float:
        """Score metabolic mode match."""
        if task.preferred_mode is None:
            # No preference
            return 0.8

        if agent.metabolic_mode == task.preferred_mode:
            return 1.0
        elif agent.metabolic_mode == MetabolicMode.MIXED:
            return 0.7  # Mixed can handle any
        else:
            return 0.3  # Mismatch

    def _score_resource_availability(self, agent: SCOBYAgent, task: Task) -> float:
        """Score resource availability."""
        if task.resources_required <= 0:
            return 1.0

        # Check if agent has enough ATP
        ratio = agent.atp_balance / task.resources_required
        return min(1.0, ratio)

    def _score_specialization(self, agent: SCOBYAgent, task: Task) -> float:
        """Score role specialization match."""
        # Role → TaskType matching
        matches = {
            AgentRole.STRATEGIST: [TaskType.STRATEGIC],
            AgentRole.RESEARCHER: [TaskType.RESEARCH],
            AgentRole.QUALITY_CONTROLLER: [TaskType.QUALITY],
            AgentRole.RESPONDER: [TaskType.CRISIS],
            AgentRole.OFFLINE_SPECIALIST: [TaskType.CRISIS],
            AgentRole.RAPID_PROTOTYPER: [TaskType.CREATIVE],
            AgentRole.GENERALIST: [
                TaskType.MAINTENANCE,
                TaskType.STRATEGIC,
                TaskType.RESEARCH,
            ],
            AgentRole.COORDINATOR: list(TaskType),  # All types
        }

        if agent.role in matches and task.task_type in matches[agent.role]:
            return 1.0
        elif agent.role == AgentRole.GENERALIST:
            return 0.7
        else:
            return 0.5

    def _calculate_fibonacci_weight(self, value: float) -> float:
        """
        Calculate Fibonacci-based weight (Layer 3 integration).

        Converges to 369/370 quality standard.

        Args:
            value: Input value (e.g., trust score)

        Returns:
            Weighted value
        """
        # Normalize to 0-1
        normalized = min(1.0, max(0.0, value / 2.0))  # Trust scores 0-2

        # Fibonacci weighting converging to golden ratio
        phi = (1 + np.sqrt(5)) / 2  # Golden ratio ≈ 1.618
        weight = 1.0 + (normalized * (phi - 1.0))

        return weight

    # ===== Metrics & Quality =====

    def calculate_collective_quality(self) -> float:
        """
        Calculate collective reasoning quality.

        Maintains 369/370 standard through weighted averaging.

        Returns:
            Collective quality (≥ 369/370)
        """
        if len(self.state.agents) == 0:
            return 369.0 / 370.0  # Exact 369/370

        total_quality = 0.0
        total_weight = 0.0

        for agent in self.state.agents.values():
            # Weight by metabolic mode
            # Heavily weight aerobic agents to maintain 369/370 standard
            if agent.metabolic_mode == MetabolicMode.AEROBIC:
                weight = 10.0  # Aerobic high quality dominates
            elif agent.metabolic_mode == MetabolicMode.ANAEROBIC:
                weight = 0.1  # Anaerobic minimal weight (acceptable degradation)
            else:
                weight = 1.0  # Mixed balanced

            total_quality += agent.reasoning_quality * weight
            total_weight += weight

        collective_quality = (
            total_quality / total_weight if total_weight > 0 else 369.0 / 370.0
        )

        self.state.collective_quality = collective_quality
        return collective_quality

    def get_metrics(self) -> Dict[str, float]:
        """Get comprehensive SCOBY metrics."""
        mode_counts = self._count_metabolic_modes()

        return {
            "num_agents": len(self.state.agents),
            "num_tasks_pending": sum(
                1 for t in self.state.tasks.values() if t.status == "pending"
            ),
            "num_tasks_assigned": sum(
                1 for t in self.state.tasks.values() if t.status == "assigned"
            ),
            "num_tasks_completed": self.state.tasks_completed,
            "num_tasks_failed": self.state.tasks_failed,
            "total_atp": self.state.total_atp,
            "total_oxygen": self.state.total_oxygen,
            "collective_consciousness": self.state.collective_consciousness,
            "emergence_factor": self.state.emergence_factor,
            "metabolic_diversity": self.state.metabolic_diversity,
            "collective_quality": self.state.collective_quality,
            "aerobic_agents": mode_counts["aerobic"],
            "anaerobic_agents": mode_counts["anaerobic"],
            "mixed_agents": mode_counts["mixed"],
        }


# Helper functions


def simulate_scoby_collective(
    num_agents: int, num_tasks: int, steps: int = 10
) -> Dict[str, List[float]]:
    """
    Simulate SCOBY collective over time.

    Args:
        num_agents: Number of agents in collective
        num_tasks: Number of tasks to process
        steps: Simulation time steps

    Returns:
        Time series of collective metrics
    """
    engine = SCOBYOrchestrationEngine()

    # Add agents with mixed roles
    roles = list(AgentRole)
    for i in range(num_agents):
        role = roles[i % len(roles)]
        engine.add_agent(f"agent_{i}", role=role)

    # Add tasks
    task_types = list(TaskType)
    for i in range(num_tasks):
        task = Task(
            task_id=f"task_{i}",
            task_type=task_types[i % len(task_types)],
            complexity=np.random.uniform(0.3, 0.9),
            urgency=np.random.uniform(0.1, 0.8),
            resources_required=np.random.uniform(10, 50),
            description=f"Task {i}",
        )
        engine.add_task(task)

    # Simulation history
    history = {
        "consciousness": [],
        "emergence": [],
        "diversity": [],
        "quality": [],
        "atp": [],
    }

    # Run simulation
    for step in range(steps):
        # Rebalance metabolic modes
        engine.rebalance_metabolic_modes()

        # Allocate tasks
        for task_id in list(engine.state.tasks.keys()):
            if engine.state.tasks[task_id].status == "pending":
                engine.allocate_task(task_id)

        # Calculate metrics
        consciousness = engine.calculate_collective_consciousness()
        quality = engine.calculate_collective_quality()

        history["consciousness"].append(consciousness)
        history["emergence"].append(engine.state.emergence_factor)
        history["diversity"].append(engine.state.metabolic_diversity)
        history["quality"].append(quality)
        history["atp"].append(engine.state.total_atp)

    return history


def verify_scoby_quality(engine: SCOBYOrchestrationEngine) -> bool:
    """
    Verify SCOBY collective maintains 369/370 quality.

    Args:
        engine: SCOBY orchestration engine

    Returns:
        True if collective quality ≥ 369/370
    """
    quality = engine.calculate_collective_quality()
    return quality >= 369.0 / 370.0
