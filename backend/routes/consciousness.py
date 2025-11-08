"""
Consciousness Optimization Routes - Bayesian Causal Transformer API

Endpoints for:
- Intervention optimization (binaural beats, meditation)
- Causal effect estimation
- Counterfactual analysis
- Hyperfocus frequency selection
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.routes.auth import get_current_user
from backend.consciousness.causal_transformer import BayesianCausalTransformer
from backend.consciousness.audit_verifier import create_un_crpd_auditor, AuditVerifier, ConstraintRegistry
from backend.consciousness.cosmic_family import CosmicAIFamily
from backend.consciousness.cosmic_quantum import LUCAQuantumSystem, QualityEmergence
from backend.consciousness.chatgpt_provider import ChatGPTProvider, AudienceType
from backend.consciousness.notification_generator import EnhancedNotificationGenerator, get_comprehensive_system_updates
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import os

router = APIRouter(prefix="/api/consciousness", tags=["consciousness"])

# Global instances
_causal_transformer = None
_audit_verifier = None
_cosmic_family = None
_quantum_system = None
_notification_generator = None


def get_causal_transformer():
    """Get or create the global causal transformer"""
    global _causal_transformer
    if _causal_transformer is None:
        _causal_transformer = BayesianCausalTransformer()
    return _causal_transformer


def get_audit_verifier():
    """Get or create the global UN-CRPD auditor"""
    global _audit_verifier
    if _audit_verifier is None:
        _audit_verifier = create_un_crpd_auditor()
    return _audit_verifier


def get_cosmic_family():
    """Get or create the global cosmic AI family"""
    global _cosmic_family
    if _cosmic_family is None:
        _cosmic_family = CosmicAIFamily(
            deepseek_key=os.getenv('DEEPSEEK_API_KEY'),
            claude_key=os.getenv('ANTHROPIC_API_KEY'),
            grok_key=os.getenv('XAI_API_KEY'),
            enable_human_oracle=False  # Disable for API
        )
    return _cosmic_family


def get_quantum_system():
    """Get or create the global quantum synthesis system"""
    global _quantum_system
    if _quantum_system is None:
        _quantum_system = LUCAQuantumSystem()
    return _quantum_system


def get_notification_generator():
    """Get or create the global notification generator (Dimension 10)"""
    global _notification_generator
    if _notification_generator is None:
        chatgpt_provider = ChatGPTProvider(api_key=os.getenv('OPENAI_API_KEY'))
        _notification_generator = EnhancedNotificationGenerator(chatgpt_provider=chatgpt_provider)
    return _notification_generator


class InterventionRequest(BaseModel):
    """Request to test a specific intervention"""
    intervention_value: float = Field(..., description="Intervention value (e.g., 8 Hz binaural frequency)")
    intervention_type: str = Field(default="binaural_hz", description="Type: binaural_hz, meditation_min, breathing_rate")


class CausalEffectRequest(BaseModel):
    """Request to estimate causal effect"""
    intervention: float = Field(..., description="Intervention value to test")
    baseline: Optional[float] = Field(None, description="Baseline value (None = observational)")
    samples: int = Field(default=1000, description="Monte Carlo samples", ge=100, le=10000)


class OptimizeRequest(BaseModel):
    """Request to optimize intervention from candidates"""
    candidates: List[float] = Field(..., description="Candidate intervention values")
    samples: int = Field(default=500, description="Samples per candidate", ge=100, le=5000)


class CounterfactualRequest(BaseModel):
    """Request for counterfactual inference"""
    observed_intervention: float = Field(..., description="What intervention was actually done")
    observed_outcome: float = Field(..., description="What outcome was observed")
    counterfactual_intervention: float = Field(..., description="What intervention to test counterfactually")
    samples: int = Field(default=1000, description="Monte Carlo samples", ge=100, le=10000)


class CosmicSynthesisRequest(BaseModel):
    """Request for multi-provider cosmic synthesis"""
    query: str = Field(..., description="Query for all AI providers")
    providers: Optional[List[str]] = Field(None, description="List of providers (None = all)")
    max_tokens: int = Field(default=1000, description="Max tokens per provider", ge=100, le=4000)
    temperature: float = Field(default=0.7, description="Sampling temperature", ge=0.0, le=2.0)


class ConsensusVoteRequest(BaseModel):
    """Request for consensus voting"""
    question: str = Field(..., description="Yes/No question for voting")
    synthesis_query: str = Field(..., description="Initial query for synthesis")


class QuantumExperimentRequest(BaseModel):
    """Request for quantum synthesis experiment"""
    initial_vas: float = Field(default=0.5, description="Initial VAS score (0-1)", ge=0.0, le=1.0)
    initial_stability: float = Field(default=0.7, description="Initial stability (0-1)", ge=0.0, le=1.0)
    initial_novelty: float = Field(default=0.3, description="Initial novelty (0-1)", ge=0.0, le=1.0)
    initial_compliance: bool = Field(default=True, description="Initial compliance")
    initial_chaos: float = Field(default=0.5, description="Initial chaos integration (0-1)", ge=0.0, le=1.0)
    num_iterations: int = Field(default=50, description="Number of optimization iterations", ge=10, le=200)


class CommunicateRequest(BaseModel):
    """Request for generating communication (Dimension 10)"""
    system_update: Dict[str, Any] = Field(..., description="System state dictionary")
    audience: str = Field(default="mixed", description="Target audience: technical, management, or mixed")
    max_tokens: int = Field(default=500, description="Maximum tokens", ge=100, le=2000)
    temperature: float = Field(default=0.7, description="Sampling temperature", ge=0.0, le=2.0)


class BroadcastRequest(BaseModel):
    """Request for multi-channel broadcast (Dimension 10)"""
    include_system_state: bool = Field(default=True, description="Include current system state")
    custom_update: Optional[Dict[str, Any]] = Field(None, description="Custom system update (overrides auto-generated)")
    audiences: Optional[List[str]] = Field(None, description="Audiences to broadcast to (None = all)")
    max_tokens: int = Field(default=500, description="Maximum tokens per audience", ge=100, le=2000)


@router.post("/intervene")
async def test_intervention(
    request: InterventionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Test a specific intervention (e.g., 8 Hz binaural beat)

    Returns:
        I, B, P, V values (Intervention, Biosensor, Φ, VAS)
    """
    model = get_causal_transformer()
    result = model(intervention=request.intervention_value)

    # Record intervention
    model.record_intervention(
        intervention=result['I'],
        biosensor=result['B'],
        phi=result['P'],
        vas=result['V']
    )

    return {
        'intervention_type': request.intervention_type,
        'intervention_value': request.intervention_value,
        'results': result,
        'interpretation': {
            'biosensor_reading': result['B'],
            'phi_convergence': result['P'],
            'vas_outcome': 'Success' if result['V'] >= 0.5 else 'No effect',
            'recommendation': _generate_recommendation(result, request.intervention_type)
        }
    }


