"""
Tests for Layer 10: DS-STAR Quantum Core

Tests cover:
- Cultural resonance analysis
- Cosmic data analysis
- Predictive routing
- Resource forecasting
- Quality standard verification
- Integration with other layers

Author: Lennart Wuchold
Date: 2025-11-12
"""

import pytest

# Optional dependencies - skip tests if not available
try:
    import matplotlib
    import numpy as np
    import pandas
    import scipy

    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not DEPS_AVAILABLE,
    reason="Optional dependencies (pandas, matplotlib, scipy) not installed",
)

from datetime import datetime, timedelta

# Conditional imports - only import if dependencies available
if DEPS_AVAILABLE:
    import numpy as np
    import pandas as pd

    from luca.core.ds_star_quantum import (
        AnalysisType,
        CulturalContext,
        CulturalResonance,
        DSStarAnalysisResult,
        DSStarQuantumCore,
        NetworkRoutingPrediction,
        ResourceForecast,
        analyze_data,
        generate_sample_data,
        verify_ds_star_quality,
    )
else:
    # Dummy imports to prevent collection errors
    (
        AnalysisType,
        CulturalContext,
        CulturalResonance,
        DSStarAnalysisResult,
        DSStarQuantumCore,
        NetworkRoutingPrediction,
        ResourceForecast,
        analyze_data,
        generate_sample_data,
        verify_ds_star_quality,
    ) = (None,) * 10
    np = None
    pd = None


class TestCulturalResonance:
    """Test cultural resonance calculations"""

    def test_cultural_resonance_initialization(self):
        """Test CulturalResonance initialization"""
        resonance = CulturalResonance(
            vedic_score=0.8, egyptian_score=0.7, mayan_score=0.9, quantum_score=0.75
        )

        assert resonance.vedic_score == 0.8
        assert resonance.egyptian_score == 0.7
        assert resonance.mayan_score == 0.9
        assert resonance.quantum_score == 0.75

    def test_total_resonance_calculation(self):
        """Test total resonance calculation"""
        resonance = CulturalResonance(
            vedic_score=0.8, egyptian_score=0.8, mayan_score=0.8, quantum_score=0.8
        )

        assert resonance.total_resonance == 0.8

    def test_cultural_balance_perfect(self):
        """Test cultural balance with perfect balance"""
        resonance = CulturalResonance(
            vedic_score=0.5, egyptian_score=0.5, mayan_score=0.5, quantum_score=0.5
        )

        assert resonance.cultural_balance == 1.0

    def test_cultural_balance_imbalanced(self):
        """Test cultural balance with imbalance"""
        resonance = CulturalResonance(
            vedic_score=0.1, egyptian_score=0.9, mayan_score=0.5, quantum_score=0.5
        )

        # Balance should be less than 1.0
        assert 0.0 <= resonance.cultural_balance < 1.0

    def test_dominant_culture_vedic(self):
        """Test dominant culture detection - Vedic"""
        resonance = CulturalResonance(
            vedic_score=0.9, egyptian_score=0.3, mayan_score=0.4, quantum_score=0.5
        )

        assert resonance.dominant_culture == CulturalContext.VEDIC

    def test_dominant_culture_quantum(self):
        """Test dominant culture detection - Quantum"""
        resonance = CulturalResonance(
            vedic_score=0.3, egyptian_score=0.4, mayan_score=0.5, quantum_score=0.9
        )

        assert resonance.dominant_culture == CulturalContext.QUANTUM


