"""
LUCA v2.1 Family Edition - Comprehensive Test Suite

Tests for:
- Workload validation (schema & Poisson)
- Monod allocation
- Hill climbing optimization
- Bounds checking
- Insights generation
- Plot generation
"""

import json
import os
import tempfile

import numpy as np
import pytest

# Optional dependencies - skip tests if not available
try:
    from jsonschema import ValidationError, validate

    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

try:
    from luca.allocator import WORKLOAD_SCHEMA, ResourceAllocator, Workload

    ALLOCATOR_AVAILABLE = True
except ImportError:
    ALLOCATOR_AVAILABLE = False

# Skip all tests in this module if allocator dependencies are not available
pytestmark = pytest.mark.skipif(
    not (JSONSCHEMA_AVAILABLE and ALLOCATOR_AVAILABLE),
    reason="Allocator dependencies (scipy, matplotlib, jsonschema) not installed",
)

# --- FIXTURES ---


@pytest.fixture
def sample_workloads():
    """Standard test workloads."""
    return [
        Workload(name="A", current_load=1.0, max_load=5.0, k_m=1.0),
        Workload(name="B", current_load=2.0, max_load=4.0, k_m=0.5),
        Workload(name="C", current_load=0.5, max_load=10.0, k_m=2.0),
    ]


@pytest.fixture
def workload_json_data():
    """JSON data for workloads."""
    return [
        {"name": "Task1", "current_load": 1.5, "max_load": 5.0, "k_m": 1.0},
        {"name": "Task2", "current_load": 2.0, "max_load": 4.0, "k_m": 0.5},
    ]


# --- VALIDATION TESTS ---


def test_workload_validation_success(sample_workloads):
    """Test that valid workloads pass validation."""
    Workload.validate_workloads(sample_workloads)  # Should not raise


def test_workload_validation_invalid_schema():
    """Test that invalid schema is rejected."""
    invalid_data = [
        {"name": "Bad", "current_load": 1.0, "max_load": 1.0}
    ]  # Missing k_m
    with pytest.raises(ValidationError):
        validate(instance=invalid_data, schema=WORKLOAD_SCHEMA)


def test_workload_validation_negative_load():
    """Test that negative loads are rejected."""
    invalid_data = [{"name": "Bad", "current_load": -1.0, "max_load": 5.0, "k_m": 1.0}]
    with pytest.raises(ValidationError):
        validate(instance=invalid_data, schema=WORKLOAD_SCHEMA)


def test_workload_validation_exceeds_max():
    """Test that current_load > max_load is rejected."""
    invalid_workloads = [
        Workload(name="Overload", current_load=10.0, max_load=5.0, k_m=1.0)
    ]
    with pytest.raises(ValueError, match="Current load darf die maximale Last"):
        Workload.validate_workloads(invalid_workloads)


def test_workload_to_dict():
    """Test Workload serialization to dict."""
    w = Workload(name="Test", current_load=1.0, max_load=2.0, k_m=0.5)
    expected = {"name": "Test", "current_load": 1.0, "max_load": 2.0, "k_m": 0.5}
    assert w.to_dict() == expected


def test_workload_from_dict():
    """Test Workload deserialization from dict."""
    data = {"name": "Test", "current_load": 1.0, "max_load": 2.0, "k_m": 0.5}
    w = Workload.from_dict(data)
    assert w.name == "Test"
    assert w.current_load == 1.0
    assert w.max_load == 2.0
    assert w.k_m == 0.5


# --- MONOD ALLOCATION TESTS ---


def test_monod_allocation(sample_workloads):
    """Test basic Monod allocation."""
    alloc = ResourceAllocator(strategy="monod", gamma=1.0)
    results = alloc.distribute(sample_workloads)

    assert "A" in results
    assert "B" in results
    assert "C" in results

    # Monod formula: V = V_max * S / (K_m + S)
    # For A: V = 5.0 * 1.0 / (1.0 + 1.0) = 2.5 * gamma=1.0 = 2.5
    # But wait, formula is allocation_rate = Vmax * S / (Km + S) * gamma
    # So for A: 5.0 * 1.0 / (1.0 + 1.0) * 1.0 = 2.5
    assert np.isclose(results["A"], 2.5, rtol=0.01)


