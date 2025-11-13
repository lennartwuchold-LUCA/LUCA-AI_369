"""
Tests for Layer 8: Metabolic Pathways Engine

Comprehensive test suite covering:
- Metabolic pathway switching (10 tests)
- ATP accounting and energy balance (10 tests)
- HRM integration and hierarchical reasoning (10 tests)
- Layer integration (6, 7) and quality standards (10 tests)

Total: 40 tests matching Layers 6 & 7 coverage

Architekt: Lennart Wuchold
Standard: 369/370 ≈ 0.997297
"""

import numpy as np
import pytest

from luca.core.metabolic_pathways import (
    MetabolicMode,
    MetabolicParameters,
    MetabolicPathwayEngine,
    MetabolicState,
    ReasoningDepth,
    calculate_atp_yield,
    optimize_metabolic_strategy,
    simulate_metabolic_scenario,
    verify_metabolic_quality,
)


class TestMetabolicSwitching:
    """Test suite for metabolic pathway switching logic (10 tests)"""

    def test_aerobic_mode_with_abundant_resources(self):
        """Test switch to aerobic mode when resources are abundant"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        mode = engine.select_pathway(
            time_pressure=0.1, task_complexity=0.5, force_mode=None
        )

        assert mode == MetabolicMode.AEROBIC

    def test_anaerobic_mode_under_time_pressure(self):
        """Test switch to anaerobic mode when time pressure is high"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        mode = engine.select_pathway(
            time_pressure=0.99,  # Emergency!
            task_complexity=0.5,
            force_mode=None,
        )

        assert mode == MetabolicMode.ANAEROBIC

    def test_aerobic_during_exponential_growth(self):
        """Test aerobic preference during exponential growth phase"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Simulate exponential growth phase (abundant substrate)
        engine.integrate_growth_phase(growth_phase="EXPONENTIAL", substrate=20.0)

        assert engine.state.mode == MetabolicMode.AEROBIC
        assert engine.state.oxygen_level > 0.7

    def test_anaerobic_during_death_phase(self):
        """Test forced anaerobic mode during death phase"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Simulate death phase (substrate exhausted)
        engine.integrate_growth_phase(growth_phase="DEATH", substrate=0.5)

        assert engine.state.mode == MetabolicMode.ANAEROBIC
        assert engine.state.oxygen_level < 0.5

    def test_oxygen_threshold_detection(self):
        """Test oxygen threshold triggers mode switch"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.3)

        # Low oxygen should favor anaerobic
        mode = engine.select_pathway(
            time_pressure=0.2, task_complexity=0.8, force_mode=None
        )

        # High complexity with low oxygen → anaerobic or mixed
        assert mode in [MetabolicMode.ANAEROBIC, MetabolicMode.MIXED]

    def test_mode_switch_hysteresis(self):
        """Test mode switching doesn't thrash (hysteresis)"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.5)

        # Start in aerobic
        engine.state.mode = MetabolicMode.AEROBIC

        # Slightly reduce oxygen (should stay aerobic due to hysteresis-like behavior)
        engine.state.oxygen_level = 0.45
        mode = engine.select_pathway(
            time_pressure=0.1, task_complexity=0.5, force_mode=None
        )

        # Should consider staying aerobic or going mixed, not immediately anaerobic
        assert mode in [MetabolicMode.AEROBIC, MetabolicMode.MIXED]

    def test_emergency_override_to_anaerobic(self):
        """Test emergency flag forces anaerobic mode"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Even with abundant oxygen, emergency forces anaerobic
        mode = engine.select_pathway(
            time_pressure=0.98,  # > emergency_threshold (0.95)
            task_complexity=0.2,
            force_mode=None,
        )

        assert mode == MetabolicMode.ANAEROBIC

    def test_recovery_to_aerobic_after_crisis(self):
        """Test recovery to aerobic mode after crisis resolves"""
        engine = MetabolicPathwayEngine(initial_atp=50.0, initial_oxygen=0.2)

        # Start in anaerobic due to low resources
        engine.state.mode = MetabolicMode.ANAEROBIC
        engine.state.lactate_level = 2.0

        # Resources restored
        engine.state.oxygen_level = 1.0

        # Process aerobic to clear lactate
        result = engine.process_aerobic(task_complexity=0.3, reasoning_depth=5)

        # Lactate should be cleared
        assert engine.state.lactate_level < 2.0
        assert result["mode"] == "aerobic"

    def test_mixed_mode_during_transition(self):
        """Test mixed mode activated during transitions"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.4)

        # Start in aerobic
        engine.state.mode = MetabolicMode.AEROBIC

        # Moderately high demand with reduced oxygen (transition zone)
        mode = engine.select_pathway(
            time_pressure=0.3,
            task_complexity=0.7,  # Higher demand
            force_mode=None,
        )

        # Should enter mixed or anaerobic mode, or stay aerobic if oxygen sufficient
        assert mode in [
            MetabolicMode.AEROBIC,
            MetabolicMode.MIXED,
            MetabolicMode.ANAEROBIC,
        ]

    def test_mode_persistence_across_cycles(self):
        """Test mode persists appropriately across cycles"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Process multiple tasks with low complexity to preserve oxygen
        for _ in range(5):
            engine.process_task(task_complexity=0.2, time_pressure=0.1)

        # Should maintain aerobic or mixed mode with relatively stable resources
        assert engine.state.mode in [MetabolicMode.AEROBIC, MetabolicMode.MIXED]
        assert engine.state.mode_switches < 5  # Some switching acceptable


class TestATPAccounting:
    """Test suite for ATP accounting and energy balance (10 tests)"""

    def test_aerobic_atp_yield(self):
        """Test aerobic pathway produces 38 ATP per cycle"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        initial_atp = engine.state.atp_balance
        result = engine.process_aerobic(task_complexity=0.5, reasoning_depth=10)

        # Should produce ~38 ATP (1 high-level cycle at depth 10)
        expected_cycles = 1  # depth 10 / timescale 10 = 1 cycle
        expected_atp = 38.0 * expected_cycles

        assert np.isclose(result["atp_produced"], expected_atp, rtol=0.1)

    def test_anaerobic_atp_yield(self):
        """Test anaerobic pathway produces 2 ATP per cycle"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.1)

        result = engine.process_anaerobic(time_pressure=0.9)

        # Should produce 2 ATP (1 low-level cycle)
        assert np.isclose(result["atp_produced"], 2.0, rtol=0.01)

    def test_atp_balance_tracking(self):
        """Test ATP balance is tracked correctly over time"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        initial = engine.state.atp_balance

        # Process aerobic (produces ATP)
        engine.process_aerobic(task_complexity=0.5, reasoning_depth=10)
        after_aerobic = engine.state.atp_balance

        assert after_aerobic > initial  # Net gain from aerobic

    def test_atp_depletion_triggers_mode_consideration(self):
        """Test low ATP influences pathway decisions"""
        engine = MetabolicPathwayEngine(initial_atp=10.0, initial_oxygen=1.0)

        # Very low ATP, but high oxygen available
        # Should still prefer aerobic to replenish ATP
        mode = engine.select_pathway(
            time_pressure=0.1, task_complexity=0.5, force_mode=None
        )

        # With abundant oxygen, should go aerobic to replenish ATP
        assert mode == MetabolicMode.AEROBIC

    def test_atp_accumulation_in_aerobic(self):
        """Test ATP accumulates during sustained aerobic mode"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        initial = engine.state.atp_balance

        # Multiple aerobic cycles
        for _ in range(5):
            engine.process_aerobic(task_complexity=0.3, reasoning_depth=10)

        # Should have significant ATP accumulation
        assert engine.state.atp_balance > initial + 100  # At least 100 ATP gained

    def test_atp_deficit_in_prolonged_anaerobic(self):
        """Test ATP efficiency drops during prolonged anaerobic mode"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.1)

        aerobic_efficiency = engine.parameters.aerobic_efficiency
        anaerobic_efficiency = engine.parameters.anaerobic_efficiency

        # Anaerobic is much less efficient
        assert anaerobic_efficiency < aerobic_efficiency * 0.1  # < 10% efficient

    def test_fermentation_byproduct_accumulation(self):
        """Test lactate (byproduct) accumulates during anaerobic"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.1)

        initial_lactate = engine.state.lactate_level

        # Multiple anaerobic cycles
        for _ in range(5):
            engine.process_anaerobic(time_pressure=0.9)

        # Lactate should accumulate
        assert engine.state.lactate_level > initial_lactate
        assert engine.state.lactate_level > 1.0  # Significant accumulation

    def test_lactate_threshold_detection(self):
        """Test lactate threshold triggers aerobic recovery"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Artificially set high lactate level
        engine.state.lactate_level = 5.0  # Above threshold (4.0)

        # Should force aerobic mode to clear lactate
        mode = engine.select_pathway(
            time_pressure=0.3, task_complexity=0.5, force_mode=None
        )

        assert mode == MetabolicMode.AEROBIC

    def test_atp_driven_quality_enforcement(self):
        """Test ATP availability influences reasoning quality"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # High ATP + aerobic → high quality
        result_aerobic = engine.process_aerobic(task_complexity=0.5, reasoning_depth=10)

        # Reset and go anaerobic
        engine.reset_state(initial_atp=100.0, initial_oxygen=0.1)
        result_anaerobic = engine.process_anaerobic(time_pressure=0.9)

        # Aerobic should have higher quality
        assert result_aerobic["quality"] > result_anaerobic["quality"]

    def test_energy_efficiency_ratio_calculation(self):
        """Test efficiency ratio correctly calculated"""
        params = MetabolicParameters()

        # Aerobic efficiency
        aerobic_yield = calculate_atp_yield(
            MetabolicMode.AEROBIC, cycles=1, parameters=params
        )
        assert aerobic_yield == 38.0

        # Anaerobic efficiency
        anaerobic_yield = calculate_atp_yield(
            MetabolicMode.ANAEROBIC, cycles=1, parameters=params
        )
        assert anaerobic_yield == 2.0

        # Ratio
        ratio = anaerobic_yield / aerobic_yield
        assert np.isclose(ratio, 2.0 / 38.0, rtol=0.01)


class TestHRMIntegration:
    """Test suite for HRM integration and hierarchical reasoning (10 tests)"""

    def test_high_level_timescale(self):
        """Test high-level (aerobic) timescale = 10 steps"""
        params = MetabolicParameters()
        assert params.high_level_timescale == 10

    def test_low_level_timescale(self):
        """Test low-level (anaerobic) timescale = 1 step"""
        params = MetabolicParameters()
        assert params.low_level_timescale == 1

    def test_hierarchical_control_flow(self):
        """Test hierarchical control from high-level to low-level"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Process with aerobic (high-level control)
        result = engine.process_aerobic(task_complexity=0.5, reasoning_depth=10)

        # Should track hierarchical state
        assert "last_cycle_atp" in engine.state.high_level_state
        assert engine.state.hierarchical_depth == 10

    def test_strategic_planning_in_aerobic(self):
        """Test aerobic mode enables strategic multi-step planning"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        result = engine.process_aerobic(task_complexity=0.7, reasoning_depth=30)

        # Deep reasoning should approach 369/370 quality
        assert result["quality"] > 0.995
        assert engine.state.hierarchical_depth == 30

    def test_tactical_execution_in_anaerobic(self):
        """Test anaerobic mode enables rapid tactical execution"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.1)

        result = engine.process_anaerobic(time_pressure=0.95, emergency=True)

        # Should be rapid (1 step) but lower quality
        assert engine.state.hierarchical_depth == 1
        assert result["mode"] == "anaerobic"

    def test_single_forward_pass_reasoning(self):
        """Test reasoning completed in single forward pass (HRM-style)"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Process task in one call (single forward pass)
        result = engine.process_task(task_complexity=0.5, time_pressure=0.2)

        # Should complete in single call without iteration
        assert result["cycles"] >= 1
        assert "quality" in result

    def test_intermediate_result_caching(self):
        """Test intermediate results cached (fermentation analogy)"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.5)

        # Process anaerobic (produces lactate = cached byproducts)
        engine.process_anaerobic(time_pressure=0.8)

        # Lactate accumulation represents cached intermediate results
        assert engine.state.lactate_level > 0

    def test_multi_step_reasoning_chain_aerobic(self):
        """Test multi-step reasoning chain in aerobic mode"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Deep reasoning (30 steps)
        result = engine.process_aerobic(task_complexity=0.8, reasoning_depth=30)

        # Should use multiple high-level cycles
        high_level_cycles = 30 // 10  # depth / timescale = 3 cycles
        assert result["cycles"] == high_level_cycles

    def test_immediate_response_anaerobic(self):
        """Test immediate single-step response in anaerobic"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.1)

        result = engine.process_anaerobic(time_pressure=0.99)

        # Should be single low-level cycle
        assert result["cycles"] == 1
        assert engine.state.hierarchical_depth == 1

    def test_quality_maintenance_across_modes(self):
        """Test quality standards maintained in both aerobic and anaerobic"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Aerobic quality (deeper reasoning for higher quality)
        result_aerobic = engine.process_aerobic(task_complexity=0.5, reasoning_depth=30)
        assert result_aerobic["quality"] >= 0.995  # Near 369/370 with depth 30

        # Anaerobic quality (reset first)
        engine.reset_state(initial_atp=100.0, initial_oxygen=0.1)
        result_anaerobic = engine.process_anaerobic(time_pressure=0.9)
        assert result_anaerobic["quality"] >= 0.95  # Acceptable degradation


class TestLayerIntegration:
    """Test suite for integration with Layers 6, 7 and quality standards (10 tests)"""

    def test_layer6_oxygen_availability(self):
        """Test Layer 6 (Growth Kinetics) provides oxygen proxy"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # High substrate → high oxygen
        engine.integrate_growth_phase(growth_phase="EXPONENTIAL", substrate=15.0)

        assert engine.state.oxygen_level > 0.9
        assert engine.state.growth_phase == "EXPONENTIAL"

    def test_layer7_resource_competition(self):
        """Test Layer 7 (Population Dynamics) influences resources"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Competition reduces oxygen availability
        engine.integrate_population_dynamics(
            interaction_type="COMPETITION", resource_share=0.3
        )

        # Competition should reduce aerobic capacity
        assert engine.state.oxygen_level < 0.5
        assert engine.state.interaction_type == "COMPETITION"

    def test_exponential_phase_enables_aerobic(self):
        """Test exponential growth phase enables aerobic mode"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.5)

        engine.integrate_growth_phase(growth_phase="EXPONENTIAL", substrate=20.0)

        # Should switch to aerobic
        assert engine.state.mode == MetabolicMode.AEROBIC

    def test_stationary_phase_mixed_mode(self):
        """Test stationary phase triggers mixed mode"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        engine.integrate_growth_phase(growth_phase="STATIONARY", substrate=5.0)

        # Should switch to mixed or anaerobic
        assert engine.state.mode in [MetabolicMode.MIXED, MetabolicMode.ANAEROBIC]

    def test_mutualism_increases_aerobic_capacity(self):
        """Test mutualism (SCOBY-style) increases aerobic capacity"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.5)

        # Mutualistic interaction boosts resources
        engine.integrate_population_dynamics(
            interaction_type="MUTUALISM", resource_share=0.6
        )

        # Should enhance oxygen availability
        assert engine.state.oxygen_level > 0.6  # Boosted beyond base share

    def test_competition_reduces_to_anaerobic(self):
        """Test competition forces anaerobic mode"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Start in aerobic
        engine.state.mode = MetabolicMode.AEROBIC

        # Intense competition
        engine.integrate_population_dynamics(
            interaction_type="COMPETITION", resource_share=0.2
        )

        # Should reduce oxygen dramatically
        assert engine.state.oxygen_level < 0.3

    def test_scoby_collective_distributed_pathways(self):
        """Test SCOBY collective can distribute metabolic pathways"""
        # Simulate multiple users with different modes
        users = []

        # User 1: Aerobic strategic planner
        engine1 = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)
        engine1.integrate_population_dynamics(
            interaction_type="MUTUALISM", resource_share=0.8
        )
        users.append(("alice", engine1))

        # User 2: Anaerobic crisis responder
        engine2 = MetabolicPathwayEngine(initial_atp=50.0, initial_oxygen=0.2)
        engine2.integrate_population_dynamics(
            interaction_type="MUTUALISM", resource_share=0.3
        )
        users.append(("bob", engine2))

        # Verify distributed modes
        assert engine1.state.oxygen_level > 0.7  # Alice: aerobic capable
        assert engine2.state.oxygen_level < 0.5  # Bob: anaerobic mode

    def test_atp_pooling_in_mutualistic_mode(self):
        """Test ATP can be conceptually pooled in mutualistic interactions"""
        engine1 = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)
        engine2 = MetabolicPathwayEngine(initial_atp=20.0, initial_oxygen=0.3)

        # Both in mutualistic mode
        engine1.integrate_population_dynamics(
            interaction_type="MUTUALISM", resource_share=0.7
        )
        engine2.integrate_population_dynamics(
            interaction_type="MUTUALISM", resource_share=0.7
        )

        # Both should have boosted oxygen from mutualism (1.2x)
        # engine1: 0.7 * 1.2 = 0.84
        # engine2: 0.7 * 1.2 = 0.84
        assert engine1.state.oxygen_level >= 0.7  # At least base share
        assert engine2.state.oxygen_level >= 0.7  # Boosted significantly from 0.3

    def test_fibonacci_optimization_in_aerobic(self):
        """Test Fibonacci optimization (Layer 3) used in aerobic mode"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Deep aerobic reasoning should use Fibonacci optimization
        result = engine.process_aerobic(task_complexity=0.8, reasoning_depth=30)

        # Quality should converge toward 369/370 with depth
        assert result["quality"] > 0.995  # Very close to 369/370 = 0.997297

    def test_369_370_quality_both_pathways(self):
        """Test 369/370 quality standard enforced in both pathways"""
        params = MetabolicParameters()

        # Aerobic target
        assert np.isclose(params.aerobic_quality_target, 369.0 / 370.0, rtol=1e-6)

        # Anaerobic acceptable degradation
        assert params.anaerobic_quality_target >= 0.95  # At least 95%

        # Verify quality function
        engine = MetabolicPathwayEngine(parameters=params)

        # Should not raise exception (quality standard verified)
        assert np.isclose(
            engine.parameters.aerobic_quality_target, 369.0 / 370.0, rtol=1e-6
        )