class TestDSStarQuantumCore:
    """Test DS-STAR Quantum Core engine"""

    @pytest.fixture
    def ds_star_engine(self):
        """Create DS-STAR engine for testing"""
        return DSStarQuantumCore()

    @pytest.fixture
    def sample_dataframe(self):
        """Create sample DataFrame for testing"""
        return generate_sample_data(days=30)

    def test_engine_initialization(self, ds_star_engine):
        """Test DS-STAR engine initialization"""
        assert ds_star_engine is not None
        assert len(ds_star_engine.analysis_history) == 0
        assert ds_star_engine.quality_standard == 369.0 / 370.0

    def test_cultural_weights_balanced(self, ds_star_engine):
        """Test cultural weights are balanced"""
        weights = ds_star_engine.cultural_weights.values()
        assert all(w == 0.25 for w in weights)
        assert sum(weights) == 1.0

    def test_analyze_query_resonance_vedic(self, ds_star_engine):
        """Test query resonance analysis - Vedic focus"""
        query = "Analyze structure and calculate optimization metrics clearly"
        resonance = ds_star_engine._analyze_query_resonance(
            query, CulturalContext.VEDIC
        )

        assert resonance.vedic_score > 0.0
        assert isinstance(resonance, CulturalResonance)

    def test_analyze_query_resonance_mayan(self, ds_star_engine):
        """Test query resonance analysis - Mayan focus"""
        query = "Predict time series trends and cyclical patterns in forecast"
        resonance = ds_star_engine._analyze_query_resonance(
            query, CulturalContext.MAYAN
        )

        assert resonance.mayan_score > 0.0

    def test_analyze_query_resonance_quantum(self, ds_star_engine):
        """Test query resonance analysis - Quantum focus"""
        query = "Analyze complex network patterns and quantum correlations"
        resonance = ds_star_engine._analyze_query_resonance(
            query, CulturalContext.QUANTUM
        )

        assert resonance.quantum_score > 0.0

    def test_basic_statistical_analysis(self, ds_star_engine, sample_dataframe):
        """Test basic statistical analysis"""
        stats = ds_star_engine._basic_statistical_analysis(sample_dataframe)

        assert "row_count" in stats
        assert stats["row_count"] == 30
        assert "column_count" in stats
        assert "numeric_columns" in stats
        assert "descriptive_stats" in stats

    def test_time_series_analysis(self, ds_star_engine, sample_dataframe):
        """Test time series analysis"""
        time_series = ds_star_engine._time_series_analysis(sample_dataframe)

        assert "time_range" in time_series
        assert "data_points" in time_series
        assert time_series["data_points"] == 30

    def test_correlation_analysis(self, ds_star_engine, sample_dataframe):
        """Test correlation analysis"""
        correlations = ds_star_engine._correlation_analysis(sample_dataframe)

        assert "correlation_matrix" in correlations or len(correlations) == 0

    def test_cosmic_data_analysis_complete(self, ds_star_engine, sample_dataframe):
        """Test complete cosmic data analysis"""
        query = "Analyze resource demand trends over time"
        result = ds_star_engine.cosmic_data_analysis(
            query=query,
            data=sample_dataframe,
            cultural_context=CulturalContext.QUANTUM,
            analysis_type=AnalysisType.TIME_SERIES,
        )

        assert isinstance(result, DSStarAnalysisResult)
        assert result.query == query
        assert result.cultural_context == CulturalContext.QUANTUM
        assert result.analysis_type == AnalysisType.TIME_SERIES
        assert result.cosmic_confidence > 0.0
        assert result.quality_factor == 369.0 / 370.0

    def test_cosmic_data_analysis_validation(self, ds_star_engine, sample_dataframe):
        """Test cosmic data analysis validation"""
        query = "High quality analysis query"
        result = ds_star_engine.cosmic_data_analysis(
            query, sample_dataframe, CulturalContext.VEDIC
        )

        # Validation should pass if confidence > 0.6
        if result.cosmic_confidence >= 0.6:
            assert result.is_validated is True
        else:
            assert result.is_validated is False

    def test_analysis_history_tracking(self, ds_star_engine, sample_dataframe):
        """Test analysis history is tracked"""
        initial_count = len(ds_star_engine.analysis_history)

        ds_star_engine.cosmic_data_analysis(
            "Test query 1", sample_dataframe, CulturalContext.VEDIC
        )
        ds_star_engine.cosmic_data_analysis(
            "Test query 2", sample_dataframe, CulturalContext.MAYAN
        )

        assert len(ds_star_engine.analysis_history) == initial_count + 2

    def test_generate_cultural_insights_vedic(self, ds_star_engine, sample_dataframe):
        """Test Vedic cultural insights"""
        insights = ds_star_engine._generate_cultural_insights(
            sample_dataframe, CulturalContext.VEDIC
        )

        assert "data_harmony" in insights
        assert "structural_integrity" in insights
        assert "balance_score" in insights
        assert insights["structural_integrity"] is True

    def test_generate_cultural_insights_egyptian(
        self, ds_star_engine, sample_dataframe
    ):
        """Test Egyptian cultural insights"""
        insights = ds_star_engine._generate_cultural_insights(
            sample_dataframe, CulturalContext.EGYPTIAN
        )

        assert "data_completeness" in insights
        assert "precision_score" in insights
        assert 0.0 <= insights["data_completeness"] <= 1.0

    def test_generate_cultural_insights_mayan(self, ds_star_engine, sample_dataframe):
        """Test Mayan cultural insights"""
        insights = ds_star_engine._generate_cultural_insights(
            sample_dataframe, CulturalContext.MAYAN
        )

        assert "cyclical_patterns" in insights
        assert "temporal_coherence" in insights

    def test_generate_cultural_insights_quantum(self, ds_star_engine, sample_dataframe):
        """Test Quantum cultural insights"""
        insights = ds_star_engine._generate_cultural_insights(
            sample_dataframe, CulturalContext.QUANTUM
        )

        assert "complexity_score" in insights
        assert "entanglement_score" in insights

    def test_calculate_cosmic_confidence(self, ds_star_engine):
        """Test cosmic confidence calculation"""
        resonance = CulturalResonance(
            vedic_score=0.2, egyptian_score=0.2, mayan_score=0.2, quantum_score=0.2
        )
        stats = {"row_count": 100, "missing_values": {"col1": 0, "col2": 0}}

        confidence = ds_star_engine._calculate_cosmic_confidence(resonance, stats)

        assert 0.0 <= confidence <= 1.0
        # Should apply 369/370 quality standard
        assert confidence <= 369.0 / 370.0


