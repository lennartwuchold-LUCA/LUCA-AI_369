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
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/consciousness", tags=["consciousness"])

# Global causal transformer instance
_causal_transformer = None
_audit_verifier = None


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