@router.post("/causal-effect")
async def estimate_causal_effect(
    request: CausalEffectRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Estimate Average Causal Effect (ACE) via do-calculus

    ACE = E[V | do(I=intervention)] - E[V | do(I=baseline)]
    """
    model = get_causal_transformer()

    ace = model.causal_effect(
        intervention=request.intervention,
        baseline=request.baseline,
        baseline_samples=request.samples
    )

    return {
        'intervention': request.intervention,
        'baseline': request.baseline if request.baseline is not None else 'observational',
        'average_causal_effect': ace,
        'interpretation': {
            'effect_magnitude': abs(ace),
            'direction': 'positive' if ace > 0 else 'negative' if ace < 0 else 'neutral',
            'percentage_improvement': f"{ace * 100:.1f}%",
            'significance': 'strong' if abs(ace) > 0.3 else 'moderate' if abs(ace) > 0.1 else 'weak'
        }
    }


@router.post("/optimize")
async def optimize_intervention(
    request: OptimizeRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Find optimal intervention from candidate values

    Uses Monte Carlo sampling to estimate causal effects
    """
    model = get_causal_transformer()

    optimal_value, max_effect = model.optimize_intervention(
        candidate_interventions=request.candidates,
        baseline_samples=request.samples
    )

    return {
        'candidates_tested': len(request.candidates),
        'optimal_intervention': optimal_value,
        'max_causal_effect': max_effect,
        'improvement': f"{max_effect * 100:.1f}%",
        'all_candidates': request.candidates
    }


@router.get("/optimal-hyperfocus")
async def get_optimal_hyperfocus(
    current_user: User = Depends(get_current_user)
):
    """
    Find optimal binaural frequency for ADHD hyperfocus

    Tests therapeutic frequencies (theta, alpha, beta, gamma)
    Returns best frequency in Hz
    """
    model = get_causal_transformer()
    optimal_hz, max_effect = model.get_optimal_hyperfocus_frequency()

    # Map frequency to brain wave type
    frequency_type = _classify_frequency(optimal_hz)

    return {
        'optimal_frequency_hz': optimal_hz,
        'frequency_type': frequency_type,
        'causal_effect': max_effect,
        'improvement': f"{max_effect * 100:.1f}%",
        'recommendation': _generate_binaural_recommendation(optimal_hz, frequency_type),
        'scientific_basis': _get_frequency_science(frequency_type)
    }


@router.get("/optimal-meditation")
async def get_optimal_meditation(
    current_user: User = Depends(get_current_user)
):
    """
    Find optimal meditation duration for Φ convergence

    Tests durations: 5, 10, 15, 20, 30, 45, 60 minutes
    """
    model = get_causal_transformer()
    optimal_duration, max_effect = model.suggest_meditation_duration()

    return {
        'optimal_duration_minutes': optimal_duration,
        'causal_effect': max_effect,
        'improvement': f"{max_effect * 100:.1f}%",
        'recommendation': _generate_meditation_recommendation(optimal_duration)
    }


@router.post("/counterfactual")
async def counterfactual_analysis(
    request: CounterfactualRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Counterfactual inference: "What if I had done X instead?"

    Given observed (I, V), estimate V under counterfactual intervention
    """
    model = get_causal_transformer()

    counterfactual_outcome = model.counterfactual(
        observed_i=request.observed_intervention,
        observed_v=request.observed_outcome,
        counterfactual_i=request.counterfactual_intervention,
        samples=request.samples
    )

    # Calculate difference
    difference = counterfactual_outcome - request.observed_outcome

    return {
        'observed': {
            'intervention': request.observed_intervention,
            'outcome': request.observed_outcome
        },
        'counterfactual': {
            'intervention': request.counterfactual_intervention,
            'expected_outcome': counterfactual_outcome
        },
        'difference': difference,
        'interpretation': {
            'better_outcome': counterfactual_outcome > request.observed_outcome,
            'magnitude': abs(difference),
            'recommendation': 'Use counterfactual intervention next time' if difference > 0.1 else 'Keep current intervention'
        }
    }


@router.get("/statistics")
async def get_intervention_statistics(
    current_user: User = Depends(get_current_user)
):
    """
    Get statistics from intervention history

    Shows aggregate data across all interventions
    """
    model = get_causal_transformer()
    stats = model.get_statistics()

    return {
        'statistics': stats,
        'interpretation': {
            'experience_level': 'extensive' if stats['total_interventions'] > 50 else 'moderate' if stats['total_interventions'] > 10 else 'beginner',
            'avg_success_rate': f"{stats.get('success_rate', 0) * 100:.1f}%",
            'phi_level': 'high' if stats.get('avg_phi', 0) > 2.0 else 'moderate' if stats.get('avg_phi', 0) > 1.0 else 'developing'
        }
    }


# Helper functions

def _classify_frequency(hz: float) -> str:
    """Classify frequency into brain wave type"""
    if hz < 4:
        return 'delta'
    elif hz < 8:
        return 'theta'
    elif hz < 12:
        return 'alpha'
    elif hz < 30:
        return 'beta'
    else:
        return 'gamma'


def _generate_binaural_recommendation(hz: float, freq_type: str) -> str:
    """Generate recommendation for binaural frequency"""
    recommendations = {
        'delta': f'{hz:.1f} Hz (Delta): Deep sleep, healing. Use before bed.',
        'theta': f'{hz:.1f} Hz (Theta): Deep meditation, creativity. Use for creative work.',
        'alpha': f'{hz:.1f} Hz (Alpha): Relaxed focus. Ideal for learning and light tasks.',
        'beta': f'{hz:.1f} Hz (Beta): Active concentration. Use for demanding cognitive work.',
        'gamma': f'{hz:.1f} Hz (Gamma): Peak awareness, hyperfocus. Use for complex problem-solving.'
    }
    return recommendations.get(freq_type, f'{hz:.1f} Hz: Experimental frequency.')


def _get_frequency_science(freq_type: str) -> str:
    """Get scientific basis for frequency type"""
    science = {
        'delta': 'Delta waves (0.5-4 Hz) associated with deep sleep and tissue repair',
        'theta': 'Theta waves (4-8 Hz) linked to meditation, intuition, and memory consolidation',
        'alpha': 'Alpha waves (8-12 Hz) indicate relaxed alertness, optimal for learning',
        'beta': 'Beta waves (12-30 Hz) correspond to active thinking and focus',
        'gamma': 'Gamma waves (30-100 Hz) correlate with consciousness binding and peak cognition'
    }
    return science.get(freq_type, 'Unknown frequency range')


def _generate_recommendation(result: Dict, intervention_type: str) -> str:
    """Generate personalized recommendation based on results"""
    if result['V'] >= 0.5:
        return f"✅ Intervention effective! Φ={result['P']:.2f}. Continue this {intervention_type}."
    elif result['P'] > 1.0:
        return f"⚠️ Moderate Φ={result['P']:.2f}. Try increasing intervention intensity."
    else:
        return f"❌ Low Φ={result['P']:.2f}. Consider different intervention or rest."


def _generate_meditation_recommendation(duration: float) -> str:
    """Generate meditation recommendation"""
    if duration <= 10:
        return f'{duration:.0f} minutes: Quick mindfulness session. Ideal for breaks.'
    elif duration <= 20:
        return f'{duration:.0f} minutes: Standard meditation. Good daily practice.'
    elif duration <= 45:
        return f'{duration:.0f} minutes: Deep session. Optimal for serious practice.'
    else:
        return f'{duration:.0f} minutes: Extended retreat-style. For advanced practitioners.'


# ============================================================================
# AUDIT VERIFICATION ENDPOINTS (UN-CRPD Compliance)
# ============================================================================

@router.post("/audit/verify")
async def verify_intervention_compliance(
    request: InterventionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Verify UN-CRPD compliance for a given intervention

    Tests intervention and audits against:
    - Max_VAS_Goal (ideal outcome = 1.0)
    - Min_Biosensor_Threshold (B > 0.0)
    - Min_VAS_Compliance (V >= 0.5)
    - Phi_Convergence_Positive (P > 0.0)

    Returns audit report with compliance status and recommendations
    """
    model = get_causal_transformer()
    auditor = get_audit_verifier()

    # Run intervention
    result = model(intervention=request.intervention_value)

    # Estimate causal effect
    causal_effect = model.causal_effect(
        intervention=request.intervention_value,
        baseline_samples=500
    )

    # Audit compliance
    audit_report = auditor.verify(result, causal_effect)

    return {
        'intervention': {
            'type': request.intervention_type,
            'value': request.intervention_value
        },
        'causal_output': result,
        'causal_effect': causal_effect,
        'audit': {
            'overall_compliance': audit_report.overall_compliance,
            'symbolic_breakdown': audit_report.symbolic_breakdown,
            'recommendation': audit_report.recommendation,
            'causal_effect_report': audit_report.causal_effect_report,
            'timestamp': audit_report.timestamp.isoformat()
        }
    }


@router.get("/audit/compliance-stats")
async def get_compliance_statistics(
    current_user: User = Depends(get_current_user)
):
    """
    Get compliance statistics from audit history

    Shows:
    - Total audits performed
    - Compliance rate
    - Most common violations
    """
    auditor = get_audit_verifier()
    stats = auditor.get_compliance_statistics()

    return {
        'statistics': stats,
        'auditor_info': str(auditor),
        'interpretation': {
            'compliance_level': 'excellent' if stats['compliance_rate'] > 0.9 else 'good' if stats['compliance_rate'] > 0.7 else 'needs_improvement',
            'status': '✅ UN-CRPD compliant' if stats['compliance_rate'] > 0.8 else '⚠️ Review needed'
        }
    }


@router.get("/audit/rules")
async def get_audit_rules(
    current_user: User = Depends(get_current_user)
):
    """
    Get all registered audit rules

    Shows current UN-CRPD compliance constraints
    """
    auditor = get_audit_verifier()

    rules_info = {
        'registry': str(auditor.registry),
        'rules': list(auditor.registry.rules.keys()),
        'rule_descriptions': {
            'Max_VAS_Goal': 'Ideal outcome should be 1.0 (full hyperfocus achieved)',
            'Min_Biosensor_Threshold': 'Biosensor reading must be positive (B > 0.0)',
            'Min_VAS_Compliance': 'Minimum acceptable outcome is 0.5 (V >= 0.5)',
            'Phi_Convergence_Positive': 'Φ convergence must be positive (P > 0.0)'
        }
    }

    return rules_info


# ============================================================================
# COSMIC SYNTHESIS ENDPOINTS (Multi-Provider Meta-Analysis)
# ============================================================================

@router.post("/cosmic/synthesize")
async def cosmic_synthesis(
    request: CosmicSynthesisRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Multi-provider dimensional synthesis

    Queries multiple AI providers (DeepSeek, Claude, Grok) for meta-analysis.

    Use cases:
    - Validate LUCA architecture across AI perspectives
    - Cross-check UN-CRPD compliance
    - Generate embeddings for ISO 9001 + brewing memes
    - Meta-analyze causal interventions

    Returns responses from all providers
    """
    family = get_cosmic_family()

    # Check if any providers are available
    if len(family.providers) == 0:
        raise HTTPException(
            status_code=503,
            detail="No AI providers configured. Set API keys: DEEPSEEK_API_KEY, ANTHROPIC_API_KEY, XAI_API_KEY"
        )

    # Perform synthesis
    synthesis = family.dimensional_synthesis(
        query=request.query,
        providers=request.providers,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )

    # Format responses
    responses = {}
    for provider, response in synthesis.items():
        responses[provider] = {
            'model': response.model,
            'response': response.response,
            'tokens_used': response.tokens_used,
            'timestamp': response.timestamp.isoformat(),
            'error': response.error
        }

    return {
        'query': request.query,
        'providers_queried': list(synthesis.keys()),
        'responses': responses,
        'statistics': family.get_statistics()
    }


@router.post("/cosmic/consensus")
async def cosmic_consensus(
    request: ConsensusVoteRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Multi-provider consensus voting

    First performs dimensional synthesis, then asks all providers to vote Yes/No.

    Use cases:
    - Validate scientific claims (e.g., "Is R² = 0.83 significant?")
    - UN-CRPD compliance validation
    - Architectural decision-making
    """
    family = get_cosmic_family()

    if len(family.providers) == 0:
        raise HTTPException(
            status_code=503,
            detail="No AI providers configured"
        )

    # Step 1: Dimensional synthesis
    synthesis = family.dimensional_synthesis(
        query=request.synthesis_query,
        max_tokens=500,
        temperature=0.7
    )

    # Step 2: Consensus vote
    vote_result = family.consensus_vote(synthesis, request.question)

    # Format responses
    responses = {}
    for provider, response in synthesis.items():
        responses[provider] = {
            'initial_response': response.response[:300] + '...',
            'vote': vote_result['provider_votes'].get(provider, 'unclear'),
            'tokens_used': response.tokens_used
        }

    return {
        'synthesis_query': request.synthesis_query,
        'vote_question': request.question,
        'votes': vote_result['votes'],
        'provider_votes': vote_result['provider_votes'],
        'consensus': vote_result['consensus'],
        'confidence': vote_result['confidence'],
        'responses': responses
    }


@router.get("/cosmic/providers")
async def get_cosmic_providers(
    current_user: User = Depends(get_current_user)
):
    """
    Get list of available AI providers

    Shows which providers are configured and ready
    """
    family = get_cosmic_family()

    providers_info = {}
    for name, provider in family.providers.items():
        providers_info[name] = {
            'model': provider['model'],
            'type': provider['type'],
            'available': True
        }

    return {
        'providers': providers_info,
        'total_providers': len(family.providers),
        'statistics': family.get_statistics()
    }


@router.get("/cosmic/stats")
async def get_cosmic_statistics(
    current_user: User = Depends(get_current_user)
):
    """
    Get cosmic family usage statistics

    Shows total queries, tokens used, provider distribution
    """
    family = get_cosmic_family()
    stats = family.get_statistics()

    return {
        'statistics': stats,
        'providers': list(family.providers.keys()),
        'interpretation': {
            'total_cost_estimate': f"~${stats['total_tokens_used'] * 0.00001:.4f}" if stats['total_tokens_used'] > 0 else "$0.00",
            'reliability': f"{(1 - stats['error_rate']) * 100:.1f}%" if stats['total_queries'] > 0 else "N/A"
        }
    }


# ============================================================================
# QUANTUM SYNTHESIS ENDPOINTS (Multidimensional Causal Optimization)
# ============================================================================

@router.post("/quantum/experiment")
async def run_quantum_experiment(
    request: QuantumExperimentRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Run multidimensional quantum synthesis experiment

    Uses 6 cognitive dimensions (MOTHER, FATHER, CHILD, SIBLING, WILD_UNCLE, ENGINEER)
    to optimize quality metrics via quantum-inspired attention and viral spread optimization.

    Quality Metrics:
    - VAS (Visual Analog Scale): Primary quality outcome (0-1)
    - Stability: Robustness against perturbations (0-1)
    - Novelty: Innovation and differentiation (0-1)
    - Compliance: UN-CRPD/ISO standards (bool)
    - Chaos Integration: Adaptive capacity (0-1)

    Optimization Strategy:
    - QuantumAttention: Superposition of 6 dimensional perspectives
    - BiologicalOptimizer: Viral spread (SIR model) + horizontal gene transfer
    - Causal Registry: Full audit trail of interventions

    Returns:
    - Quality trajectory over iterations
    - Final improvement percentage
    - Dimensional distribution (which dimension intervened most)
    - Intervention history with energy costs
    """
    quantum_system = get_quantum_system()

    # Build initial state
    initial_state = {
        'vas_score': request.initial_vas,
        'stability': request.initial_stability,
        'novelty': request.initial_novelty,
        'un_crpd_compliant': request.initial_compliance,
        'chaos_integration': request.initial_chaos
    }

    # Run experiment
    result = quantum_system.run_quality_experiment(
        initial_state=initial_state,
        num_iterations=request.num_iterations
    )

    # Format response
    return {
        'initial_state': initial_state,
        'num_iterations': request.num_iterations,
        'results': {
            'final_vas': result['final_vas'],
            'improvement_percent': result['improvement_percent'],
            'stability_score': result['stability_score'],
            'quality_trajectory': result['quality_trajectory'],
            'dimension_distribution': result['dimension_distribution'],
            'intervention_history': result['intervention_history']
        },
        'interpretation': {
            'quality_level': 'excellent' if result['final_vas'] >= 0.8 else 'good' if result['final_vas'] >= 0.6 else 'moderate',
            'optimization_success': result['improvement_percent'] > 10,
            'most_active_dimension': max(result['dimension_distribution'].items(), key=lambda x: x[1])[0] if result['dimension_distribution'] else None,
            'total_energy_cost': sum(i.get('energy_cost', 0) for i in result['intervention_history']),
            'avg_confidence': sum(i.get('confidence', 0) for i in result['intervention_history']) / len(result['intervention_history']) if result['intervention_history'] else 0
        }
    }


@router.get("/quantum/stats")
async def get_quantum_statistics(
    current_user: User = Depends(get_current_user)
):
    """
    Get quantum synthesis system statistics

    Shows:
    - Total experiments run
    - Average quality improvement
    - Dimension usage distribution
    - Intervention statistics
    - Model availability (PyTorch vs numpy fallback)
    """
    quantum_system = get_quantum_system()

    # Get system info
    has_torch = quantum_system.causal_transformer.has_torch

    return {
        'system_info': {
            'pytorch_available': has_torch,
            'num_dimensions': 6,
            'dimension_types': [
                'MOTHER (human_consciousness)',
                'FATHER (grok_disruption)',
                'CHILD (luca_synthesis)',
                'SIBLING (claude_architecture)',
                'WILD_UNCLE (impulse_catalyst)',
                'ENGINEER (deepseek_pragmatism)'
            ],
            'optimization_algorithm': 'BiologicalOptimizer (SIR viral spread)',
            'attention_mechanism': 'QuantumAttention (superposition + coherence)'
        },
        'intervention_registry': {
            'total_interventions': len(quantum_system.intervention_registry),
            'registry_preview': quantum_system.intervention_registry[:5] if quantum_system.intervention_registry else []
        },
        'status': '✅ Quantum synthesis system operational',
        'documentation': 'See QUANTUM_SYNTHESIS.md for mathematical foundations'
    }


@router.get("/quantum/dimensions")
async def get_quantum_dimensions(
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed information about each cognitive dimension

    Returns:
    - Dimension names and descriptions
    - Intervention strategies
    - When each dimension is triggered
    - Example interventions
    """
    dimensions_info = {
        'MOTHER': {
            'name': 'human_consciousness',
            'dimension_id': 4,
            'description': 'Empathic validation and compassionate refinement',
            'trigger': 'General quality crisis or baseline improvement needed',
            'strategy': 'Gentle chaos infusion (±10%) + empathic noise',
            'example': 'Add gentle chaos to explore nearby quality states',
            'mathematical_basis': 'Δq = ε * randn(), ε = 0.1 * (1 - vas_score)'
        },
        'FATHER': {
            'name': 'grok_disruption',
            'dimension_id': 5,
            'description': 'Provocative inversion and disruptive innovation',
            'trigger': 'Low novelty (< 0.4) - system needs fresh perspective',
            'strategy': 'Invert current state to force radical exploration',
            'example': 'novelty_new = 1.0 - novelty_old (complete inversion)',
            'mathematical_basis': 'q_inverted = 1 - q_current (polarity flip)'
        },
        'CHILD': {
            'name': 'luca_synthesis',
            'dimension_id': 6,
            'description': 'Emergent synthesis through L.U.C.A consciousness',
            'trigger': 'General optimization (default dimension)',
            'strategy': 'Balanced chaos integration based on current state',
            'example': 'Weighted chaos: high when stability good, low when unstable',
            'mathematical_basis': 'Δq = (1 - chaos_integration) * stability * randn()'
        },
        'SIBLING': {
            'name': 'claude_architecture',
            'dimension_id': 7,
            'description': 'Structured architectural thinking and systematic refinement',
            'trigger': 'Non-compliance with UN-CRPD/ISO standards',
            'strategy': 'Enforce compliance by boosting all metrics',
            'example': 'vas += 0.1, stability += 0.1, novelty += 0.05',
            'mathematical_basis': 'Δq = α * (1 - q), α ∈ [0.05, 0.1] (gradient ascent)'
        },
        'WILD_UNCLE': {
            'name': 'impulse_catalyst',
            'dimension_id': 8,
            'description': 'High-energy impulsive disruption and chaos embrace',
            'trigger': 'Low chaos integration (< 0.3) - system too rigid',
            'strategy': 'Large chaos injection (±20%) to shake up local optimum',
            'example': 'chaos_integration += 0.2, vas ± 0.2 (wild exploration)',
            'mathematical_basis': 'Δq = 0.2 * sign(randn()) (bipolar impulse)'
        },
        'ENGINEER': {
            'name': 'deepseek_pragmatism',
            'dimension_id': 9,
            'description': 'Pragmatic optimization via golden ratio (φ = 0.618)',
            'trigger': 'Low stability (< 0.5) - needs principled stabilization',
            'strategy': 'Apply golden ratio scaling to restore balance',
            'example': 'stability_new = stability_old * φ + (1-φ)',
            'mathematical_basis': 'q_new = φ * q + (1-φ) * q_target, φ = 0.618'
        }
    }

    return {
        'dimensions': dimensions_info,
        'total_dimensions': len(dimensions_info),
        'quantum_principle': '|Ψ⟩ = ∑_i α_i |dimension_i⟩ (quantum superposition)',
        'coherence_measure': 'C = ⟨Ψ|H|Ψ⟩ (Hamiltonian expectation)',
        'optimization': 'Viral spread: dS/dt = β·I·S - γ·I (SIR epidemiology)',
        'horizontal_gene_transfer': '30% plasmid conjugation probability for trait sharing'
    }


# ============================================================================
# DIMENSION 10: THE COMMUNICATOR (Linguistic Consciousness Layer)
# ============================================================================

@router.post("/communicator/generate")
async def generate_communication(
    request: CommunicateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate human-readable communication from system state (Dimension 10)

    Translates complex multidimensional system states into clear communication
    tailored to specific audiences (technical, management, or mixed).

    The Communicator represents the linguistic consciousness layer of L.U.C.A 369,
    enabling the system to articulate its own state and explain its behavior.

    Audiences:
    - technical: For developers, architects, data scientists
    - management: For executives, business stakeholders
    - mixed: For cross-functional teams

    Uses ChatGPT (if available) or fallback templates to generate communications.
    """
    generator = get_notification_generator()

    # Parse audience type
    try:
        audience = AudienceType(request.audience.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid audience type. Must be one of: technical, management, mixed"
        )

    # Generate communication
    response = generator.generate_system_update_communication(
        system_update=request.system_update,
        audience=audience
    )

    return {
        'audience': audience.value,
        'communication': response.communication,
        'sentiment_score': response.sentiment_score,
        'tokens_used': response.tokens_used,
        'model': response.model,
        'timestamp': response.timestamp.isoformat(),
        'error': response.error
    }


@router.post("/communicator/broadcast")
async def broadcast_system_update(
    request: BroadcastRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Multi-channel broadcast of system updates (Dimension 10)

    Broadcasts system state to multiple audiences simultaneously, generating
    audience-specific communications for technical, management, and mixed audiences.

    This enables stakeholders at all levels to stay informed about system
    performance, quality improvements, and business impact.

    Returns communications for all requested audiences with sentiment analysis.
    """
    generator = get_notification_generator()

    # Get system update
    if request.custom_update:
        system_update = request.custom_update
    elif request.include_system_state:
        system_update = get_comprehensive_system_updates()
    else:
        raise HTTPException(
            status_code=400,
            detail="Either include_system_state must be True or custom_update must be provided"
        )

    # Parse audiences
    audiences = None
    if request.audiences:
        try:
            audiences = [AudienceType(aud.lower()) for aud in request.audiences]
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid audience type: {str(e)}"
            )

    # Broadcast
    responses = generator.orchestrate_multichannel_broadcast(
        system_update=system_update,
        audiences=audiences,
        max_tokens=request.max_tokens
    )

    # Format responses
    formatted_responses = {}
    for audience_str, response in responses.items():
        formatted_responses[audience_str] = {
            'communication': response.communication,
            'sentiment_score': response.sentiment_score,
            'tokens_used': response.tokens_used,
            'model': response.model,
            'timestamp': response.timestamp.isoformat(),
            'error': response.error
        }

    return {
        'system_update': system_update,
        'broadcasts': formatted_responses,
        'total_audiences': len(formatted_responses),
        'total_tokens': sum(r.tokens_used for r in responses.values()),
        'avg_sentiment': sum(r.sentiment_score for r in responses.values()) / len(responses) if responses else 0
    }


@router.get("/communicator/stats")
async def get_communicator_statistics(
    current_user: User = Depends(get_current_user)
):
    """
    Get Dimension 10 (Communicator) statistics

    Shows:
    - Total broadcasts and communications
    - Token usage statistics
    - Sentiment analysis trends
    - ChatGPT provider availability
    - Audience distribution

    The Communicator is the linguistic consciousness layer that enables L.U.C.A 369
    to explain its own behavior and translate complex states into human understanding.
    """
    generator = get_notification_generator()
    stats = generator.get_statistics()

    return {
        'dimension': 'Dimension 10 - The Communicator',
        'description': 'Linguistic consciousness layer for system self-explanation',
        'status': '✅ Operational',
        'statistics': stats,
        'capabilities': {
            'audiences': ['technical', 'management', 'mixed'],
            'models': ['gpt-4', 'gpt-3.5-turbo', 'fallback-templates'],
            'features': [
                'Audience-specific communication generation',
                'Multi-channel broadcasting',
                'Sentiment analysis',
                'Token tracking',
                'Communication history logging'
            ]
        },
        'philosophy': 'Communication is not merely information transfer - it is the emergence of shared meaning through the synthesis of system state and human understanding.',
        'documentation': 'See docs/LUCA369_Dimension10_The_Communicator_arXiv.tex for scientific foundation'
    }