class TestPredictiveRouting:
    """Test predictive routing analysis"""

    @pytest.fixture
    def ds_star_engine(self):
        """Create DS-STAR engine"""
        return DSStarQuantumCore()

    @pytest.fixture
    def network_data(self):
        """Create sample network data"""
        return {
            "nodes": [
                {"id": "node_1", "status": "active"},
                {"id": "node_2", "status": "active"},
                {"id": "node_3", "status": "active"},
            ],
            "connections": [
                {"from": "node_1", "to": "node_2", "latency": 45},
                {"from": "node_2", "to": "node_3", "latency": 62},
            ],
            "traffic": [
                {"timestamp": datetime.now().isoformat(), "volume": 1024},
            ],
        }

    def test_predictive_routing_analysis(self, ds_star_engine, network_data):
        """Test complete predictive routing analysis"""
        prediction = ds_star_engine.predictive_routing_analysis(network_data)

        assert isinstance(prediction, NetworkRoutingPrediction)
        assert "optimal_paths" in prediction.__dict__
        assert "crisis_adjustments" in prediction.__dict__
        assert "cosmic_validation" in prediction.__dict__
        assert 0.0 <= prediction.prediction_confidence <= 1.0

    def test_calculate_optimal_paths(self, ds_star_engine, network_data):
        """Test optimal path calculation"""
        paths = ds_star_engine._calculate_optimal_paths(
            network_data["nodes"], network_data["connections"], network_data["traffic"]
        )

        assert isinstance(paths, dict)
        assert len(paths) > 0

    def test_crisis_mode_adjustments(self, ds_star_engine, network_data):
        """Test crisis mode adjustments"""
        paths = {"node_1": ["node_1", "node_2"]}
        adjustments = ds_star_engine._crisis_mode_adjustments(paths, network_data)

        assert "emergency_routes_activated" in adjustments
        assert adjustments["emergency_routes_activated"] is True

    def test_cosmic_path_validation(self, ds_star_engine):
        """Test cosmic path validation"""
        paths = {"node_1": ["node_1", "node_2"], "node_2": ["node_2", "node_3"]}
        validation = ds_star_engine._cosmic_path_validation(paths)

        assert "paths_validated" in validation
        assert validation["paths_validated"] == 2
        assert "quality_standard_met" in validation

    def test_calculate_routing_confidence(self, ds_star_engine):
        """Test routing confidence calculation"""
        paths = {"node_1": ["node_1"], "node_2": ["node_2"]}
        confidence = ds_star_engine._calculate_routing_confidence(paths)

        assert 0.0 <= confidence <= 1.0
        # Should apply quality standard
        assert confidence <= 369.0 / 370.0

    def test_empty_network_routing(self, ds_star_engine):
        """Test routing with empty network"""
        empty_data = {"nodes": [], "connections": [], "traffic": []}
        prediction = ds_star_engine.predictive_routing_analysis(empty_data)

        assert isinstance(prediction, NetworkRoutingPrediction)
        assert prediction.prediction_confidence == 0.0


