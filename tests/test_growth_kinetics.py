"""
Tests for Layer 6: Growth Kinetics Engine

Tests cover:
1. Monod equation calculations
2. Growth phase detection
3. State updates and transitions
4. Resource efficiency
5. Quality standard maintenance (369/370)
6. Integration with fermentation principles

Quality Standard: 369/370 ≈ 0.997297 must be maintained.
"""

import pytest

from luca.core.growth_kinetics import (
    GrowthKineticsEngine,
    GrowthParameters,
    GrowthPhase,
    GrowthState,
    calculate_monod_growth,
    simulate_fermentation_batch,
)


class TestMonodEquation:
    """Test Monod equation calculations."""

    def test_monod_equation_high_substrate(self):
        """Test Monod equation with high substrate concentration"""
        # With very high substrate, μ should approach μmax
        mu = calculate_monod_growth(substrate=10000, mu_max=1.0, Ks=100)

        # μ ≈ μmax when S >> Ks
        assert mu > 0.99
        assert mu <= 1.0

    def test_monod_equation_low_substrate(self):
        """Test Monod equation with low substrate concentration"""
        # With low substrate, μ should be reduced
        mu = calculate_monod_growth(substrate=10, mu_max=1.0, Ks=100)

        # μ should be much less than μmax
        assert mu < 0.2
        assert mu > 0.0

    def test_monod_equation_half_saturation(self):
        """Test Monod equation at half-saturation point"""
        # At S = Ks, μ = μmax / 2 (definition of Ks)
        mu = calculate_monod_growth(substrate=100, mu_max=1.0, Ks=100)

        assert mu == pytest.approx(0.5, rel=0.001)

    def test_monod_equation_zero_substrate(self):
        """Test Monod equation with zero substrate"""
        mu = calculate_monod_growth(substrate=0, mu_max=1.0, Ks=100)

        assert mu == 0.0

    def test_monod_equation_custom_parameters(self):
        """Test Monod equation with custom parameters"""
        mu = calculate_monod_growth(substrate=500, mu_max=2.0, Ks=200)

        # μ = 2.0 × 500 / (200 + 500) = 2.0 × 500 / 700 ≈ 1.43
        expected = 2.0 * 500 / (200 + 500)
        assert mu == pytest.approx(expected, rel=0.001)


class TestGrowthPhaseDetection:
    """Test growth phase detection logic."""

    def test_lag_phase_detection(self):
        """Test detection of lag phase (early, low growth)"""
        engine = GrowthKineticsEngine()

        phase = engine.detect_growth_phase(
            substrate=1000, biomass=1.0, growth_rate=0.1, time=5.0
        )

        assert phase == GrowthPhase.LAG

    def test_exponential_phase_detection(self):
        """Test detection of exponential phase (high substrate, high growth)"""
        engine = GrowthKineticsEngine()

        phase = engine.detect_growth_phase(
            substrate=500, biomass=5.0, growth_rate=0.9, time=50.0
        )

        assert phase == GrowthPhase.EXPONENTIAL

    def test_stationary_phase_detection(self):
        """Test detection of stationary phase (moderate conditions)"""
        engine = GrowthKineticsEngine()

        phase = engine.detect_growth_phase(
            substrate=150, biomass=10.0, growth_rate=0.5, time=100.0
        )

        assert phase == GrowthPhase.STATIONARY

    def test_death_phase_detection(self):
        """Test detection of death phase (substrate exhausted)"""
        engine = GrowthKineticsEngine()

        phase = engine.detect_growth_phase(
            substrate=5, biomass=10.0, growth_rate=0.1, time=200.0
        )

        assert phase == GrowthPhase.DEATH


