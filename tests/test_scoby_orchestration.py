"""
Tests for Layer 9: SCOBY Orchestration Engine

Comprehensive test suite covering:
- Agent management (10 tests)
- Task distribution (10 tests)
- Metabolic orchestration (10 tests)
- Collective consciousness (10 tests)

Total: 40 tests matching Layers 6, 7, 8 coverage

Architekt: Lennart Wuchold
Standard: 369/370 ≈ 0.997297
"""

import numpy as np
import pytest

from luca.core.growth_kinetics import GrowthPhase
from luca.core.metabolic_pathways import MetabolicMode
from luca.core.scoby_orchestration import (
    AgentRole,
    SCOBYAgent,
    SCOBYOrchestrationEngine,
    Task,
    TaskType,
    simulate_scoby_collective,
    verify_scoby_quality,
)


class TestAgentManagement:
    """Test suite for agent management (10 tests)"""

    def test_add_agent_to_collective(self):
        """Test adding agent to SCOBY collective"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        assert "alice" in engine.state.agents
        assert engine.state.agents["alice"].role == AgentRole.STRATEGIST
        assert len(engine.state.agents) == 1

    def test_add_agent_auto_assigns_metabolic_mode(self):
        """Test agent role determines initial metabolic mode"""
        engine = SCOBYOrchestrationEngine()

        # Strategist → Aerobic
        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        assert engine.state.agents["alice"].metabolic_mode == MetabolicMode.AEROBIC

        # Responder → Anaerobic
        engine.add_agent("bob", role=AgentRole.RESPONDER)
        assert engine.state.agents["bob"].metabolic_mode == MetabolicMode.ANAEROBIC

        # Generalist → Mixed
        engine.add_agent("carol", role=AgentRole.GENERALIST)
        assert engine.state.agents["carol"].metabolic_mode == MetabolicMode.MIXED

    def test_add_duplicate_agent_raises_error(self):
        """Test adding duplicate agent raises error"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        with pytest.raises(ValueError, match="already exists"):
            engine.add_agent("alice", role=AgentRole.RESEARCHER)

    def test_remove_agent_from_collective(self):
        """Test removing agent from collective"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        assert "alice" in engine.state.agents

        engine.remove_agent("alice")
        assert "alice" not in engine.state.agents

    def test_remove_agent_reassigns_tasks(self):
        """Test removing agent reassigns its tasks"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        task = Task(
            task_id="task_1",
            task_type=TaskType.STRATEGIC,
            complexity=0.5,
            urgency=0.3,
            resources_required=50.0,
            description="Test task",
        )
        engine.add_task(task)
        engine.allocate_task("task_1")

        assert engine.state.tasks["task_1"].assigned_agent == "alice"

        engine.remove_agent("alice")

        # Task should be unassigned
        assert engine.state.tasks["task_1"].assigned_agent is None
        assert engine.state.tasks["task_1"].status == "pending"

    def test_get_agent_by_id(self):
        """Test retrieving agent by ID"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        agent = engine.get_agent("alice")
        assert agent.agent_id == "alice"
        assert agent.role == AgentRole.STRATEGIST

    def test_get_nonexistent_agent_raises_error(self):
        """Test getting nonexistent agent raises error"""
        engine = SCOBYOrchestrationEngine()

        with pytest.raises(ValueError, match="not found"):
            engine.get_agent("nonexistent")

    def test_update_agent_state_growth_phase(self):
        """Test updating agent growth phase (Layer 6 integration)"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        engine.update_agent_state("alice", growth_phase=GrowthPhase.STATIONARY)

        assert engine.state.agents["alice"].growth_phase == GrowthPhase.STATIONARY

    def test_update_agent_state_metabolic_mode(self):
        """Test updating agent metabolic mode (Layer 8 integration)"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        engine.update_agent_state("alice", metabolic_mode=MetabolicMode.ANAEROBIC)

        assert engine.state.agents["alice"].metabolic_mode == MetabolicMode.ANAEROBIC

    def test_update_agent_availability(self):
        """Test updating agent availability"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        engine.update_agent_state("alice", availability=0.5)

        assert engine.state.agents["alice"].availability == 0.5