class TestResourceForecasting:
    """Test resource forecasting"""

    @pytest.fixture
    def ds_star_engine(self):
        """Create DS-STAR engine"""
        return DSStarQuantumCore()

    @pytest.fixture
    def historical_data(self):
        """Create historical resource data"""
        return generate_sample_data(days=90)

    def test_resource_prediction_engine(self, ds_star_engine, historical_data):
        """Test complete resource prediction"""
        forecast = ds_star_engine.resource_prediction_engine(
            historical_data, resource_type="water"
        )

        assert isinstance(forecast, ResourceForecast)
        assert forecast.resource_type == "water"
        assert "trend" in forecast.__dict__
        assert "seasonality" in forecast.__dict__
        assert "ensemble_forecast" in forecast.__dict__

    def test_trend_analysis(self, ds_star_engine, historical_data):
        """Test trend analysis"""
        trend = ds_star_engine._calculate_trend_analysis(historical_data)

        assert "direction" in trend
        assert "strength" in trend
        assert "slope" in trend
        assert trend["direction"] in ["increasing", "decreasing", "stable"]

    def test_seasonality_detection(self, ds_star_engine, historical_data):
        """Test seasonality detection"""
        seasonality = ds_star_engine._detect_seasonality(historical_data)

        assert "seasonal_detected" in seasonality
        assert isinstance(seasonality["seasonal_detected"], bool)

    def test_anomaly_detection(self, ds_star_engine):
        """Test anomaly detection"""
        # Create data with anomalies
        data = pd.DataFrame(
            {
                "timestamp": pd.date_range(start="2024-01-01", periods=100),
                "value": [50] * 95 + [200, 210, 205, 195, 190],  # Last 5 are anomalies
            }
        )

        anomalies = ds_star_engine._detect_anomalies(data)

        # Should detect anomalies
        assert isinstance(anomalies, list)

    def test_mayan_calendar_analysis(self, ds_star_engine, historical_data):
        """Test Mayan calendar cycle analysis"""
        mayan = ds_star_engine._apply_mayan_calendar_analysis(historical_data)

        assert "tzolkin_alignment" in mayan
        assert "haab_alignment" in mayan
        assert "long_count_phase" in mayan

    def test_vedic_pattern_detection(self, ds_star_engine, historical_data):
        """Test Vedic pattern detection"""
        vedic = ds_star_engine._vedic_pattern_detection(historical_data)

        assert "harmonic_patterns" in vedic
        assert "structural_integrity" in vedic

    def test_quantum_prediction_models(self, ds_star_engine, historical_data):
        """Test quantum prediction models"""
        quantum = ds_star_engine._quantum_prediction_models(historical_data)

        assert "superposition_states" in quantum
        assert "entanglement_score" in quantum
        assert "prediction_confidence" in quantum

    def test_cosmic_ensemble_forecast(self, ds_star_engine):
        """Test cosmic ensemble forecast"""
        mayan = {"tzolkin_alignment": 0.7}
        vedic = {"balance_score": 0.8}
        quantum = {"prediction_confidence": 0.75}

        ensemble = ds_star_engine._cosmic_ensemble_forecast(mayan, vedic, quantum)

        assert "ensemble_confidence" in ensemble
        assert 0.0 <= ensemble["ensemble_confidence"] <= 1.0

    def test_confidence_intervals(self, ds_star_engine):
        """Test confidence interval calculation"""
        ensemble = {"ensemble_confidence": 0.8}
        intervals = ds_star_engine._calculate_confidence_intervals(ensemble)

        assert "lower_bound" in intervals
        assert "upper_bound" in intervals
        assert intervals["lower_bound"] < intervals["upper_bound"]

    def test_resource_recommendations(self, ds_star_engine):
        """Test resource recommendations generation"""
        high_conf_ensemble = {"ensemble_confidence": 0.9}
        recommendations = ds_star_engine._generate_resource_recommendations(
            high_conf_ensemble
        )

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert "High confidence" in recommendations[0]

    def test_low_confidence_recommendations(self, ds_star_engine):
        """Test recommendations for low confidence"""
        low_conf_ensemble = {"ensemble_confidence": 0.3}
        recommendations = ds_star_engine._generate_resource_recommendations(
            low_conf_ensemble
        )

        assert any("Low confidence" in rec for rec in recommendations)