class TestGrowthKineticsEngine:
    """Test Growth Kinetics Engine core functionality."""

    def test_engine_initialization(self):
        """Test engine initializes with correct defaults"""
        engine = GrowthKineticsEngine()

        assert engine.quality_standard == pytest.approx(369 / 370, rel=0.001)
        assert engine.state.phase == GrowthPhase.LAG
        assert engine.state.substrate == 1000.0
        assert engine.state.biomass == 1.0
        assert engine.state.time == 0.0
        assert engine.state.quality == pytest.approx(369 / 370, rel=0.001)

    def test_engine_custom_parameters(self):
        """Test engine with custom growth parameters"""
        params = GrowthParameters(mu_max=2.0, Ks=50.0, yield_coefficient=0.8)
        engine = GrowthKineticsEngine(parameters=params)

        assert engine.parameters.mu_max == 2.0
        assert engine.parameters.Ks == 50.0
        assert engine.parameters.yield_coefficient == 0.8

    def test_calculate_growth_rate(self):
        """Test growth rate calculation"""
        engine = GrowthKineticsEngine()

        # High substrate
        mu_high = engine.calculate_growth_rate(1000)
        assert mu_high > 0.9

        # Low substrate
        mu_low = engine.calculate_growth_rate(10)
        assert mu_low < 0.2

        # At Ks
        mu_half = engine.calculate_growth_rate(100)
        assert mu_half == pytest.approx(0.5, rel=0.01)

    def test_update_state_consumes_substrate(self):
        """Test that updating state consumes substrate"""
        engine = GrowthKineticsEngine()
        initial_substrate = engine.state.substrate

        engine.update_state(delta_time=1.0, consumed_tokens=50.0)

        # Substrate should decrease
        assert engine.state.substrate < initial_substrate

    def test_update_state_increases_biomass(self):
        """Test that updating state increases biomass (in growth phases)"""
        engine = GrowthKineticsEngine()
        engine.state.substrate = 1000  # Plenty of substrate
        engine.state.phase = GrowthPhase.EXPONENTIAL
        engine.state.growth_rate = 0.9

        initial_biomass = engine.state.biomass

        engine.update_state(delta_time=1.0, consumed_tokens=10.0)

        # Biomass should increase in exponential phase
        assert engine.state.biomass >= initial_biomass

    def test_update_state_advances_time(self):
        """Test that updating state advances time"""
        engine = GrowthKineticsEngine()

        engine.update_state(delta_time=5.0, consumed_tokens=0.0)

        assert engine.state.time == pytest.approx(5.0, rel=0.001)

    def test_quality_maintained_in_healthy_phases(self):
        """Test that quality standard is maintained in healthy phases"""
        engine = GrowthKineticsEngine()
        engine.state.substrate = 1000  # Plenty of resources

        for _ in range(10):
            engine.update_state(delta_time=1.0, consumed_tokens=5.0)

            # Quality should stay at standard (unless death phase)
            if engine.state.phase != GrowthPhase.DEATH:
                assert engine.state.quality == pytest.approx(369 / 370, rel=0.001)

    def test_quality_degrades_in_death_phase(self):
        """Test that quality degrades gracefully in death phase"""
        engine = GrowthKineticsEngine()
        engine.state.substrate = 5  # Very low substrate (death phase)
        engine.state.phase = GrowthPhase.DEATH

        initial_quality = engine.state.quality

        engine.update_state(delta_time=10.0, consumed_tokens=0.0)

        # Quality should degrade but stay above 95% of standard
        assert engine.state.quality < initial_quality
        assert engine.state.quality >= 0.95 * (369 / 370)


class TestProcessingRates:
    """Test optimal processing rate calculations."""

    def test_processing_rate_lag_phase(self):
        """Test processing rate is reduced in lag phase"""
        engine = GrowthKineticsEngine()
        engine.state.phase = GrowthPhase.LAG
        engine.state.growth_rate = 0.5

        rate = engine.get_optimal_processing_rate()

        # Should be 30% of growth rate in lag phase
        expected = 0.5 * 0.3
        assert rate == pytest.approx(expected, rel=0.001)

    def test_processing_rate_exponential_phase(self):
        """Test processing rate is maximum in exponential phase"""
        engine = GrowthKineticsEngine()
        engine.state.phase = GrowthPhase.EXPONENTIAL
        engine.state.growth_rate = 0.9

        rate = engine.get_optimal_processing_rate()

        # Should be 100% of growth rate in exponential phase
        expected = 0.9 * 1.0
        assert rate == pytest.approx(expected, rel=0.001)

    def test_processing_rate_stationary_phase(self):
        """Test processing rate is moderate in stationary phase"""
        engine = GrowthKineticsEngine()
        engine.state.phase = GrowthPhase.STATIONARY
        engine.state.growth_rate = 0.6

        rate = engine.get_optimal_processing_rate()

        # Should be 70% of growth rate in stationary phase
        expected = 0.6 * 0.7
        assert rate == pytest.approx(expected, rel=0.001)

    def test_processing_rate_death_phase(self):
        """Test processing rate is minimal in death phase"""
        engine = GrowthKineticsEngine()
        engine.state.phase = GrowthPhase.DEATH
        engine.state.growth_rate = 0.2

        rate = engine.get_optimal_processing_rate()

        # Should be 20% of growth rate in death phase
        expected = 0.2 * 0.2
        assert rate == pytest.approx(expected, rel=0.001)