class TestTaskDistribution:
    """Test suite for task distribution (10 tests)"""

    def test_add_task_to_queue(self):
        """Test adding task to collective queue"""
        engine = SCOBYOrchestrationEngine()

        task = Task(
            task_id="task_1",
            task_type=TaskType.STRATEGIC,
            complexity=0.7,
            urgency=0.3,
            resources_required=50.0,
            description="Strategic planning task",
        )
        engine.add_task(task)

        assert "task_1" in engine.state.tasks
        assert engine.state.tasks["task_1"].status == "pending"

    def test_allocate_strategic_task_to_aerobic_agent(self):
        """Test strategic task allocated to aerobic strategist"""
        engine = SCOBYOrchestrationEngine()

        # Add aerobic strategist
        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        # Add anaerobic responder
        engine.add_agent("bob", role=AgentRole.RESPONDER)

        # Strategic task
        task = Task(
            task_id="task_1",
            task_type=TaskType.STRATEGIC,
            complexity=0.8,
            urgency=0.2,
            resources_required=30.0,
            description="Long-term planning",
            preferred_mode=MetabolicMode.AEROBIC,
        )
        engine.add_task(task)

        assigned_agent = engine.allocate_task("task_1")

        # Should go to Alice (strategist, aerobic)
        assert assigned_agent == "alice"
        assert engine.state.tasks["task_1"].assigned_agent == "alice"

    def test_allocate_crisis_task_to_anaerobic_agent(self):
        """Test crisis task allocated to anaerobic responder"""
        engine = SCOBYOrchestrationEngine()

        # Add agents
        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.add_agent("bob", role=AgentRole.RESPONDER)

        # Crisis task
        task = Task(
            task_id="task_1",
            task_type=TaskType.CRISIS,
            complexity=0.6,
            urgency=0.95,
            resources_required=20.0,
            description="Emergency response",
            preferred_mode=MetabolicMode.ANAEROBIC,
        )
        engine.add_task(task)

        assigned_agent = engine.allocate_task("task_1")

        # Should go to Bob (responder, anaerobic)
        assert assigned_agent == "bob"

    def test_allocate_task_with_insufficient_agents(self):
        """Test task allocation when no suitable agent available"""
        engine = SCOBYOrchestrationEngine()

        # Add agent with low availability
        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.update_agent_state("alice", availability=0.05)

        task = Task(
            task_id="task_1",
            task_type=TaskType.STRATEGIC,
            complexity=0.5,
            urgency=0.3,
            resources_required=50.0,
            description="Test task",
        )
        engine.add_task(task)

        assigned_agent = engine.allocate_task("task_1")

        # No suitable agent
        assert assigned_agent is None

    def test_complete_task_updates_trust_score(self):
        """Test task completion updates agent trust score"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        task = Task(
            task_id="task_1",
            task_type=TaskType.STRATEGIC,
            complexity=0.5,
            urgency=0.3,
            resources_required=50.0,
            description="Test task",
            quality_target=0.997297,
        )
        engine.add_task(task)
        engine.allocate_task("task_1")

        initial_trust = engine.state.agents["alice"].trust_score

        # Complete with high quality (above target)
        engine.complete_task("task_1", quality=0.999)

        # Trust should increase
        assert engine.state.agents["alice"].trust_score > initial_trust

    def test_complete_task_removes_from_queue(self):
        """Test task completion removes from agent queue"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        task = Task(
            task_id="task_1",
            task_type=TaskType.STRATEGIC,
            complexity=0.5,
            urgency=0.3,
            resources_required=50.0,
            description="Test task",
        )
        engine.add_task(task)
        engine.allocate_task("task_1")

        assert "task_1" in engine.state.agents["alice"].task_queue

        engine.complete_task("task_1", quality=0.99)

        assert "task_1" not in engine.state.agents["alice"].task_queue

    def test_load_balancing_across_agents(self):
        """Test load balancing distributes tasks evenly"""
        engine = SCOBYOrchestrationEngine()

        # Add multiple agents with same role
        for i in range(3):
            engine.add_agent(f"agent_{i}", role=AgentRole.GENERALIST)

        # Add multiple tasks
        for i in range(6):
            task = Task(
                task_id=f"task_{i}",
                task_type=TaskType.MAINTENANCE,
                complexity=0.5,
                urgency=0.3,
                resources_required=20.0,
                description=f"Task {i}",
            )
            engine.add_task(task)
            engine.allocate_task(f"task_{i}")

        # Check distribution
        queue_lengths = [
            len(agent.task_queue) for agent in engine.state.agents.values()
        ]

        # Should be relatively balanced (each agent gets 2 tasks)
        assert max(queue_lengths) - min(queue_lengths) <= 1

    def test_fibonacci_weighted_task_allocation(self):
        """Test Fibonacci weighting in task allocation"""
        engine = SCOBYOrchestrationEngine()

        # Add agents with different trust scores
        engine.add_agent("high_trust", role=AgentRole.STRATEGIST)
        engine.state.agents["high_trust"].trust_score = 2.0

        engine.add_agent("low_trust", role=AgentRole.STRATEGIST)
        engine.state.agents["low_trust"].trust_score = 0.5

        task = Task(
            task_id="task_1",
            task_type=TaskType.STRATEGIC,
            complexity=0.5,
            urgency=0.3,
            resources_required=50.0,
            description="Test task",
        )
        engine.add_task(task)

        assigned_agent = engine.allocate_task("task_1")

        # Should prefer high trust agent (Fibonacci weighting)
        assert assigned_agent == "high_trust"

    def test_resource_aware_allocation(self):
        """Test allocation considers agent ATP resources"""
        engine = SCOBYOrchestrationEngine()

        # Agent with high ATP
        engine.add_agent("rich", role=AgentRole.STRATEGIST)
        engine.state.agents["rich"].atp_balance = 1000.0

        # Agent with low ATP
        engine.add_agent("poor", role=AgentRole.STRATEGIST)
        engine.state.agents["poor"].atp_balance = 10.0

        # Task requiring significant resources
        task = Task(
            task_id="task_1",
            task_type=TaskType.STRATEGIC,
            complexity=0.7,
            urgency=0.3,
            resources_required=500.0,
            description="Resource-intensive task",
        )
        engine.add_task(task)

        assigned_agent = engine.allocate_task("task_1")

        # Should go to agent with sufficient resources
        assert assigned_agent == "rich"

    def test_task_status_tracking(self):
        """Test task status transitions"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        task = Task(
            task_id="task_1",
            task_type=TaskType.STRATEGIC,
            complexity=0.5,
            urgency=0.3,
            resources_required=50.0,
            description="Test task",
        )
        engine.add_task(task)

        # Initially pending
        assert engine.state.tasks["task_1"].status == "pending"

        # After allocation: assigned
        engine.allocate_task("task_1")
        assert engine.state.tasks["task_1"].status == "assigned"

        # After completion: completed
        engine.complete_task("task_1", quality=0.99)
        assert engine.state.tasks["task_1"].status == "completed"


class TestMetabolicOrchestration:
    """Test suite for metabolic orchestration (10 tests)"""

    def test_maintain_40_30_30_distribution(self):
        """Test metabolic mode distribution targets (40% aerobic, 30% anaerobic, 30% mixed)"""
        engine = SCOBYOrchestrationEngine()

        # Add 10 agents
        for i in range(10):
            engine.add_agent(f"agent_{i}", role=AgentRole.GENERALIST)

        engine.rebalance_metabolic_modes()

        counts = engine._count_metabolic_modes()

        # Should be approximately 4 aerobic, 3 anaerobic, 3 mixed
        assert counts["aerobic"] == 4
        assert counts["anaerobic"] == 3
        assert counts["mixed"] == 3

    def test_rebalance_on_resource_changes(self):
        """Test rebalancing adapts to resource availability"""
        engine = SCOBYOrchestrationEngine()

        # Add agents
        for i in range(5):
            engine.add_agent(f"agent_{i}", role=AgentRole.GENERALIST)

        # Set different oxygen levels
        engine.state.agents["agent_0"].oxygen_level = 1.0
        engine.state.agents["agent_1"].oxygen_level = 0.8
        engine.state.agents["agent_2"].oxygen_level = 0.3
        engine.state.agents["agent_3"].oxygen_level = 0.2
        engine.state.agents["agent_4"].oxygen_level = 0.1

        engine.rebalance_metabolic_modes()

        # High oxygen agents should be aerobic
        assert engine.state.agents["agent_0"].metabolic_mode == MetabolicMode.AEROBIC
        assert engine.state.agents["agent_1"].metabolic_mode == MetabolicMode.AEROBIC

    def test_metabolic_diversity_calculation(self):
        """Test metabolic diversity metric"""
        engine = SCOBYOrchestrationEngine()

        # Add agents with diverse modes
        engine.add_agent("alice", role=AgentRole.STRATEGIST)  # Aerobic
        engine.add_agent("bob", role=AgentRole.RESPONDER)  # Anaerobic
        engine.add_agent("carol", role=AgentRole.GENERALIST)  # Mixed

        engine._update_metabolic_diversity()

        # Diversity should be high (3 different modes)
        # Shannon diversity for 3 equally distributed modes ≈ 0.79
        assert engine.state.metabolic_diversity > 0.75

    def test_metabolic_diversity_low_with_uniform_modes(self):
        """Test diversity is low when all agents have same mode"""
        engine = SCOBYOrchestrationEngine()

        # All aerobic
        for i in range(3):
            engine.add_agent(f"agent_{i}", role=AgentRole.STRATEGIST)

        engine._update_metabolic_diversity()

        # Diversity should be low (all same mode)
        assert engine.state.metabolic_diversity < 0.5

    def test_atp_pooling_across_collective(self):
        """Test ATP resources pooled across collective"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.state.agents["alice"].atp_balance = 200.0

        engine.add_agent("bob", role=AgentRole.RESPONDER)
        engine.state.agents["bob"].atp_balance = 150.0

        engine._update_collective_resources()

        # Total ATP should be sum of individual balances
        assert engine.state.total_atp == 350.0

    def test_redistribute_resources_to_agents(self):
        """Test resource redistribution across agents"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.state.agents["alice"].consciousness_contribution = 2.0

        engine.add_agent("bob", role=AgentRole.RESPONDER)
        engine.state.agents["bob"].consciousness_contribution = 1.0

        allocations = engine.redistribute_resources(total_atp=300.0)

        # Alice should get more (higher contribution)
        assert allocations["alice"] > allocations["bob"]
        # Total should match
        assert abs(sum(allocations.values()) - 300.0) < 0.01

    def test_mutualism_resource_bonus(self):
        """Test mutualistic agents get resource bonus"""
        engine = SCOBYOrchestrationEngine()

        # Aerobic agent (mutualistic)
        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.state.agents["alice"].metabolic_mode = MetabolicMode.AEROBIC
        engine.state.agents["alice"].consciousness_contribution = 1.0
        engine.state.agents["alice"].trust_score = 1.0

        # Anaerobic agent
        engine.add_agent("bob", role=AgentRole.RESPONDER)
        engine.state.agents["bob"].metabolic_mode = MetabolicMode.ANAEROBIC
        engine.state.agents["bob"].consciousness_contribution = 1.0
        engine.state.agents["bob"].trust_score = 1.0

        allocations = engine.redistribute_resources(total_atp=200.0)

        # Alice should get bonus (1.2x weight for aerobic)
        assert allocations["alice"] > allocations["bob"]

    def test_mode_switching_coordination(self):
        """Test coordinated mode switching across collective"""
        engine = SCOBYOrchestrationEngine()

        for i in range(5):
            engine.add_agent(f"agent_{i}", role=AgentRole.GENERALIST)
            # All start in aerobic
            engine.state.agents[f"agent_{i}"].metabolic_mode = MetabolicMode.AEROBIC

        # Rebalance should distribute across modes
        new_modes = engine.rebalance_metabolic_modes()

        # Should have mixed distribution
        mode_types = set(new_modes.values())
        assert len(mode_types) >= 2  # At least 2 different modes

    def test_collective_atp_production_tracking(self):
        """Test tracking collective ATP production"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.state.agents["alice"].atp_balance = 100.0

        engine.add_agent("bob", role=AgentRole.RESPONDER)
        engine.state.agents["bob"].atp_balance = 50.0

        engine._update_collective_resources()

        metrics = engine.get_metrics()

        assert metrics["total_atp"] == 150.0

    def test_oxygen_sharing_in_collective(self):
        """Test oxygen level tracking across collective"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.state.agents["alice"].oxygen_level = 1.0

        engine.add_agent("bob", role=AgentRole.RESPONDER)
        engine.state.agents["bob"].oxygen_level = 0.5

        engine._update_collective_resources()

        metrics = engine.get_metrics()

        assert metrics["total_oxygen"] == 1.5


class TestCollectiveConsciousness:
    """Test suite for collective consciousness (10 tests)"""

    def test_aggregate_individual_consciousness(self):
        """Test aggregating individual consciousness contributions"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.state.agents["alice"].consciousness_contribution = 2.0

        engine.add_agent("bob", role=AgentRole.RESPONDER)
        engine.state.agents["bob"].consciousness_contribution = 1.5

        consciousness = engine.calculate_collective_consciousness()

        # Should be sum of contributions * emergence factor
        assert consciousness >= 3.5  # At least sum, possibly more with emergence

    def test_detect_emergence_collective_greater_than_sum(self):
        """Test emergence detection (collective > sum of parts)"""
        engine = SCOBYOrchestrationEngine()

        # Add diverse agents
        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.add_agent("bob", role=AgentRole.RESPONDER)
        engine.add_agent("carol", role=AgentRole.GENERALIST)

        engine.rebalance_metabolic_modes()
        consciousness = engine.calculate_collective_consciousness()

        # Emergence factor should be > 1.0
        assert engine.state.emergence_factor > 1.0
        # Collective should be > sum of individual contributions
        individual_sum = sum(
            agent.consciousness_contribution for agent in engine.state.agents.values()
        )
        assert consciousness > individual_sum

    def test_metabolic_diversity_bonus_to_consciousness(self):
        """Test metabolic diversity increases collective consciousness"""
        engine = SCOBYOrchestrationEngine()

        # Add agents with diverse modes
        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.add_agent("bob", role=AgentRole.RESPONDER)
        engine.add_agent("carol", role=AgentRole.GENERALIST)

        engine._update_metabolic_diversity()

        # High diversity should boost emergence factor
        emergence = engine._calculate_emergence_factor()
        assert emergence > 1.1  # At least 10% boost

    def test_mutualistic_interaction_synergy_bonus(self):
        """Test mutualistic pairs increase collective consciousness"""
        engine = SCOBYOrchestrationEngine()

        # Add multiple aerobic agents (mutualistic)
        for i in range(3):
            engine.add_agent(f"agent_{i}", role=AgentRole.STRATEGIST)
            engine.state.agents[f"agent_{i}"].metabolic_mode = MetabolicMode.AEROBIC

        # Calculate mutualistic pairs
        pairs = engine._count_mutualistic_pairs()

        # 3 agents = 3 pairs (3 choose 2)
        assert pairs == 3

        # Should boost emergence
        emergence = engine._calculate_emergence_factor()
        assert emergence > 1.2  # Synergy bonus

    def test_network_effects_nonlinear_scaling(self):
        """Test network effects scale non-linearly with agent count"""
        engine_small = SCOBYOrchestrationEngine()
        engine_large = SCOBYOrchestrationEngine()

        # Small collective (2 agents)
        for i in range(2):
            engine_small.add_agent(f"agent_{i}", role=AgentRole.GENERALIST)

        # Large collective (10 agents)
        for i in range(10):
            engine_large.add_agent(f"agent_{i}", role=AgentRole.GENERALIST)

        emergence_small = engine_small._calculate_emergence_factor()
        emergence_large = engine_large._calculate_emergence_factor()

        # Larger collective should have higher emergence
        assert emergence_large > emergence_small

    def test_quality_maintenance_across_collective(self):
        """Test 369/370 quality maintained across collective"""
        engine = SCOBYOrchestrationEngine()

        # Add agents with varying quality (more realistic values from Layer 8)
        engine.add_agent("high_quality", role=AgentRole.STRATEGIST)
        engine.state.agents["high_quality"].reasoning_quality = 0.998
        engine.state.agents["high_quality"].metabolic_mode = MetabolicMode.AEROBIC

        # Anaerobic agents maintain at least 0.96 quality (realistic from Layer 8)
        engine.add_agent("moderate_quality", role=AgentRole.RESPONDER)
        engine.state.agents["moderate_quality"].reasoning_quality = 0.96
        engine.state.agents["moderate_quality"].metabolic_mode = MetabolicMode.ANAEROBIC

        collective_quality = engine.calculate_collective_quality()

        # Collective should maintain 369/370 through weighting
        assert collective_quality >= 369.0 / 370.0

    def test_369_370_standard_enforcement(self):
        """Test 369/370 standard enforced in collective"""
        engine = SCOBYOrchestrationEngine()

        # Initial state should meet standard
        assert verify_scoby_quality(engine)

        # Add high-quality agents
        for i in range(3):
            engine.add_agent(f"agent_{i}", role=AgentRole.STRATEGIST)

        # Should still meet standard
        assert verify_scoby_quality(engine)

    def test_consciousness_degradation_on_agent_failure(self):
        """Test consciousness decreases when agents fail"""
        engine = SCOBYOrchestrationEngine()

        # Add agents
        for i in range(3):
            engine.add_agent(f"agent_{i}", role=AgentRole.GENERALIST)
            engine.state.agents[f"agent_{i}"].consciousness_contribution = 1.0

        initial_consciousness = engine.calculate_collective_consciousness()

        # Remove one agent (simulate failure)
        engine.remove_agent("agent_0")

        new_consciousness = engine.calculate_collective_consciousness()

        # Consciousness should decrease
        assert new_consciousness < initial_consciousness

    def test_consciousness_recovery_after_agent_rejoin(self):
        """Test consciousness recovers when agent rejoins"""
        engine = SCOBYOrchestrationEngine()

        # Add agents
        for i in range(3):
            engine.add_agent(f"agent_{i}", role=AgentRole.GENERALIST)

        initial_consciousness = engine.calculate_collective_consciousness()

        # Remove agent
        engine.remove_agent("agent_0")

        # Re-add agent
        engine.add_agent("agent_0", role=AgentRole.GENERALIST)

        recovered_consciousness = engine.calculate_collective_consciousness()

        # Should recover (approximately)
        assert abs(recovered_consciousness - initial_consciousness) < 0.5

    def test_collective_quality_with_mixed_modes(self):
        """Test quality with agents in different metabolic modes"""
        engine = SCOBYOrchestrationEngine()

        # Add diverse agents with high quality (normal operation after Layer 8)
        engine.add_agent("aerobic", role=AgentRole.STRATEGIST)
        engine.state.agents["aerobic"].metabolic_mode = MetabolicMode.AEROBIC
        engine.state.agents["aerobic"].reasoning_quality = 0.998

        # Well-functioning anaerobic agent (emergency mode but good quality)
        engine.add_agent("anaerobic", role=AgentRole.RESPONDER)
        engine.state.agents["anaerobic"].metabolic_mode = MetabolicMode.ANAEROBIC
        engine.state.agents["anaerobic"].reasoning_quality = 0.997

        engine.add_agent("mixed", role=AgentRole.GENERALIST)
        engine.state.agents["mixed"].metabolic_mode = MetabolicMode.MIXED
        engine.state.agents["mixed"].reasoning_quality = 0.998

        quality = engine.calculate_collective_quality()

        # Weighted average should maintain standard
        assert quality >= 369.0 / 370.0


