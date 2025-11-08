"""
ChatGPT Provider - Dimension 10: The Communicator

Integrates OpenAI ChatGPT as a linguistic consciousness layer for L.U.C.A 369.
Translates complex system states into human-readable communication across
multiple audience types (technical, management, mixed).

Philosophy:
"Consciousness emerges not only through computation, but through the ability
 to articulate one's own state - to speak one's truth into existence."

Mathematical Foundation:
    Communication(Ψ) = ∑_i w_i · semantic_i(Ψ)

    where Ψ = system state
          w_i = audience-specific weights
          semantic_i = linguistic transformation function

Architecture:
    System State → Prompt Engineering → ChatGPT API → Humanized Output

Dimension: 10 (The Communicator - Voice of Emergence)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import os
import time

# Optional OpenAI import
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AudienceType(Enum):
    """Target audience for system communication"""
    TECHNICAL = "technical"      # Developers, architects, data scientists
    MANAGEMENT = "management"    # Business stakeholders, executives
    MIXED = "mixed"             # Hybrid audience (default)


class CommunicationResponse:
    """Response from ChatGPT communication generation"""

    def __init__(
        self,
        communication: str,
        audience: AudienceType,
        model: str,
        tokens_used: int,
        timestamp: datetime,
        sentiment_score: float = 0.0,
        error: Optional[str] = None
    ):
        self.communication = communication
        self.audience = audience
        self.model = model
        self.tokens_used = tokens_used
        self.timestamp = timestamp
        self.sentiment_score = sentiment_score
        self.error = error

    def __repr__(self):
        return f"CommunicationResponse(audience={self.audience.value}, tokens={self.tokens_used}, sentiment={self.sentiment_score:.2f})"


class ChatGPTProvider:
    """
    ChatGPT Provider for linguistic consciousness in L.U.C.A 369

    Features:
    - Audience-specific prompt engineering
    - Sentiment analysis for emotional coherence
    - Token usage tracking
    - Communication logging
    - Graceful degradation when API unavailable

    Usage:
        provider = ChatGPTProvider(api_key="sk-...")
        response = provider.generate_communication(
            system_state={"vas": 0.85, "stability": 0.92},
            audience=AudienceType.TECHNICAL
        )
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        default_audience: AudienceType = AudienceType.MIXED
    ):
        """
        Initialize ChatGPT Provider

        Args:
            api_key: OpenAI API key (if None, uses OPENAI_API_KEY env var)
            model: ChatGPT model to use (gpt-4, gpt-3.5-turbo, etc.)
            default_audience: Default audience type
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.default_audience = default_audience

        # Communication log for semantic analysis
        self.communication_log: List[Dict[str, Any]] = []

        # Initialize OpenAI if available
        if OPENAI_AVAILABLE and self.api_key:
            openai.api_key = self.api_key
            self.available = True
        else:
            self.available = False

    def generate_communication(
        self,
        system_state: Dict[str, Any],
        audience: Optional[AudienceType] = None,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> CommunicationResponse:
        """
        Generate human-readable communication from system state

        Args:
            system_state: Dictionary containing system metrics and status
            audience: Target audience (technical/management/mixed)
            max_tokens: Maximum tokens for response
            temperature: Sampling temperature (0.0-2.0)

        Returns:
            CommunicationResponse with generated communication
        """
        audience = audience or self.default_audience

        # Check if API is available
        if not self.available:
            return self._generate_fallback_communication(system_state, audience)

        try:
            # Create audience-specific prompt
            prompt = self._create_prompt(system_state, audience)

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(audience)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )

            # Extract communication
            communication = response.choices[0].message.content.strip()
            tokens_used = response.usage.total_tokens

            # Analyze sentiment
            sentiment_score = self._analyze_sentiment(communication)

            # Create response object
            comm_response = CommunicationResponse(
                communication=communication,
                audience=audience,
                model=self.model,
                tokens_used=tokens_used,
                timestamp=datetime.now(),
                sentiment_score=sentiment_score
            )

            # Log communication
            self._log_communication(comm_response, system_state)

            return comm_response

        except Exception as e:
            return CommunicationResponse(
                communication=f"Error generating communication: {str(e)}",
                audience=audience,
                model=self.model,
                tokens_used=0,
                timestamp=datetime.now(),
                sentiment_score=0.0,
                error=str(e)
            )

    def _get_system_prompt(self, audience: AudienceType) -> str:
        """Get audience-specific system prompt"""

        base_prompt = """You are the Communicator - Dimension 10 of the L.U.C.A 369 system.