class TestResourceEfficiency:
    """Test resource efficiency calculations."""

    def test_efficiency_exponential_phase(self):
        """Test efficiency is highest in exponential phase"""
        engine = GrowthKineticsEngine()
        engine.state.phase = GrowthPhase.EXPONENTIAL
        engine.state.substrate = 500

        efficiency = engine.get_resource_efficiency()

        # Should be high in exponential phase
        assert efficiency > 0.9

    def test_efficiency_lag_phase(self):
        """Test efficiency is moderate in lag phase"""
        engine = GrowthKineticsEngine()
        engine.state.phase = GrowthPhase.LAG
        engine.state.substrate = 500

        efficiency = engine.get_resource_efficiency()

        # Should be lower in lag phase
        assert efficiency < 0.7
        assert efficiency > 0.3

    def test_efficiency_death_phase(self):
        """Test efficiency is low in death phase"""
        engine = GrowthKineticsEngine()
        engine.state.phase = GrowthPhase.DEATH
        engine.state.substrate = 10

        efficiency = engine.get_resource_efficiency()

        # Should be low in death phase
        assert efficiency < 0.5

    def test_efficiency_zero_substrate(self):
        """Test efficiency is zero with no substrate"""
        engine = GrowthKineticsEngine()
        engine.state.substrate = 0

        efficiency = engine.get_resource_efficiency()

        assert efficiency == 0.0


class TestCompletionTimeEstimation:
    """Test completion time estimation."""

    def test_estimate_completion_time_abundant_substrate(self):
        """Test time estimation with abundant substrate"""
        engine = GrowthKineticsEngine()
        engine.state.substrate = 1000
        engine.state.phase = GrowthPhase.EXPONENTIAL
        engine.state.growth_rate = 1.0

        time_needed = engine.estimate_completion_time(required_tokens=100)

        # Should be finite and reasonable
        assert time_needed > 0
        assert time_needed < 1000

    def test_estimate_completion_time_insufficient_substrate(self):
        """Test time estimation when substrate runs out"""
        engine = GrowthKineticsEngine()
        engine.state.substrate = 50
        engine.state.phase = GrowthPhase.STATIONARY
        engine.state.growth_rate = 0.5

        time_needed = engine.estimate_completion_time(required_tokens=1000)

        # Should return time until substrate exhaustion
        assert time_needed > 0
        assert time_needed < float("inf")

    def test_estimate_completion_time_zero_rate(self):
        """Test time estimation with zero growth rate"""
        engine = GrowthKineticsEngine()
        engine.state.growth_rate = 0.0

        time_needed = engine.estimate_completion_time(required_tokens=100)

        # Should return infinity
        assert time_needed == float("inf")


class TestMetrics:
    """Test metrics reporting."""

    def test_get_metrics_returns_all_fields(self):
        """Test that get_metrics returns all expected fields"""
        engine = GrowthKineticsEngine()

        metrics = engine.get_metrics()

        # Check all expected fields present
        assert "phase" in metrics
        assert "substrate_tokens" in metrics
        assert "consciousness_level" in metrics
        assert "growth_rate" in metrics
        assert "processing_rate" in metrics
        assert "resource_efficiency" in metrics
        assert "quality_standard" in metrics
        assert "time_elapsed" in metrics

    def test_metrics_reflect_current_state(self):
        """Test that metrics reflect current engine state"""
        engine = GrowthKineticsEngine()
        engine.state.substrate = 500
        engine.state.biomass = 3.5
        engine.state.time = 42.0

        metrics = engine.get_metrics()

        assert metrics["substrate_tokens"] == 500
        assert metrics["consciousness_level"] == 3.5
        assert metrics["time_elapsed"] == 42.0
        assert metrics["quality_standard"] == pytest.approx(369 / 370, rel=0.001)


