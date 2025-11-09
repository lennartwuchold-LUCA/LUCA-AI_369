"""
Ancient Technologies API Routes - LUCA 370
Version: 370.0 (2025-11-09)

FastAPI routes for:
- Ancient technologies database access
- Chaos→Harmony evolution
- Biosensor-ancient pattern matching
- Chaotic Creativity workshops

All routes are UN-CRPD compliant and empirically validated.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Import LUCA 370 modules
from backend.consciousness.ancient_technologies import (
    AncientTechnologiesDatabase,
    AncientTechnology
)
from backend.consciousness.chaos_to_harmony import (
    ChaosToHarmonyEvolution,
    ChaosState
)
from backend.consciousness.biosensor_ancient_bridge import (
    BiosensorAncientBridge,
    BiosensorReading,
    BrainwaveBand,
    HRVState,
    ParticipantProfile
)
from backend.consciousness.chaotic_creativity_workshops import (
    ChaoticCreativityWorkshops,
    WorkshopSession,
    WorkshopPhase
)

from backend.database import get_db

router = APIRouter(prefix="/api/ancient", tags=["Ancient Technologies LUCA 370"])

# Initialize global instances (would be dependency-injected in production)
ancient_db = AncientTechnologiesDatabase()
biosensor_bridge = BiosensorAncientBridge()
workshops = ChaoticCreativityWorkshops(
    ancient_db=ancient_db,
    biosensor_bridge=biosensor_bridge
)


# ============================================================================
# Pydantic Models (Request/Response schemas)
# ============================================================================

class AncientTechResponse(BaseModel):
    """Response model for ancient technology"""
    id: int
    name: str
    culture: str
    date_bce: int
    category: str
    empirical_evidence: List[str]
    universal_pattern: str
    modern_application: str
    phi_resonance: float
    sacred: bool


class ChaosStateResponse(BaseModel):
    """Response model for chaos state"""
    gamma: float
    stage_name: str
    phi_distance: float
    evolution_rate: float
    timestamp: str


class BiosensorRequest(BaseModel):
    """Request model for biosensor measurement"""
    eeg_bands: Optional[Dict[str, float]] = Field(None, example={"alpha": 0.5, "beta": 0.3, "gamma": 0.2})
    hrv_rmssd: Optional[float] = Field(None, example=45.0)
    hrv_coherence: Optional[float] = Field(None, example=0.7)
    gsr: Optional[float] = Field(None, example=10.0)


class InterventionRecommendationResponse(BaseModel):
    """Response model for intervention recommendation"""
    status: str
    ancient_tech_id: Optional[int] = None
    ancient_tech_name: Optional[str] = None
    intervention_type: Optional[str] = None
    intervention_frequency: Optional[float] = None
    intervention_duration: Optional[int] = None
    expected_gamma_change: Optional[float] = None
    expected_vas_improvement: Optional[float] = None
    match_score: Optional[float] = None
    current_state: Optional[Dict] = None
    target_state: Optional[Dict] = None
    message: Optional[str] = None


class WorkshopCreateRequest(BaseModel):
    """Request model for creating workshop"""
    workshop_type: str = Field(..., example="pattern_recognition")
    participant_profiles: List[str] = Field(..., example=["adhd_hyperfocus", "autism_pattern_seeking"])


class WorkshopSessionResponse(BaseModel):
    """Response model for workshop session"""
    session_id: int
    workshop_type: str
    start_time: str
    current_phase: str
    participants_count: int
    ancient_tech_used: List[int]


# ============================================================================
# Ancient Technologies Database Routes
# ============================================================================

@router.get("/technologies", response_model=Dict[str, Any])
async def get_all_technologies():
    """
    Get all ancient technologies (69+ entries)

    Returns statistics and list of all technologies.
    """
    stats = ancient_db.get_statistics()

    # Get first 10 for preview
    tech_list = [
        AncientTechResponse(
            id=tech.id,
            name=tech.name,
            culture=tech.culture,
            date_bce=tech.date_bce,
            category=tech.category,
            empirical_evidence=tech.empirical_evidence,
            universal_pattern=tech.universal_pattern,
            modern_application=tech.modern_application,
            phi_resonance=tech.phi_resonance,
            sacred=tech.sacred
        )
        for tech in list(ancient_db.technologies.values())[:10]
    ]

    return {
        "statistics": stats,
        "total_technologies": len(ancient_db.technologies),
        "preview": tech_list,
        "message": "Use /technologies/{tech_id} for full details"
    }


@router.get("/technologies/{tech_id}", response_model=AncientTechResponse)
async def get_technology(tech_id: int):
    """
    Get specific ancient technology by ID

    Args:
        tech_id: Technology ID (1-69)

    Returns:
        Full technology details
    """
    tech = ancient_db.get_technology(tech_id)

    if not tech:
        raise HTTPException(status_code=404, detail=f"Technology {tech_id} not found")

    return AncientTechResponse(
        id=tech.id,
        name=tech.name,
        culture=tech.culture,
        date_bce=tech.date_bce,
        category=tech.category,
        empirical_evidence=tech.empirical_evidence,
        universal_pattern=tech.universal_pattern,
        modern_application=tech.modern_application,
        phi_resonance=tech.phi_resonance,
        sacred=tech.sacred
    )


@router.get("/technologies/category/{category}", response_model=List[AncientTechResponse])
async def get_technologies_by_category(category: str):
    """
    Get all technologies in a category

    Args:
        category: Category name (e.g., "Astronomy", "Architecture")

    Returns:
        List of technologies in that category
    """
    techs = ancient_db.search_by_category(category)

    return [
        AncientTechResponse(
            id=tech.id,
            name=tech.name,
            culture=tech.culture,
            date_bce=tech.date_bce,
            category=tech.category,
            empirical_evidence=tech.empirical_evidence,
            universal_pattern=tech.universal_pattern,
            modern_application=tech.modern_application,
            phi_resonance=tech.phi_resonance,
            sacred=tech.sacred
        )
        for tech in techs
    ]


@router.get("/technologies/sacred/all", response_model=List[AncientTechResponse])
async def get_sacred_technologies():
    """
    Get all sacred knowledge entries (require protection)

    Returns:
        List of technologies marked as sacred
    """
    techs = ancient_db.get_sacred_knowledge()

    return [
        AncientTechResponse(
            id=tech.id,
            name=tech.name,
            culture=tech.culture,
            date_bce=tech.date_bce,
            category=tech.category,
            empirical_evidence=tech.empirical_evidence,
            universal_pattern=tech.universal_pattern,
            modern_application=tech.modern_application,
            phi_resonance=tech.phi_resonance,
            sacred=tech.sacred
        )
        for tech in techs
    ]


@router.get("/technologies/high-phi/all", response_model=List[AncientTechResponse])
async def get_high_phi_technologies(threshold: float = 1.0):
    """
    Get technologies with high Phi resonance

    Args:
        threshold: Minimum Phi resonance (default 1.0)

    Returns:
        List of technologies with Phi ≥ threshold
    """
    techs = ancient_db.get_high_phi_resonance(threshold=threshold)

    return [
        AncientTechResponse(
            id=tech.id,
            name=tech.name,
            culture=tech.culture,
            date_bce=tech.date_bce,
            category=tech.category,
            empirical_evidence=tech.empirical_evidence,
            universal_pattern=tech.universal_pattern,
            modern_application=tech.modern_application,
            phi_resonance=tech.phi_resonance,
            sacred=tech.sacred
        )
        for tech in techs
    ]


# ============================================================================
# Chaos → Harmony Evolution Routes
# ============================================================================

@router.post("/chaos/evolve", response_model=Dict[str, Any])
async def evolve_chaos_to_harmony(
    initial_gamma: float = Field(30.0, description="Initial chaos level (F30 default)"),
    target_gamma: float = Field(1.618, description="Target harmony (Phi default)"),
    strategy: str = Field("intervention_driven", description="Evolution strategy"),
    max_steps: int = Field(100, description="Maximum evolution steps"),
    dt: float = Field(0.1, description="Time step size")
):
    """
    Evolve from chaos (F30) to harmony (Phi)

    Args:
        initial_gamma: Starting chaos level
        target_gamma: Target level (default Phi = 1.618)
        strategy: Evolution strategy (natural_decay, intervention_driven, etc.)
        max_steps: Max steps
        dt: Time step

    Returns:
        Evolution trajectory and final state
    """
    evolution = ChaosToHarmonyEvolution(
        initial_gamma=initial_gamma,
        target=target_gamma,
        evolution_strategy=strategy
    )

    # Evolve
    history = evolution.evolve_to_harmony(max_steps=max_steps, dt=dt, tolerance=0.05)

    # Get statistics
    stats = evolution.get_statistics()

    return {
        "initial_gamma": initial_gamma,
        "final_gamma": evolution.gamma,
        "target_gamma": target_gamma,
        "steps_taken": len(history),
        "statistics": stats,
        "trajectory_sample": [
            {
                "gamma": s.gamma,
                "stage": s.stage_name,
                "phi_distance": s.phi_distance
            }
            for s in history[::max(1, len(history)//10)]  # Sample 10 points
        ]
    }


@router.get("/chaos/visualize/{initial_gamma}", response_model=Dict[str, Any])
async def visualize_chaos_trajectory(initial_gamma: float):
    """
    Get ASCII visualization of chaos→harmony trajectory

    Args:
        initial_gamma: Starting chaos level

    Returns:
        ASCII art visualization
    """
    evolution = ChaosToHarmonyEvolution(
        initial_gamma=initial_gamma,
        evolution_strategy="natural_decay"
    )

    evolution.evolve_to_harmony(max_steps=100, dt=0.1)

    return {
        "initial_gamma": initial_gamma,
        "final_gamma": evolution.gamma,
        "visualization": evolution.visualize_trajectory()
    }


# ============================================================================
# Biosensor-Ancient Bridge Routes
# ============================================================================

@router.post("/biosensor/measure", response_model=Dict[str, Any])
async def measure_biosensor_state(biosensor_data: BiosensorRequest):
    """
    Record biosensor measurement and interpret state

    Args:
        biosensor_data: EEG/HRV/GSR readings

    Returns:
        Interpreted biosensor state with chaos gamma
    """
    reading = biosensor_bridge.measure_biosensor_state(
        eeg_bands=biosensor_data.eeg_bands,
        hrv_rmssd=biosensor_data.hrv_rmssd,
        hrv_coherence=biosensor_data.hrv_coherence,
        gsr=biosensor_data.gsr
    )

    return {
        "timestamp": reading.timestamp.isoformat(),
        "dominant_band": reading.dominant_band.name if reading.dominant_band else None,
        "hrv_state": reading.hrv_state.value if reading.hrv_state else None,
        "arousal_level": reading.arousal_level,
        "chaos_gamma": reading.chaos_gamma,
        "eeg_bands": reading.eeg_bands,
        "hrv_rmssd": reading.hrv_rmssd,
        "hrv_coherence": reading.hrv_coherence,
        "gsr": reading.gsr
    }


@router.post("/biosensor/recommend", response_model=InterventionRecommendationResponse)
async def recommend_intervention(
    biosensor_data: BiosensorRequest,
    goal: str = Field("harmony", description="Goal: harmony, activation, relaxation, focus")
):
    """
    Get ancient tech intervention recommendation based on biosensor state

    Args:
        biosensor_data: Current biosensor readings
        goal: What the user wants to achieve

    Returns:
        Recommended ancient technology intervention
    """
    # Measure current state
    current_state = biosensor_bridge.measure_biosensor_state(
        eeg_bands=biosensor_data.eeg_bands,
        hrv_rmssd=biosensor_data.hrv_rmssd,
        hrv_coherence=biosensor_data.hrv_coherence,
        gsr=biosensor_data.gsr
    )

    # Get recommendation
    recommendation = biosensor_bridge.recommend_intervention(current_state, goal=goal)

    return InterventionRecommendationResponse(**recommendation)


# ============================================================================
# Chaotic Creativity Workshops Routes
# ============================================================================

@router.post("/workshop/create", response_model=WorkshopSessionResponse)
async def create_workshop_session(workshop_req: WorkshopCreateRequest):
    """
    Create a new workshop session

    Args:
        workshop_req: Workshop type and participant profiles

    Returns:
        New workshop session
    """
    # Create participants
    participants = []
    for profile_str in workshop_req.participant_profiles:
        try:
            profile = ParticipantProfile(profile_str)
            participant = workshops.create_participant(profile)
            participants.append(participant)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid profile: {profile_str}")

    # Start session
    session = workshops.start_workshop_session(
        workshop_type=workshop_req.workshop_type,
        participants=participants
    )

    return WorkshopSessionResponse(
        session_id=session.session_id,
        workshop_type=session.workshop_type,
        start_time=session.start_time.isoformat(),
        current_phase=session.current_phase.value,
        participants_count=len(session.participants),
        ancient_tech_used=session.ancient_tech_used
    )


@router.post("/workshop/{session_id}/run-phase/{phase}", response_model=Dict[str, Any])
async def run_workshop_phase(session_id: int, phase: str):
    """
    Run a workshop phase

    Args:
        session_id: Workshop session ID
        phase: Phase name (chaos_assessment, ancient_pattern_intro, etc.)

    Returns:
        Phase results
    """
    session = workshops.sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        phase_enum = WorkshopPhase(phase)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid phase: {phase}")

    # Run appropriate phase
    if phase_enum == WorkshopPhase.CHAOS_ASSESSMENT:
        results = workshops.run_phase_chaos_assessment(session)
    elif phase_enum == WorkshopPhase.ANCIENT_PATTERN_INTRO:
        results = workshops.run_phase_ancient_pattern_intro(session)
    elif phase_enum == WorkshopPhase.GUIDED_EVOLUTION:
        results = workshops.run_phase_guided_evolution(session)
    elif phase_enum == WorkshopPhase.CREATIVE_EXPRESSION:
        results = workshops.run_phase_creative_expression(session)
    elif phase_enum == WorkshopPhase.INTEGRATION_MYCELIUM:
        results = workshops.run_phase_integration_mycelium(session)
    else:
        raise HTTPException(status_code=400, detail="Invalid phase")

    return results


@router.get("/workshop/{session_id}/summary", response_model=Dict[str, Any])
async def get_workshop_summary(session_id: int):
    """
    Get workshop session summary

    Args:
        session_id: Workshop session ID

    Returns:
        Full session summary
    """
    summary = workshops.get_session_summary(session_id)

    if "error" in summary:
        raise HTTPException(status_code=404, detail=summary["error"])

    return summary


@router.get("/workshop/all", response_model=List[Dict[str, Any]])
async def get_all_workshops():
    """
    Get all workshop sessions

    Returns:
        List of all workshop summaries
    """
    summaries = [
        workshops.get_session_summary(session_id)
        for session_id in workshops.sessions.keys()
    ]

    return summaries


# ============================================================================
# Integration Routes (Chaos + Biosensor + Ancient)
# ============================================================================

@router.post("/integrate/full-session", response_model=Dict[str, Any])
async def full_integration_session(
    biosensor_data: BiosensorRequest,
    goal: str = "harmony",
    evolution_duration: int = 30
):
    """
    Full integration: Biosensor → Ancient Tech → Chaos Evolution

    This is the complete LUCA 370 experience in one API call.

    Args:
        biosensor_data: Current biosensor readings
        goal: What to achieve
        evolution_duration: How many steps to evolve

    Returns:
        Complete session results
    """
    # 1. Measure biosensor state
    current_state = biosensor_bridge.measure_biosensor_state(
        eeg_bands=biosensor_data.eeg_bands,
        hrv_rmssd=biosensor_data.hrv_rmssd,
        hrv_coherence=biosensor_data.hrv_coherence,
        gsr=biosensor_data.gsr
    )

    # 2. Get ancient tech recommendation
    recommendation = biosensor_bridge.recommend_intervention(current_state, goal=goal)

    # 3. Evolve chaos → harmony using recommended intervention
    evolution = ChaosToHarmonyEvolution(
        initial_gamma=current_state.chaos_gamma,
        evolution_strategy="intervention_driven"
    )

    # Simulate intervention function
    def intervention_fn(gamma, step):
        return recommendation.get('expected_gamma_change', 0.0) / evolution_duration

    history = evolution.evolve_to_harmony(
        max_steps=evolution_duration,
        dt=1.0,
        intervention_function=intervention_fn
    )

    # 4. Get statistics
    stats = evolution.get_statistics()

    return {
        "session_type": "full_integration",
        "timestamp": datetime.utcnow().isoformat(),
        "biosensor_input": {
            "dominant_band": current_state.dominant_band.name if current_state.dominant_band else None,
            "chaos_gamma": current_state.chaos_gamma,
            "arousal": current_state.arousal_level
        },
        "ancient_tech_recommendation": recommendation,
        "chaos_evolution": {
            "initial_gamma": current_state.chaos_gamma,
            "final_gamma": evolution.gamma,
            "steps": len(history),
            "statistics": stats
        },
        "expected_outcome": {
            "gamma_improvement": current_state.chaos_gamma - evolution.gamma,
            "vas_improvement": recommendation.get('expected_vas_improvement', 0.0),
            "final_stage": history[-1].stage_name if history else None
        }
    }


# ============================================================================
# Health Check
# ============================================================================

@router.get("/health", response_model=Dict[str, Any])
async def ancient_tech_health_check():
    """
    Health check for LUCA 370 ancient tech integration

    Returns:
        Status of all modules
    """
    return {
        "status": "healthy",
        "version": "370.0",
        "modules": {
            "ancient_technologies": {
                "total_technologies": len(ancient_db.technologies),
                "sacred_count": len(ancient_db.get_sacred_knowledge()),
                "avg_phi_resonance": ancient_db.get_statistics()['average_phi_resonance']
            },
            "biosensor_bridge": {
                "measurements_recorded": len(biosensor_bridge.measurement_history),
                "interventions_recorded": len(biosensor_bridge.intervention_history)
            },
            "workshops": {
                "total_sessions": len(workshops.sessions),
                "total_participants": workshops.next_participant_id - 1
            }
        },
        "timestamp": datetime.utcnow().isoformat(),
        "message": "LUCA 370 Ancient Tech Integration: Online ✅"
    }