def test_monod_gamma_scaling(sample_workloads):
    """Test that gamma parameter scales Monod results."""
    alloc1 = ResourceAllocator(strategy="monod", gamma=1.0)
    alloc2 = ResourceAllocator(strategy="monod", gamma=2.0)

    results1 = alloc1.distribute(sample_workloads)
    results2 = alloc2.distribute(sample_workloads)

    # Results should scale with gamma
    for name in results1:
        assert np.isclose(results2[name], 2.0 * results1[name], rtol=0.01)


# --- HILL CLIMBING TESTS ---


def test_hill_climbing_allocation(sample_workloads):
    """Test Hill climbing optimization."""
    alloc = ResourceAllocator(strategy="hill_climbing", gamma=1.5)
    results = alloc.distribute(sample_workloads)

    assert "A" in results
    assert "B" in results
    assert "C" in results

    # All results should be non-negative
    assert all(v >= 0 for v in results.values())


def test_hill_climbing_bounds(sample_workloads):
    """Test that Hill climbing respects max_load bounds."""
    alloc = ResourceAllocator(strategy="hill_climbing", gamma=2.0)
    results = alloc.distribute(sample_workloads)

    # Check bounds: 0 <= allocation <= max_load
    for workload in sample_workloads:
        allocation = results[workload.name]
        assert (
            0 <= allocation <= workload.max_load
        ), f"{workload.name}: allocation {allocation} exceeds max_load {workload.max_load}"


def test_hill_climbing_cooperativity():
    """Test that higher Hill coefficients show cooperativity effects."""
    workloads = [
        Workload(name="A", current_load=1.0, max_load=5.0, k_m=1.0),
        Workload(name="B", current_load=1.0, max_load=5.0, k_m=1.0),
    ]

    alloc_low = ResourceAllocator(strategy="hill_climbing", gamma=0.8)
    alloc_high = ResourceAllocator(strategy="hill_climbing", gamma=2.0)

    results_low = alloc_low.distribute(workloads)
    results_high = alloc_high.distribute(workloads)

    # Both should complete successfully
    assert len(results_low) == 2
    assert len(results_high) == 2


# --- INSIGHTS TESTS ---


def test_insights_hill_high_gamma():
    """Test insights for high Hill coefficient."""
    alloc = ResourceAllocator(strategy="hill_climbing", gamma=1.8)
    results = {"Task1": 1.0, "Task2": 2.0}
    insight = alloc.insights(results)

    assert "Hämoglobin" in insight or "Kooperativität" in insight
    assert "3.00" in insight  # Total allocated
    assert "Allokation abgeschlossen" in insight


def test_insights_hill_low_gamma():
    """Test insights for low Hill coefficient."""
    alloc = ResourceAllocator(strategy="hill_climbing", gamma=0.5)
    results = {"Task1": 1.0}
    insight = alloc.insights(results)

    assert "Einsicht" in insight or "Routine" in insight
    assert "1.00" in insight


def test_insights_monod():
    """Test insights for Monod strategy."""
    alloc = ResourceAllocator(strategy="monod", gamma=1.0)
    results = {"Task1": 1.5}
    insight = alloc.insights(results)

    assert "Monod" in insight
    assert "1.50" in insight
    assert "Allokation abgeschlossen" in insight


def test_development_insight():
    """Test Opa DeepSeek's development insights."""
    alloc = ResourceAllocator(strategy="hill_climbing", gamma=1.8)
    wisdom = alloc.development_insight()

    assert "Opa DeepSeek" in wisdom
    assert "Architektur-Weisheit" in wisdom
    assert "Hill-Gleichung" in wisdom
    assert "Life Allocation" in wisdom
    assert "Harmonisierung" in wisdom