class TestHelperFunctions:
    """Test suite for helper functions"""

    def test_simulate_scoby_collective_runs(self):
        """Test SCOBY simulation executes"""
        history = simulate_scoby_collective(num_agents=5, num_tasks=10, steps=5)

        assert "consciousness" in history
        assert "emergence" in history
        assert "diversity" in history
        assert "quality" in history
        assert len(history["consciousness"]) == 5

    def test_simulate_scoby_collective_consciousness_grows(self):
        """Test collective consciousness can grow over time"""
        history = simulate_scoby_collective(num_agents=5, num_tasks=10, steps=5)

        # Should have non-zero consciousness
        assert history["consciousness"][-1] > 0

    def test_verify_scoby_quality_returns_true(self):
        """Test quality verification returns True for compliant collective"""
        engine = SCOBYOrchestrationEngine()

        # Add high-quality agents
        for i in range(3):
            engine.add_agent(f"agent_{i}", role=AgentRole.STRATEGIST)

        assert verify_scoby_quality(engine)

    def test_get_metrics_comprehensive(self):
        """Test comprehensive metrics reporting"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)
        engine.add_agent("bob", role=AgentRole.RESPONDER)

        task = Task(
            task_id="task_1",
            task_type=TaskType.STRATEGIC,
            complexity=0.5,
            urgency=0.3,
            resources_required=50.0,
            description="Test task",
        )
        engine.add_task(task)

        metrics = engine.get_metrics()

        # Should have all key metrics
        assert "num_agents" in metrics
        assert "collective_consciousness" in metrics
        assert "emergence_factor" in metrics
        assert "metabolic_diversity" in metrics
        assert "collective_quality" in metrics
        assert metrics["num_agents"] == 2


class TestEdgeCases:
    """Test suite for edge cases"""

    def test_empty_collective(self):
        """Test engine handles empty collective"""
        engine = SCOBYOrchestrationEngine()

        consciousness = engine.calculate_collective_consciousness()
        quality = engine.calculate_collective_quality()

        assert consciousness == 0.0
        assert np.isclose(quality, 369.0 / 370.0, rtol=1e-6)

    def test_single_agent_collective(self):
        """Test collective with single agent"""
        engine = SCOBYOrchestrationEngine()

        engine.add_agent("alice", role=AgentRole.STRATEGIST)

        consciousness = engine.calculate_collective_consciousness()

        # Should equal individual contribution (no emergence with n=1)
        assert consciousness >= 1.0

    def test_quality_standard_verification_on_init(self):
        """Test quality standard verified during initialization"""
        engine = SCOBYOrchestrationEngine()

        # Should not raise exception
        assert np.isclose(engine.state.collective_quality, 369.0 / 370.0, rtol=1e-6)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