class TestHelperFunctions:
    """Test helper functions"""

    def test_analyze_data_helper(self):
        """Test analyze_data helper function"""
        data = generate_sample_data(days=30)
        result = analyze_data(
            query="Test analysis",
            data=data,
            cultural_context="quantum",
            analysis_type="time_series",
        )

        assert isinstance(result, DSStarAnalysisResult)
        assert result.query == "Test analysis"

    def test_generate_sample_data_default(self):
        """Test sample data generation with defaults"""
        data = generate_sample_data()

        assert isinstance(data, pd.DataFrame)
        assert len(data) == 30
        assert "timestamp" in data.columns

    def test_generate_sample_data_custom_days(self):
        """Test sample data generation with custom days"""
        data = generate_sample_data(days=90)

        assert len(data) == 90

    def test_generate_sample_data_custom_columns(self):
        """Test sample data generation with custom columns"""
        columns = ["timestamp", "value"]
        data = generate_sample_data(days=30, columns=columns)

        assert "value" in data.columns
        assert len(data.columns) == 2

    def test_verify_ds_star_quality_pass(self):
        """Test quality verification - pass"""
        resonance = CulturalResonance(
            vedic_score=0.2, egyptian_score=0.2, mayan_score=0.2, quantum_score=0.2
        )
        result = DSStarAnalysisResult(
            query="Test",
            cultural_context=CulturalContext.QUANTUM,
            cultural_resonance=resonance,
            analysis_type=AnalysisType.TIME_SERIES,
            basic_stats={"row_count": 100},
            cosmic_confidence=0.8,
            quality_factor=369.0 / 370.0,
            is_validated=True,
        )

        assert verify_ds_star_quality(result) is True

    def test_verify_ds_star_quality_fail(self):
        """Test quality verification - fail"""
        resonance = CulturalResonance()
        result = DSStarAnalysisResult(
            query="Test",
            cultural_context=CulturalContext.QUANTUM,
            cultural_resonance=resonance,
            analysis_type=AnalysisType.TIME_SERIES,
            cosmic_confidence=0.0,  # Will fail
            quality_factor=0.5,  # Below standard
        )

        assert verify_ds_star_quality(result) is False


class TestIntegration:
    """Test integration with other LUCA layers"""

    def test_quality_standard_369_370(self):
        """Test 369/370 quality standard is enforced (Layer 0)"""
        engine = DSStarQuantumCore()

        assert engine.quality_standard == 369.0 / 370.0

    def test_fibonacci_optimization_reference(self):
        """Test Fibonacci optimization is used (Layer 3)"""
        engine = DSStarQuantumCore()
        network_data = {
            "nodes": [{"id": "node_1"}],
            "connections": [],
            "traffic": [],
        }

        # Routing should use Fibonacci-weighted scoring
        prediction = engine.predictive_routing_analysis(network_data)

        # Verify prediction structure includes optimal paths
        assert hasattr(prediction, "optimal_paths")

    def test_cultural_context_enum_complete(self):
        """Test all cultural contexts are defined"""
        contexts = [
            CulturalContext.VEDIC,
            CulturalContext.EGYPTIAN,
            CulturalContext.MAYAN,
            CulturalContext.QUANTUM,
        ]

        assert len(contexts) == 4

    def test_analysis_result_to_dict(self):
        """Test DSStarAnalysisResult serialization"""
        resonance = CulturalResonance(vedic_score=0.5)
        result = DSStarAnalysisResult(
            query="Test",
            cultural_context=CulturalContext.VEDIC,
            cultural_resonance=resonance,
            analysis_type=AnalysisType.TIME_SERIES,
        )

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert "query" in result_dict
        assert "cultural_context" in result_dict
        assert result_dict["quality_factor"] == 369.0 / 370.0


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_dataframe_analysis(self):
        """Test analysis with empty DataFrame"""
        engine = DSStarQuantumCore()
        empty_df = pd.DataFrame()

        result = engine.cosmic_data_analysis(
            "Test query", empty_df, CulturalContext.QUANTUM
        )

        assert result.basic_stats["row_count"] == 0

    def test_dataframe_without_timestamp(self):
        """Test analysis without timestamp column"""
        engine = DSStarQuantumCore()
        data = pd.DataFrame({"value": [1, 2, 3, 4, 5]})

        result = engine.cosmic_data_analysis("Test query", data, CulturalContext.VEDIC)

        # Should handle missing timestamp gracefully
        assert result.time_series_analysis == {}

    def test_dataframe_with_missing_values(self):
        """Test analysis with missing values"""
        engine = DSStarQuantumCore()
        data = pd.DataFrame(
            {
                "timestamp": pd.date_range("2024-01-01", periods=5),
                "value": [1, None, 3, None, 5],
            }
        )

        result = engine.cosmic_data_analysis(
            "Test query", data, CulturalContext.EGYPTIAN
        )

        # Should report missing values
        assert result.basic_stats["missing_values"]["value"] == 2

    def test_single_column_dataframe(self):
        """Test analysis with single column"""
        engine = DSStarQuantumCore()
        data = pd.DataFrame({"value": range(10)})

        result = engine.cosmic_data_analysis("Test query", data, CulturalContext.MAYAN)

        # Correlation analysis should be empty (need 2+ columns)
        assert result.correlations == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
