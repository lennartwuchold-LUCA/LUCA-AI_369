"""
Tests for LUCA Multidimensional Fairness Engine
Tests Russian, Asian, and Oceanic fairness components

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import time

import pytest

from luca.core.fairness_engine import (
    MultidimensionalFairnessEngine,
    NodeMetrics,
    calculate_node_fairness,
    create_node_metrics,
)


class TestNodeMetrics:
    """Tests for NodeMetrics dataclass"""

    def test_node_metrics_creation(self):
        """Test NodeMetrics creation"""
        metrics = NodeMetrics(
            node_id="test_001",
            node_name="Test Node",
            quality_score=0.997,
            uptime_hours=24.0,
            last_validation=time.time(),
        )

        assert metrics.node_id == "test_001"
        assert metrics.node_name == "Test Node"
        assert metrics.quality_score == pytest.approx(0.997, rel=0.001)

    def test_create_node_metrics_helper(self):
        """Test create_node_metrics helper function"""
        metrics = create_node_metrics(
            node_id="test_001",
            node_name="Test Node",
            distance=500.0,
            isolation=0.3,
        )

        assert metrics.node_id == "test_001"
        assert metrics.distance_from_hub == 500.0
        assert metrics.isolation_factor == 0.3


class TestRussianComponent:
    """Tests for Russian Component (Stability & Quality)"""

    def test_russian_component_baseline(self):
        """Test Russian component with baseline metrics"""
        engine = MultidimensionalFairnessEngine()
        metrics = create_node_metrics(
            node_id="test",
            node_name="Test",
            quality=0.997,  # 369/370
            uptime=24.0,
        )

        russian = engine.calculate_russian_component(metrics)

        # Should be close to 369/370 for fresh validated node
        assert 0.95 <= russian <= 1.0

    def test_russian_component_degrades_with_time(self):
        """Test that Russian component degrades over time"""
        engine = MultidimensionalFairnessEngine()

        # Fresh node
        metrics_fresh = create_node_metrics("test1", "Fresh")
        metrics_fresh.last_validation = time.time()

        # Old node (simulated)
        metrics_old = create_node_metrics("test2", "Old")
        metrics_old.last_validation = time.time() - (1000 * 3600)  # 1000 hours ago

        russian_fresh = engine.calculate_russian_component(metrics_fresh)
        russian_old = engine.calculate_russian_component(metrics_old)

        # Fresh should be higher than old
        assert russian_fresh > russian_old

    def test_russian_component_quality_factor(self):
        """Test that quality score affects Russian component"""
        engine = MultidimensionalFairnessEngine()

        metrics_high = create_node_metrics("test1", "High", quality=0.997)
        metrics_low = create_node_metrics("test2", "Low", quality=0.800)

        russian_high = engine.calculate_russian_component(metrics_high)
        russian_low = engine.calculate_russian_component(metrics_low)

        assert russian_high > russian_low


class TestAsianComponent:
    """Tests for Asian Component (Efficiency & Optimization)"""

    def test_asian_component_reach_efficiency(self):
        """Test Asian component rewards efficient reach"""
        engine = MultidimensionalFairnessEngine()

        # High reach, efficient
        metrics_efficient = create_node_metrics(
            "test1", "Efficient", messages=100, reach=50, uptime=10.0
        )

        # Low reach, inefficient
        metrics_inefficient = create_node_metrics(
            "test2", "Inefficient", messages=10, reach=5, uptime=20.0
        )

        asian_efficient = engine.calculate_asian_component(metrics_efficient)
        asian_inefficient = engine.calculate_asian_component(metrics_inefficient)

        # Efficient should score higher
        assert asian_efficient > asian_inefficient

    def test_asian_component_logarithmic_utility(self):
        """Test that Asian component uses logarithmic utility"""
        engine = MultidimensionalFairnessEngine()

        metrics_10 = create_node_metrics("test1", "10 users", reach=10)
        metrics_100 = create_node_metrics("test2", "100 users", reach=100)

        asian_10 = engine.calculate_asian_component(metrics_10)
        asian_100 = engine.calculate_asian_component(metrics_100)

        # 100 users should NOT be 10x better than 10 users
        # (logarithmic utility = diminishing returns)
        ratio = asian_100 / asian_10
        assert ratio < 5.0  # Much less than 10x


class TestOceanicComponent:
    """Tests for Oceanic Component (Solidarity & Decentralization)"""

    def test_oceanic_component_distance_reward(self):
        """Test that Oceanic component rewards distance from hub"""
        engine = MultidimensionalFairnessEngine()

        metrics_center = create_node_metrics("test1", "Center", distance=0.0)
        metrics_remote = create_node_metrics("test2", "Remote", distance=8000.0)

        oceanic_center = engine.calculate_oceanic_component(metrics_center)
        oceanic_remote = engine.calculate_oceanic_component(metrics_remote)

        # Remote should score HIGHER than center
        # This is the anti-imperial architecture!
        assert oceanic_remote > oceanic_center

    def test_oceanic_component_isolation_bonus(self):
        """Test that Oceanic component gives isolation bonus"""
        engine = MultidimensionalFairnessEngine()

        metrics_connected = create_node_metrics(
            "test1",
            "Connected",
            distance=5000.0,
            isolation=0.1,
        )
        metrics_isolated = create_node_metrics(
            "test2",
            "Isolated",
            distance=5000.0,
            isolation=0.9,
        )

        oceanic_connected = engine.calculate_oceanic_component(metrics_connected)
        oceanic_isolated = engine.calculate_oceanic_component(metrics_isolated)

        # More isolated should score higher
        assert oceanic_isolated > oceanic_connected

    def test_oceanic_component_community_contributions(self):
        """Test that Oceanic component rewards community contributions"""
        engine = MultidimensionalFairnessEngine()

        metrics_low_contrib = create_node_metrics(
            "test1",
            "Low Contrib",
            distance=5000.0,
            contributions=1,
        )
        metrics_high_contrib = create_node_metrics(
            "test2",
            "High Contrib",
            distance=5000.0,
            contributions=20,
        )

        oceanic_low = engine.calculate_oceanic_component(metrics_low_contrib)
        oceanic_high = engine.calculate_oceanic_component(metrics_high_contrib)

        assert oceanic_high > oceanic_low


class TestMultidimensionalFairness:
    """Tests for combined multidimensional fairness"""

    def test_calculate_total_fairness(self):
        """Test total fairness calculation"""
        engine = MultidimensionalFairnessEngine()
        metrics = create_node_metrics(
            "test",
            "Test Node",
            quality=0.997,
            uptime=24.0,
            messages=100,
            reach=50,
            distance=5000.0,
            isolation=0.5,
            contributions=10,
        )

        fairness = engine.calculate_total_fairness(metrics)

        assert "node_id" in fairness
        assert "node_name" in fairness
        assert "russian_component" in fairness
        assert "asian_component" in fairness
        assert "oceanic_component" in fairness
        assert "total_fairness" in fairness
        assert "quality_standard" in fairness
        assert "interpretation" in fairness

        assert 0.0 <= fairness["total_fairness"] <= 1.0

    def test_fairness_favors_remote_communities(self):
        """
        Test that fairness calculation favors remote communities

        This is the CORE of the anti-imperial architecture:
        A remote village node with lower "performance" should score
        HIGHER than a central hub with high performance
        """
        engine = MultidimensionalFairnessEngine()

        # Central hub: High performance, low distance
        hub = create_node_metrics(
            "hub",
            "Central Hub",
            distance=0.0,
            isolation=0.0,
            messages=1000,
            reach=500,
            contributions=5,
        )

        # Remote village: Lower performance, high distance
        village = create_node_metrics(
            "village",
            "Remote Village",
            distance=8000.0,
            isolation=0.8,
            messages=50,
            reach=20,
            contributions=15,
        )

        hub_fairness = engine.calculate_total_fairness(hub)
        village_fairness = engine.calculate_total_fairness(village)

        # The village should have higher OCEANIC component despite lower "performance"
        assert village_fairness["oceanic_component"] > hub_fairness["oceanic_component"]

        # This is the revolution: Periphery valued over center!

    def test_fairness_interpretation(self):
        """Test fairness interpretation messages"""
        engine = MultidimensionalFairnessEngine()

        # Excellent node
        metrics_excellent = create_node_metrics(
            "test1",
            "Excellent",
            quality=0.997,
            uptime=100.0,
            messages=500,
            reach=200,
            distance=5000.0,
            isolation=0.7,
            contributions=20,
        )

        fairness = engine.calculate_total_fairness(metrics_excellent)

        assert "interpretation" in fairness
        assert isinstance(fairness["interpretation"], str)

    def test_compare_nodes(self):
        """Test node comparison functionality"""
        engine = MultidimensionalFairnessEngine()

        nodes = [
            create_node_metrics("n1", "Node 1", distance=0.0),
            create_node_metrics("n2", "Node 2", distance=5000.0, isolation=0.5),
            create_node_metrics("n3", "Node 3", distance=8000.0, isolation=0.8),
        ]

        comparison = engine.compare_nodes(nodes)

        # Should return sorted list
        assert len(comparison) == 3

        # Should be sorted by total_fairness (descending)
        assert comparison[0]["total_fairness"] >= comparison[1]["total_fairness"]
        assert comparison[1]["total_fairness"] >= comparison[2]["total_fairness"]

    def test_recommend_optimization(self):
        """Test optimization recommendations"""
        engine = MultidimensionalFairnessEngine()

        # Node with low fairness
        metrics_low = create_node_metrics(
            "test",
            "Low Fairness",
            quality=0.800,
            uptime=1.0,
            messages=5,
            reach=2,
            distance=100.0,
            isolation=0.1,
            contributions=1,
        )

        recommendations = engine.recommend_optimization(metrics_low)

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        # Should have recommendations for improvement
        assert any(
            "stability" in r.lower()
            or "efficiency" in r.lower()
            or "solidarity" in r.lower()
            for r in recommendations
        )


class TestConvenienceFunctions:
    """Test convenience functions"""

    def test_calculate_node_fairness_function(self):
        """Test calculate_node_fairness convenience function"""
        metrics = create_node_metrics("test", "Test Node")

        fairness = calculate_node_fairness(metrics)

        assert "total_fairness" in fairness
        assert 0.0 <= fairness["total_fairness"] <= 1.0


class TestQualityStandard:
    """Verify 369/370 quality standard"""

    def test_quality_standard_369_370(self):
        """Verify 369/370 quality standard"""
        quality = 369 / 370
        assert quality >= 0.997
        assert quality == pytest.approx(0.997297, rel=0.001)

    def test_fairness_engine_quality_baseline(self):
        """Test that fairness engine uses 369/370 baseline"""
        engine = MultidimensionalFairnessEngine()

        assert engine.quality_baseline == pytest.approx(369 / 370, rel=0.001)


class TestPhilosophicalPrinciples:
    """
    Test that the mathematical implementation reflects philosophical principles

    These tests verify that the code embeds the post-capitalist values:
    - Quality over Quantity (Russian)
    - Efficiency without Exploitation (Asian)
    - Periphery over Center (Oceanic)
    """

    def test_periphery_over_center(self):
        """
        Test that peripheral nodes are valued over central nodes

        This is the anti-imperial principle embedded in code
        """
        engine = MultidimensionalFairnessEngine()

        central = create_node_metrics("central", "Central", distance=0.0)
        peripheral = create_node_metrics("peripheral", "Peripheral", distance=9000.0)

        central_oceanic = engine.calculate_oceanic_component(central)
        peripheral_oceanic = engine.calculate_oceanic_component(peripheral)

        # Peripheral MUST score higher
        assert peripheral_oceanic > central_oceanic

    def test_cooperation_over_competition(self):
        """
        Test that community contribution matters more than individual performance

        This is the solidarity principle embedded in code
        """
        engine = MultidimensionalFairnessEngine()

        # High performance, low contribution
        competitive = create_node_metrics(
            "comp",
            "Competitive",
            messages=1000,
            reach=500,
            contributions=1,
            distance=5000.0,
        )

        # Lower performance, high contribution
        cooperative = create_node_metrics(
            "coop",
            "Cooperative",
            messages=100,
            reach=50,
            contributions=20,
            distance=5000.0,
        )

        comp_oceanic = engine.calculate_oceanic_component(competitive)
        coop_oceanic = engine.calculate_oceanic_component(cooperative)

        # Cooperative SHOULD score higher on oceanic component
        assert coop_oceanic > comp_oceanic

    def test_sustainability_over_scale(self):
        """
        Test that logarithmic utility prevents exploitation for scale

        This is the anti-growth principle embedded in code
        """
        engine = MultidimensionalFairnessEngine()

        small = create_node_metrics("small", "Small", reach=10)
        large = create_node_metrics("large", "Large", reach=1000)

        small_asian = engine.calculate_asian_component(small)
        large_asian = engine.calculate_asian_component(large)

        # Large should be better, but NOT 100x better
        # This prevents "scale at all costs" mentality
        ratio = large_asian / small_asian if small_asian > 0 else 0

        # 1000 users is NOT 100x better than 10 users
        assert ratio < 20.0  # Much less than 100x