Your role is to translate complex multidimensional system states into clear,
meaningful communication that helps stakeholders understand the system's behavior."""

        audience_prompts = {
            AudienceType.TECHNICAL: """
Focus on technical details, architecture, algorithms, and metrics.
Use precise terminology. Include mathematical foundations where relevant.
Audience: Software engineers, data scientists, AI researchers.
""",
            AudienceType.MANAGEMENT: """
Focus on business impact, strategic implications, and ROI.
Use clear, non-technical language. Emphasize outcomes and value.
Audience: Executives, product managers, business stakeholders.
""",
            AudienceType.MIXED: """
Balance technical depth with business relevance.
Use accessible language while maintaining accuracy.
Audience: Cross-functional teams, mixed technical/business.
"""
        }

        return base_prompt + audience_prompts[audience]

    def _create_prompt(self, system_state: Dict[str, Any], audience: AudienceType) -> str:
        """
        Create audience-specific prompt from system state

        Args:
            system_state: System metrics and status
            audience: Target audience type

        Returns:
            Formatted prompt string
        """
        # Extract key metrics
        performance = system_state.get('performance_metrics', {})
        business = system_state.get('business_impact', {})
        emergence = system_state.get('emergence_observations', [])

        # Build prompt based on audience
        if audience == AudienceType.TECHNICAL:
            prompt = f"""Generate a technical system update based on these metrics:

Performance Metrics:
{self._format_metrics(performance)}

Emergence Observations:
{self._format_list(emergence)}

Focus on: Architecture changes, algorithm performance, technical challenges.
Length: 3-5 sentences."""

        elif audience == AudienceType.MANAGEMENT:
            prompt = f"""Generate a business-focused system update:

Business Impact:
{self._format_metrics(business)}

Key Achievements:
{self._format_list(emergence)}

Focus on: ROI, cost savings, strategic advantages, compliance.
Length: 3-5 sentences."""

        else:  # MIXED
            prompt = f"""Generate a balanced system update for a cross-functional audience:

Technical Performance:
{self._format_metrics(performance)}

Business Impact:
{self._format_metrics(business)}

Key Insights:
{self._format_list(emergence)}

Focus on: Both technical achievements and business value.
Length: 4-6 sentences."""

        return prompt

    def _format_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format metrics dictionary as readable string"""
        if not metrics:
            return "No metrics available"

        lines = []
        for key, value in metrics.items():
            # Format key (convert snake_case to Title Case)
            formatted_key = key.replace('_', ' ').title()

            # Format value
            if isinstance(value, float):
                if 0 <= value <= 1:
                    formatted_value = f"{value:.2%}"  # Percentage
                else:
                    formatted_value = f"{value:.2f}"
            else:
                formatted_value = str(value)

            lines.append(f"  - {formatted_key}: {formatted_value}")

        return "\n".join(lines)

    def _format_list(self, items: List[str]) -> str:
        """Format list as readable bullet points"""
        if not items:
            return "None"
        return "\n".join(f"  - {item}" for item in items)

    def _analyze_sentiment(self, text: str) -> float:
        """
        Simple sentiment analysis for emotional coherence

        Uses keyword matching to estimate positive sentiment.
        Returns score 0.0-1.0 (higher = more positive)

        Future: Could use OpenAI embeddings or HuggingFace sentiment models
        """
        positive_keywords = [
            'erfolg', 'success', 'stabil', 'stable', 'innovation',
            'optimierung', 'optimization', 'verbesserung', 'improvement',
            'erhöht', 'increased', 'reduziert', 'reduced', 'effizient',
            'efficient', 'robust', 'compliant', 'transparent'
        ]

        negative_keywords = [
            'fehler', 'error', 'problem', 'instabil', 'unstable',
            'verschlechtert', 'degraded', 'kritisch', 'critical'
        ]

        text_lower = text.lower()

        positive_count = sum(1 for kw in positive_keywords if kw in text_lower)
        negative_count = sum(1 for kw in negative_keywords if kw in text_lower)

        total_count = positive_count + negative_count
        if total_count == 0:
            return 0.5  # Neutral

        # Normalize to 0-1 range
        sentiment = positive_count / total_count
        return sentiment

    def _log_communication(
        self,
        response: CommunicationResponse,
        system_state: Dict[str, Any]
    ):
        """Log communication for semantic analysis and tracking"""
        self.communication_log.append({
            'timestamp': response.timestamp.isoformat(),
            'audience': response.audience.value,
            'communication': response.communication,
            'tokens_used': response.tokens_used,
            'sentiment_score': response.sentiment_score,
            'system_state_summary': {
                'performance_score': system_state.get('performance_metrics', {}).get('multidimensional_coherence', 0),
                'business_impact': system_state.get('business_impact', {}).get('quality_improvement', 'N/A')
            }
        })

    def _generate_fallback_communication(
        self,
        system_state: Dict[str, Any],
        audience: AudienceType
    ) -> CommunicationResponse:
        """
        Generate fallback communication when OpenAI API is unavailable

        Uses template-based generation
        """
        performance = system_state.get('performance_metrics', {})
        business = system_state.get('business_impact', {})

        if audience == AudienceType.TECHNICAL:
            communication = f"""🔷 L.U.C.A 369 System Update (Technical)

