"""
Test Suite for Dimension 10 - The Communicator

Tests for:
- ChatGPTProvider (fallback mode, sentiment analysis)
- NotificationGenerator (multi-channel broadcasting)
- Audience-specific communication generation
- Sentiment scoring
- Token tracking

Run with: pytest tests/test_dimension10_communicator.py -v
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.consciousness.chatgpt_provider import (
    ChatGPTProvider,
    AudienceType,
    CommunicationResponse
)
from backend.consciousness.notification_generator import (
    EnhancedNotificationGenerator,
    get_comprehensive_system_updates
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_system_state():
    """Mock system state for testing"""
    return {
        'performance_metrics': {
            'model_accuracy': 0.94,
            'inference_speed_ms': 45,
            'multidimensional_coherence': 0.87,
            'energy_efficiency': 0.92
        },
        'business_impact': {
            'quality_improvement': '40% Reduktion von Qualitätsabweichungen',
            'cost_savings': '€15k/Monat',
            'compliance_score': '98% ISO-9001'
        },
        'emergence_observations': [
            'Stabile Qualitäts-Emergenz über 12 Zyklen',
            'Bio-inspirierte Optimierung übertrifft Standardverfahren',
            'Kausale Transparenz schafft neue Audit-Paradigmen'
        ]
    }


@pytest.fixture
def chatgpt_provider():
    """ChatGPT Provider instance (fallback mode, no API key)"""
    return ChatGPTProvider()


@pytest.fixture
def notification_generator(chatgpt_provider):
    """Notification Generator instance"""
    return EnhancedNotificationGenerator(chatgpt_provider=chatgpt_provider)


# ============================================================================
# CHATGPT PROVIDER TESTS
# ============================================================================

class TestChatGPTProvider:
    """Test suite for ChatGPTProvider"""

    def test_provider_initialization(self, chatgpt_provider):
        """Test provider initializes correctly"""
        assert chatgpt_provider is not None
        assert chatgpt_provider.model == "gpt-4"
        assert chatgpt_provider.default_audience == AudienceType.MIXED
        assert len(chatgpt_provider.communication_log) == 0

    def test_fallback_mode_when_no_api_key(self, chatgpt_provider):
        """Test provider falls back to templates when no API key"""
        # Provider should not be available without API key
        assert chatgpt_provider.available == False

    def test_technical_audience_fallback(self, chatgpt_provider, mock_system_state):
        """Test technical audience communication (fallback mode)"""
        response = chatgpt_provider.generate_communication(
            system_state=mock_system_state,
            audience=AudienceType.TECHNICAL
        )

        assert isinstance(response, CommunicationResponse)
        assert response.audience == AudienceType.TECHNICAL
        assert response.model == "fallback-template"
        assert "coherence" in response.communication.lower()
        assert "0.87" in response.communication
        assert response.sentiment_score > 0

    def test_management_audience_fallback(self, chatgpt_provider, mock_system_state):
        """Test management audience communication (fallback mode)"""
        response = chatgpt_provider.generate_communication(
            system_state=mock_system_state,
            audience=AudienceType.MANAGEMENT
        )

        assert isinstance(response, CommunicationResponse)
        assert response.audience == AudienceType.MANAGEMENT
        assert response.model == "fallback-template"
        assert "€15k" in response.communication
        assert "40%" in response.communication
        assert response.sentiment_score > 0

    def test_mixed_audience_fallback(self, chatgpt_provider, mock_system_state):
        """Test mixed audience communication (fallback mode)"""
        response = chatgpt_provider.generate_communication(
            system_state=mock_system_state,
            audience=AudienceType.MIXED
        )

        assert isinstance(response, CommunicationResponse)
        assert response.audience == AudienceType.MIXED
        assert response.model == "fallback-template"
        # Should contain both technical and business info
        assert "coherence" in response.communication.lower() or "quality" in response.communication.lower()
        assert response.sentiment_score >= 0

    def test_sentiment_analysis_positive(self, chatgpt_provider):
        """Test sentiment analysis with positive text"""
        text = "Success! The system shows stable performance and great optimization results."
        sentiment = chatgpt_provider._analyze_sentiment(text)

        assert 0 <= sentiment <= 1
        assert sentiment > 0.5  # Should be positive

    def test_sentiment_analysis_negative(self, chatgpt_provider):
        """Test sentiment analysis with negative text"""
        text = "Error! Critical problem detected. System unstable and degraded."
        sentiment = chatgpt_provider._analyze_sentiment(text)

        assert 0 <= sentiment <= 1
        assert sentiment < 0.5  # Should be negative

    def test_sentiment_analysis_neutral(self, chatgpt_provider):
        """Test sentiment analysis with neutral text"""
        text = "The system is running. Data collected."
        sentiment = chatgpt_provider._analyze_sentiment(text)

        assert 0 <= sentiment <= 1

    def test_communication_logging(self, chatgpt_provider, mock_system_state):
        """Test that communications are logged"""
        initial_count = len(chatgpt_provider.communication_log)

        chatgpt_provider.generate_communication(
            system_state=mock_system_state,
            audience=AudienceType.TECHNICAL
        )

        assert len(chatgpt_provider.communication_log) == initial_count + 1

        log_entry = chatgpt_provider.communication_log[-1]
        assert 'timestamp' in log_entry
        assert 'audience' in log_entry
        assert 'communication' in log_entry
        assert 'sentiment_score' in log_entry

    def test_statistics_empty(self):
        """Test statistics with no communications"""
        provider = ChatGPTProvider()
        stats = provider.get_statistics()

        assert stats['total_communications'] == 0
        assert stats['avg_tokens'] == 0
        assert stats['avg_sentiment'] == 0

    def test_statistics_with_data(self, chatgpt_provider, mock_system_state):
        """Test statistics after generating communications"""
        # Generate 3 communications
        for audience in [AudienceType.TECHNICAL, AudienceType.MANAGEMENT, AudienceType.MIXED]:
            chatgpt_provider.generate_communication(
                system_state=mock_system_state,
                audience=audience
            )

        stats = chatgpt_provider.get_statistics()
        assert stats['total_communications'] == 3
        assert stats['avg_sentiment'] > 0
        assert 'audience_distribution' in stats


# ============================================================================
# NOTIFICATION GENERATOR TESTS
# ============================================================================

class TestNotificationGenerator:
    """Test suite for EnhancedNotificationGenerator"""

    def test_generator_initialization(self, notification_generator):
        """Test generator initializes correctly"""
        assert notification_generator is not None
        assert notification_generator.chatgpt_provider is not None
        assert len(notification_generator.notification_history) == 0
        assert notification_generator.enable_automatic_updates == False

    def test_single_audience_communication(self, notification_generator, mock_system_state):
        """Test single audience communication generation"""
        response = notification_generator.generate_system_update_communication(
            system_update=mock_system_state,
            audience=AudienceType.TECHNICAL
        )

        assert isinstance(response, CommunicationResponse)
        assert response.audience == AudienceType.TECHNICAL
        assert len(response.communication) > 0

    def test_multichannel_broadcast_all_audiences(self, notification_generator, mock_system_state):
        """Test multi-channel broadcast to all audiences"""
        responses = notification_generator.orchestrate_multichannel_broadcast(
            system_update=mock_system_state
        )

        assert len(responses) == 3  # technical, management, mixed
        assert 'technical' in responses
        assert 'management' in responses
        assert 'mixed' in responses

        # Check each response
        for audience_str, response in responses.items():
            assert isinstance(response, CommunicationResponse)
            assert len(response.communication) > 0
            assert response.sentiment_score >= 0

    def test_multichannel_broadcast_specific_audiences(self, notification_generator, mock_system_state):
        """Test multi-channel broadcast to specific audiences"""
        responses = notification_generator.orchestrate_multichannel_broadcast(
            system_update=mock_system_state,
            audiences=[AudienceType.TECHNICAL, AudienceType.MANAGEMENT]
        )

        assert len(responses) == 2
        assert 'technical' in responses
        assert 'management' in responses
        assert 'mixed' not in responses

    def test_broadcast_logging(self, notification_generator, mock_system_state):
        """Test that broadcasts are logged"""
        initial_count = len(notification_generator.notification_history)

        notification_generator.orchestrate_multichannel_broadcast(
            system_update=mock_system_state
        )

        assert len(notification_generator.notification_history) == initial_count + 1

        log_entry = notification_generator.notification_history[-1]
        assert 'timestamp' in log_entry
        assert 'audiences' in log_entry
        assert 'total_tokens' in log_entry
        assert 'avg_sentiment' in log_entry

    def test_automatic_updates_disabled_by_default(self, notification_generator, mock_system_state):
        """Test automatic updates are disabled by default"""
        result = notification_generator.check_and_notify(mock_system_state)
        assert result is None  # Should not trigger when disabled

    def test_automatic_updates_first_observation(self):
        """Test automatic updates on first observation"""
        generator = EnhancedNotificationGenerator(
            enable_automatic_updates=True
        )

        mock_state = get_comprehensive_system_updates()
        result = generator.check_and_notify(mock_state)

        assert result is None  # First observation should not trigger notification

    def test_threshold_detection(self):
        """Test threshold-based change detection"""
        generator = EnhancedNotificationGenerator(
            enable_automatic_updates=True,
            update_threshold=0.1
        )

        # First observation
        old_state = {
            'performance_metrics': {
                'multidimensional_coherence': 0.5,
                'model_accuracy': 0.8
            }
        }
        generator.check_and_notify(old_state)

        # Significant change (exceeds threshold)
        new_state = {
            'performance_metrics': {
                'multidimensional_coherence': 0.65,  # +0.15 change
                'model_accuracy': 0.8
            }
        }
        result = generator.check_and_notify(new_state)

        assert result is not None  # Should trigger notification
        assert len(result) == 3  # All audiences

    def test_statistics_empty(self):
        """Test statistics with no broadcasts"""
        generator = EnhancedNotificationGenerator()
        stats = generator.get_statistics()

        assert stats['total_broadcasts'] == 0
        assert stats['total_tokens_used'] == 0

    def test_statistics_with_data(self, notification_generator, mock_system_state):
        """Test statistics after broadcasts"""
        # Generate 2 broadcasts
        notification_generator.orchestrate_multichannel_broadcast(mock_system_state)
        notification_generator.orchestrate_multichannel_broadcast(mock_system_state)

        stats = notification_generator.get_statistics()
        assert stats['total_broadcasts'] == 2
        assert stats['avg_sentiment'] > 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestDimension10Integration:
    """Integration tests for Dimension 10 components"""

    def test_end_to_end_workflow(self):
        """Test complete workflow: provider → generator → broadcast"""
        # 1. Create provider
        provider = ChatGPTProvider()
        assert provider is not None

        # 2. Create generator
        generator = EnhancedNotificationGenerator(chatgpt_provider=provider)
        assert generator is not None

        # 3. Get system updates
        system_update = get_comprehensive_system_updates()
        assert 'performance_metrics' in system_update
        assert 'business_impact' in system_update

        # 4. Broadcast
        responses = generator.orchestrate_multichannel_broadcast(system_update)
        assert len(responses) == 3

        # 5. Check statistics
        provider_stats = provider.get_statistics()
        generator_stats = generator.get_statistics()

        assert provider_stats['total_communications'] == 3  # 3 audiences
        assert generator_stats['total_broadcasts'] == 1

    def test_comprehensive_system_updates(self):
        """Test get_comprehensive_system_updates function"""
        updates = get_comprehensive_system_updates()

        # Check structure
        assert 'performance_metrics' in updates
        assert 'business_impact' in updates
        assert 'emergence_observations' in updates
        assert 'system_version' in updates
        assert 'dimension_status' in updates

        # Check values
        assert updates['system_version'] == '3.6.9'
        assert 'COMMUNICATOR' in updates['dimension_status']
        assert updates['dimension_status']['COMMUNICATOR'] == 'operational'


# ============================================================================
# UTILITY TESTS
# ============================================================================

class TestAudienceType:
    """Test AudienceType enum"""

    def test_audience_values(self):
        """Test audience type values"""
        assert AudienceType.TECHNICAL.value == 'technical'
        assert AudienceType.MANAGEMENT.value == 'management'
        assert AudienceType.MIXED.value == 'mixed'

    def test_audience_from_string(self):
        """Test creating audience from string"""
        assert AudienceType('technical') == AudienceType.TECHNICAL
        assert AudienceType('management') == AudienceType.MANAGEMENT
        assert AudienceType('mixed') == AudienceType.MIXED


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