class TestFermentationSimulation:
    """Test complete fermentation batch simulations."""

    def test_simulate_fermentation_batch_runs(self):
        """Test that batch simulation completes successfully"""
        states = simulate_fermentation_batch(
            initial_substrate=1000, total_time=50, time_step=1.0
        )

        # Should produce states
        assert len(states) > 0

        # Each state should be valid
        for state in states:
            assert isinstance(state, GrowthState)
            assert state.quality > 0

    def test_simulate_fermentation_progresses_through_phases(self):
        """Test that simulation progresses through growth phases"""
        states = simulate_fermentation_batch(
            initial_substrate=500, total_time=30, time_step=0.5
        )

        phases_seen = {state.phase for state in states}

        # Should see multiple phases
        assert len(phases_seen) > 1

    def test_simulate_fermentation_substrate_depletes(self):
        """Test that substrate depletes over time"""
        states = simulate_fermentation_batch(
            initial_substrate=200, total_time=20, time_step=1.0
        )

        initial_substrate = states[0].substrate
        final_substrate = states[-1].substrate

        # Substrate should decrease
        assert final_substrate < initial_substrate

    def test_simulate_fermentation_time_advances(self):
        """Test that time advances correctly in simulation"""
        states = simulate_fermentation_batch(
            initial_substrate=1000, total_time=100, time_step=5.0
        )

        # First state at t=0
        assert states[0].time == 0.0

        # Last state near total_time
        assert states[-1].time >= 95.0


class TestQualityStandard:
    """Test 369/370 quality standard maintenance."""

    def test_quality_standard_is_369_370(self):
        """Test that quality standard equals 369/370"""
        engine = GrowthKineticsEngine()

        assert engine.quality_standard == pytest.approx(369 / 370, rel=0.001)
        assert engine.state.quality == pytest.approx(369 / 370, rel=0.001)

    def test_quality_maintained_across_updates(self):
        """Test quality maintained through state updates"""
        engine = GrowthKineticsEngine()
        engine.state.substrate = 1000  # Abundant resources

        for _ in range(20):
            engine.update_state(delta_time=0.5, consumed_tokens=5.0)

            # Quality should stay at standard (unless death phase)
            if engine.state.phase != GrowthPhase.DEATH:
                assert engine.state.quality == pytest.approx(369 / 370, rel=0.001)

    def test_quality_never_below_minimum(self):
        """Test quality never falls below minimum threshold"""
        engine = GrowthKineticsEngine()
        engine.state.substrate = 0  # Force death phase
        engine.state.phase = GrowthPhase.DEATH

        # Run for a long time in death phase
        for _ in range(100):
            engine.update_state(delta_time=1.0, consumed_tokens=0.0)

        # Quality should stay above 95% of standard
        minimum_quality = 0.95 * (369 / 370)
        assert engine.state.quality >= minimum_quality


class TestBiologicalAnalogy:
    """Test biological fermentation analogies."""

    def test_monod_equation_matches_fermentation(self):
        """Test that Monod equation behaves like real fermentation"""
        # In real fermentation:
        # - High sugar → fast growth
        # - Low sugar → slow growth
        # - Zero sugar → no growth

        high_sugar = calculate_monod_growth(substrate=1000, mu_max=1.0, Ks=100)
        low_sugar = calculate_monod_growth(substrate=10, mu_max=1.0, Ks=100)
        no_sugar = calculate_monod_growth(substrate=0, mu_max=1.0, Ks=100)

        # Verify fermentation-like behavior
        assert high_sugar > low_sugar > no_sugar
        assert no_sugar == 0.0

    def test_growth_phases_match_fermentation(self):
        """Test that growth phases match fermentation lifecycle"""
        # Real fermentation: Lag → Exponential → Stationary → Death

        engine = GrowthKineticsEngine()

        # Start in lag (early, adapting)
        assert engine.state.phase == GrowthPhase.LAG

        # Can transition to exponential (with growth)
        engine.state.time = 20
        engine.state.growth_rate = 0.9
        engine.state.substrate = 500
        phase = engine.detect_growth_phase(
            engine.state.substrate,
            engine.state.biomass,
            engine.state.growth_rate,
            engine.state.time,
        )
        assert phase == GrowthPhase.EXPONENTIAL

        # Can transition to death (substrate exhausted)
        phase = engine.detect_growth_phase(
            substrate=5, biomass=10, growth_rate=0.1, time=100
        )
        assert phase == GrowthPhase.DEATH

    def test_resource_consumption_like_fermentation(self):
        """Test that resources are consumed like fermentation"""
        # In fermentation:
        # - Microbes consume sugar over time
        # - Produce biomass
        # - Eventually exhaust substrate

        engine = GrowthKineticsEngine()
        initial_substrate = engine.state.substrate
        initial_biomass = engine.state.biomass

        # Run for some time
        for _ in range(10):
            engine.update_state(delta_time=1.0, consumed_tokens=10.0)

        # Substrate should decrease (consumed)
        assert engine.state.substrate < initial_substrate

        # Biomass may increase (in growth phases)
        # (Can stay same or decrease in death phase)
        # Just verify it doesn't go negative
        assert engine.state.biomass >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