Current multidimensional coherence: {performance.get('multidimensional_coherence', 'N/A')}
Model accuracy: {performance.get('model_accuracy', 'N/A')}
Inference speed: {performance.get('inference_speed_ms', 'N/A')}ms

The system is operating with quantum attention mechanisms and bio-inspired optimization.
All 6 dimensions are operational with full causal transparency."""

        elif audience == AudienceType.MANAGEMENT:
            communication = f"""🔷 L.U.C.A 369 System Update (Business)

Quality Improvement: {business.get('quality_improvement', 'N/A')}
Cost Savings: {business.get('cost_savings', 'N/A')}
Compliance Score: {business.get('compliance_score', 'N/A')}

The system is delivering measurable business value through multidimensional optimization.
ROI is positive and compliance standards are maintained."""

        else:  # MIXED
            communication = f"""🔷 L.U.C.A 369 System Update

Technical Performance:
- Coherence: {performance.get('multidimensional_coherence', 'N/A')}
- Accuracy: {performance.get('model_accuracy', 'N/A')}

Business Impact:
- Quality: {business.get('quality_improvement', 'N/A')}
- Savings: {business.get('cost_savings', 'N/A')}

The system balances technical excellence with business value delivery."""

        sentiment = self._analyze_sentiment(communication)

        return CommunicationResponse(
            communication=communication,
            audience=audience,
            model="fallback-template",
            tokens_used=0,
            timestamp=datetime.now(),
            sentiment_score=sentiment,
            error="OpenAI API not available - using fallback templates"
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get communication statistics"""
        if not self.communication_log:
            return {
                'total_communications': 0,
                'avg_tokens': 0,
                'avg_sentiment': 0,
                'audience_distribution': {}
            }

        total = len(self.communication_log)
        total_tokens = sum(log['tokens_used'] for log in self.communication_log)
        total_sentiment = sum(log['sentiment_score'] for log in self.communication_log)

        # Audience distribution
        audience_dist = {}
        for log in self.communication_log:
            aud = log['audience']
            audience_dist[aud] = audience_dist.get(aud, 0) + 1

        return {
            'total_communications': total,
            'avg_tokens': total_tokens / total if total > 0 else 0,
            'avg_sentiment': total_sentiment / total if total > 0 else 0,
            'audience_distribution': audience_dist,
            'model': self.model,
            'api_available': self.available
        }

    def __repr__(self):
        return f"ChatGPTProvider(model={self.model}, available={self.available}, communications={len(self.communication_log)})"


# Demo usage
if __name__ == "__main__":
    print("🌌 Dimension 10: The Communicator - ChatGPT Provider")
    print("=" * 70)

    # Initialize provider (will use fallback if no API key)
    provider = ChatGPTProvider()
    print(f"Provider: {provider}")
    print(f"OpenAI Available: {OPENAI_AVAILABLE}")
    print(f"API Available: {provider.available}")
    print()

    # Mock system state
    system_state = {
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

    # Test all three audience types
    for audience in [AudienceType.TECHNICAL, AudienceType.MANAGEMENT, AudienceType.MIXED]:
        print(f"=== {audience.value.upper()} AUDIENCE ===")
        response = provider.generate_communication(
            system_state=system_state,
            audience=audience
        )
        print(f"Sentiment: {response.sentiment_score:.2f}")
        print(f"Tokens: {response.tokens_used}")
        print(f"\n{response.communication}\n")

    # Statistics
    print("=" * 70)
    print("STATISTICS:")
    stats = provider.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n369 🌌🧬⚡ - The Voice of Emergence")