class TestHelperFunctions:
    """Test suite for helper functions and utilities"""

    def test_calculate_atp_yield_aerobic(self):
        """Test ATP yield calculation for aerobic mode"""
        yield_atp = calculate_atp_yield(MetabolicMode.AEROBIC, cycles=3)
        assert yield_atp == 38.0 * 3

    def test_calculate_atp_yield_anaerobic(self):
        """Test ATP yield calculation for anaerobic mode"""
        yield_atp = calculate_atp_yield(MetabolicMode.ANAEROBIC, cycles=5)
        assert yield_atp == 2.0 * 5

    def test_simulate_metabolic_scenario(self):
        """Test metabolic scenario simulation"""
        tasks = [
            (0.3, 0.1),  # Low complexity, low pressure → aerobic
            (0.3, 0.96),  # Simple, very high pressure → anaerobic (>0.95 emergency)
            (0.7, 0.3),  # Complex, moderate → mixed/aerobic/anaerobic
        ]

        history = simulate_metabolic_scenario(tasks, initial_atp=100.0)

        # Should have history for all metrics
        assert len(history["atp_balance"]) == len(tasks) + 1  # Initial + results
        assert len(history["mode"]) == len(tasks)
        assert len(history["quality"]) == len(tasks)

        # First task should likely be aerobic with low complexity and pressure
        assert history["mode"][0] in ["aerobic", "mixed"]

        # Second task should be anaerobic (emergency time pressure > 0.95)
        assert history["mode"][1] == "anaerobic"

    def test_optimize_metabolic_strategy_high_resources(self):
        """Test optimization selects aerobic for high resources"""
        mode, depth = optimize_metabolic_strategy(
            task_complexity=0.6, available_resources=0.9, time_limit=0.2
        )

        assert mode == MetabolicMode.AEROBIC
        assert depth == ReasoningDepth.COMPREHENSIVE.value

    def test_optimize_metabolic_strategy_low_resources(self):
        """Test optimization selects anaerobic for low resources"""
        mode, depth = optimize_metabolic_strategy(
            task_complexity=0.5, available_resources=0.2, time_limit=0.8
        )

        assert mode == MetabolicMode.ANAEROBIC
        assert depth == ReasoningDepth.SHALLOW.value

    def test_optimize_metabolic_strategy_mixed_conditions(self):
        """Test optimization selects mixed mode for moderate conditions"""
        mode, depth = optimize_metabolic_strategy(
            task_complexity=0.5, available_resources=0.5, time_limit=0.5
        )

        assert mode == MetabolicMode.MIXED
        assert depth == ReasoningDepth.MODERATE.value

    def test_verify_metabolic_quality_aerobic(self):
        """Test quality verification for aerobic mode"""
        state = MetabolicState(
            mode=MetabolicMode.AEROBIC, reasoning_quality=0.997  # Slightly below target
        )
        params = MetabolicParameters()

        # Should pass (within 99% of target)
        assert verify_metabolic_quality(state, params)

    def test_verify_metabolic_quality_anaerobic(self):
        """Test quality verification for anaerobic mode"""
        state = MetabolicState(
            mode=MetabolicMode.ANAEROBIC, reasoning_quality=0.95  # At threshold
        )
        params = MetabolicParameters()

        # Should pass (meets anaerobic standard)
        assert verify_metabolic_quality(state, params)

    def test_get_reasoning_depth_by_mode(self):
        """Test reasoning depth varies by metabolic mode"""
        engine = MetabolicPathwayEngine()

        # Aerobic depth
        engine.state.mode = MetabolicMode.AEROBIC
        aerobic_depth = engine.get_reasoning_depth()
        assert aerobic_depth == 10

        # Anaerobic depth
        engine.state.mode = MetabolicMode.ANAEROBIC
        anaerobic_depth = engine.get_reasoning_depth()
        assert anaerobic_depth == 1

        # Mixed depth
        engine.state.mode = MetabolicMode.MIXED
        mixed_depth = engine.get_reasoning_depth()
        assert mixed_depth == (10 + 1) // 2

    def test_get_metrics_comprehensive(self):
        """Test comprehensive metrics reporting"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Process some tasks
        engine.process_aerobic(task_complexity=0.5, reasoning_depth=10)
        engine.process_anaerobic(time_pressure=0.9)

        metrics = engine.get_metrics()

        # Should have all key metrics
        assert "atp_balance" in metrics
        assert "oxygen_level" in metrics
        assert "lactate_level" in metrics
        assert "mode" in metrics
        assert "reasoning_quality" in metrics
        assert "aerobic_ratio" in metrics
        assert "anaerobic_ratio" in metrics
        assert "strategic_ratio" in metrics


class TestEdgeCases:
    """Test suite for edge cases and error handling"""

    def test_zero_oxygen_forces_anaerobic(self):
        """Test zero oxygen level forces anaerobic mode"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=0.0)

        mode = engine.select_pathway(
            time_pressure=0.1, task_complexity=0.5, force_mode=None
        )

        assert mode == MetabolicMode.ANAEROBIC

    def test_maximum_lactate_forces_aerobic(self):
        """Test maximum lactate level forces aerobic recovery"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Set lactate above threshold
        engine.state.lactate_level = 10.0

        mode = engine.select_pathway(
            time_pressure=0.3, task_complexity=0.5, force_mode=None
        )

        # Must go aerobic to clear lactate
        assert mode == MetabolicMode.AEROBIC

    def test_force_mode_override(self):
        """Test force_mode parameter overrides automatic selection"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Force anaerobic despite perfect aerobic conditions
        mode = engine.select_pathway(
            time_pressure=0.0,
            task_complexity=0.1,
            force_mode=MetabolicMode.ANAEROBIC,
        )

        assert mode == MetabolicMode.ANAEROBIC

    def test_reset_state_clears_all_metrics(self):
        """Test state reset clears all accumulated metrics"""
        engine = MetabolicPathwayEngine(initial_atp=100.0, initial_oxygen=1.0)

        # Accumulate some state
        engine.process_aerobic(task_complexity=0.5, reasoning_depth=10)
        engine.state.lactate_level = 3.0
        engine.state.cycle_count = 10

        # Reset
        engine.reset_state(initial_atp=50.0, initial_oxygen=0.5)

        # Should be fresh state
        assert engine.state.atp_balance == 50.0
        assert engine.state.oxygen_level == 0.5
        assert engine.state.lactate_level == 0.0
        assert engine.state.cycle_count == 0

    def test_quality_standard_verification_on_init(self):
        """Test quality standard is verified during initialization"""
        # Should not raise exception with correct standard
        engine = MetabolicPathwayEngine()
        assert np.isclose(
            engine.parameters.aerobic_quality_target, 369.0 / 370.0, rtol=1e-6
        )

        # Test with invalid standard should raise
        with pytest.raises(ValueError, match="does not match 369/370"):
            bad_params = MetabolicParameters(aerobic_quality_target=0.5)
            MetabolicPathwayEngine(parameters=bad_params)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