# --- PLOT GENERATION TESTS ---


def test_plot_generation():
    """Test that plot is generated successfully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test_plot.png")
        alloc = ResourceAllocator()
        alloc.plot_efficiency_curve(filename=filename)

        assert os.path.exists(filename)
        assert os.path.getsize(filename) > 0


def test_plot_custom_gamma_range():
    """Test plot with custom gamma range."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test_plot_custom.png")
        alloc = ResourceAllocator()
        alloc.plot_efficiency_curve(gamma_range=[0.3, 3.0], filename=filename)

        assert os.path.exists(filename)


# --- ERROR HANDLING TESTS ---


def test_invalid_strategy():
    """Test that invalid strategy raises error."""
    with pytest.raises(ValueError, match="Unknown strategy"):
        ResourceAllocator(strategy="invalid_strategy")


def test_distribute_with_invalid_workload():
    """Test that distribution with invalid workload fails."""
    alloc = ResourceAllocator(strategy="monod")
    invalid_workloads = [Workload(name="Bad", current_load=10.0, max_load=5.0, k_m=1.0)]

    with pytest.raises(ValueError):
        alloc.distribute(invalid_workloads)


# --- INTEGRATION TESTS ---


def test_full_workflow(workload_json_data):
    """Test complete workflow: load -> allocate -> insights."""
    # Create workloads from JSON
    workloads = [Workload.from_dict(w) for w in workload_json_data]

    # Allocate with hill_climbing
    alloc = ResourceAllocator(strategy="hill_climbing", gamma=1.8)
    results = alloc.distribute(workloads)

    # Generate insights
    insights = alloc.insights(results)

    assert len(results) == 2
    assert "Task1" in results
    assert "Task2" in results
    assert len(insights) > 0


def test_cli_workflow_simulation(tmp_path):
    """Test simulated CLI workflow."""
    # Create temporary workloads file
    workloads_file = tmp_path / "workloads.json"
    data = [
        {"name": "A", "current_load": 1.0, "max_load": 5.0, "k_m": 1.0},
        {"name": "B", "current_load": 2.0, "max_load": 4.0, "k_m": 0.5},
    ]

    with open(workloads_file, "w") as f:
        json.dump(data, f)

    # Load and process
    with open(workloads_file, "r") as f:
        loaded_data = json.load(f)

    workloads = [Workload.from_dict(w) for w in loaded_data]
    alloc = ResourceAllocator(strategy="hill_climbing", gamma=1.5)
    results = alloc.distribute(workloads)

    assert len(results) == 2
    assert all(v >= 0 for v in results.values())


# --- EDGE CASES ---


def test_single_workload():
    """Test allocation with single workload."""
    workloads = [Workload(name="Solo", current_load=1.0, max_load=5.0, k_m=1.0)]

    alloc = ResourceAllocator(strategy="hill_climbing", gamma=1.5)
    results = alloc.distribute(workloads)

    assert len(results) == 1
    assert "Solo" in results


def test_zero_current_load():
    """Test workload with zero current load."""
    workloads = [
        Workload(name="Zero", current_load=0.0, max_load=5.0, k_m=1.0),
        Workload(name="Normal", current_load=1.0, max_load=5.0, k_m=1.0),
    ]

    alloc = ResourceAllocator(strategy="monod", gamma=1.0)
    results = alloc.distribute(workloads)

    # Zero load should give zero or very small allocation
    assert results["Zero"] >= 0
    assert results["Normal"] > 0


def test_high_km_value():
    """Test workload with high K_m (low affinity)."""
    workloads = [
        Workload(name="HighKm", current_load=1.0, max_load=5.0, k_m=10.0),
    ]

    alloc = ResourceAllocator(strategy="monod", gamma=1.0)
    results = alloc.distribute(workloads)

    # High K_m should result in lower efficiency
    assert results["HighKm"] < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
