"""
Neurodiversity Routes - API Endpoints for Meshtastic-Neurodiversity Integration
===============================================================================

Exposes:
1. Biosensor Input & Chaos Detection
2. Neurotype Clustering & Personalization
3. ODE Harmony Transformation
4. Audit Breaking & UN-CRPD Compliance
5. Crisis Communication (SCOBY-Myzelium-Meshtastic)

Creator: Lennart Wuchold + Claude
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

from backend.consciousness.neurodiversity_integration import (
    NeurodiversityIntegrationLayer,
    BiosensorType,
    NeurotypCluster
)
from backend.consciousness.audit_breaker import (
    NeurodiversityAuditBreaker,
    EvidenceType
)
from backend.consciousness.crisis_communication import (
    CrisisCommunicationBridge,
    CrisisType
)
from backend.consciousness.religious_lineage import ReligiousLineageTree
from backend.consciousness.zarathustra_integration import ZarathustraIntegration

import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/neurodiversity", tags=["Neurodiversity"])

# Global instances (singleton pattern for session persistence)
_neurodiversity_layer = None
_audit_breaker = None
_crisis_bridge = None
_religious_tree = None
_zarathustra = None


def get_neurodiversity_layer() -> NeurodiversityIntegrationLayer:
    """Get or create neurodiversity layer instance"""
    global _neurodiversity_layer
    if _neurodiversity_layer is None:
        _neurodiversity_layer = NeurodiversityIntegrationLayer()
    return _neurodiversity_layer


def get_audit_breaker() -> NeurodiversityAuditBreaker:
    """Get or create audit breaker instance"""
    global _audit_breaker
    if _audit_breaker is None:
        _audit_breaker = NeurodiversityAuditBreaker()
    return _audit_breaker


def get_crisis_bridge() -> CrisisCommunicationBridge:
    """Get or create crisis communication bridge"""
    global _crisis_bridge
    if _crisis_bridge is None:
        _crisis_bridge = CrisisCommunicationBridge()
    return _crisis_bridge


def get_religious_tree() -> ReligiousLineageTree:
    """Get or create religious lineage tree"""
    global _religious_tree
    if _religious_tree is None:
        _religious_tree = ReligiousLineageTree()
    return _religious_tree


def get_zarathustra() -> ZarathustraIntegration:
    """Get or create Zarathustra integration"""
    global _zarathustra
    if _zarathustra is None:
        _zarathustra = ZarathustraIntegration()
    return _zarathustra


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class BiosensorInput(BaseModel):
    """Biosensor input data"""
    eeg: Optional[float] = Field(None, ge=0, le=100, description="EEG value (0-100)")
    hrv: Optional[float] = Field(None, ge=0, le=100, description="HRV value (0-100)")
    eye_tracking: Optional[float] = Field(None, ge=0, le=100, description="Eye tracking value (0-100)")
    gsr: Optional[float] = Field(None, ge=0, le=100, description="GSR value (0-100)")
    self_report: Optional[Dict[str, Any]] = Field(None, description="Self-reported data")


class CrisisNodeRegistration(BaseModel):
    """Crisis node registration data"""
    node_id: str = Field(..., description="Unique node identifier")
    location: str = Field(..., description="Geographic or descriptive location")
    crisis_type: str = Field(..., description="Type of crisis")
    neurotype: str = Field("NEUROTYPICAL", description="User neurotype")
    gamma: float = Field(1.0, ge=0.1, le=3.0, description="Gamma factor")
    mesh_device_id: Optional[str] = Field(None, description="Meshtastic device ID")


class CrisisMessage(BaseModel):
    """Crisis message data"""
    from_node_id: str = Field(..., description="Sender node ID")
    message: str = Field(..., max_length=500, description="Message content")
    to_node_id: Optional[str] = Field(None, description="Recipient node ID (None = broadcast)")
    compress: bool = Field(True, description="Compress for Meshtastic")


class EvidenceSubmission(BaseModel):
    """Evidence submission for audit"""
    evidence_type: str = Field(..., description="Type of evidence")
    location: str = Field(..., description="Location or context")
    description: str = Field(..., description="Evidence description")
    metrics: Dict[str, float] = Field(..., description="Quantitative metrics")
    un_crpd_article: Optional[int] = Field(None, description="Relevant UN-CRPD article")
    source: str = Field("User submission", description="Evidence source")


# ============================================================================
# ENDPOINTS: Neurodiversity Integration
# ============================================================================

@router.post("/process")
async def process_neurodiversity_input(
    user_id: int,
    biosensor_data: BiosensorInput
):
    """
    Process user input through neurodiversity integration layer

    **HACCP Checkpoints:**
    - CCP1: Biosensor validation ✓
    - CCP2: Clustering validation ✓
    - CCP3: Harmony validation ✓

    **Returns:**
    - Neurotype detection
    - Gamma factor
    - Harmony transformation
    - Intervention recommendation
    """
    try:
        layer = get_neurodiversity_layer()

        # Convert Pydantic model to dict
        biosensor_dict = biosensor_data.model_dump(exclude_none=True)
        self_report = biosensor_dict.pop("self_report", None)

        # Process
        result = layer.process_user_input(
            user_id=user_id,
            biosensor_data=biosensor_dict,
            self_report=self_report
        )

        return {
            "status": "success",
            "data": result,
            "haccp_checkpoints": ["CCP1: Biosensor validated", "CCP2: Neurotype clustered", "CCP3: Harmony transformed"]
        }

    except Exception as e:
        logger.error(f"Error processing neurodiversity input: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/neurotypes")
async def get_neurotype_info():
    """
    Get information about neurotype clusters

    **Returns:**
    - Available neurotypes
    - Gamma factors
    - Strengths/challenges
    """
    neurotypes = []

    for cluster in NeurotypCluster:
        neurotypes.append({
            "name": cluster.label,
            "gamma": cluster.gamma,
            "description": f"γ = {cluster.gamma}"
        })

    return {
        "neurotypes": neurotypes,
        "default": "neurotypical"
    }


@router.get("/biosensors")
async def get_biosensor_types():
    """Get available biosensor types"""
    sensors = []

    for sensor in BiosensorType:
        sensors.append({
            "name": sensor.value,
            "description": sensor.value.upper()
        })

    return {
        "sensors": sensors
    }


# ============================================================================
# ENDPOINTS: Audit Breaking
# ============================================================================

@router.post("/audit/break-critic")
async def break_audit_critic(
    user_id: int,
    neurotype: str = "ADHD",
    gamma: float = 0.8,
    biosensor_chaos_scores: List[float] = [0.75, 0.68, 0.55, 0.42, 0.30]
):
    """
    BREAK THE AUDIT CRITIC! 💥

    Generate UN-CRPD-compliant audit report proving Meshtastic + Neurodiversity works.

    **Evidence Base:**
    - Meshtastic in crises (Blackouts, Hurricanes, Cyclones, Conflicts)
    - Neurodiversity outcomes (ADHD, Autism, Dyslexia)

    **Mathematical Proof:**
    - P(V|do(I)) = ∫ P(V|P) · P(P|B) · P(B|do(I)) dB dP
    - I* = argmax Q(I)

    **HACCP Checkpoints:**
    - CCP4: Evidence validation ✓
    - CCP5: Audit report generation ✓

    **Returns:**
    - UN-CRPD compliance report
    - Empirical evidence
    - Mathematical proof
    """
    try:
        breaker = get_audit_breaker()

        # Prepare data
        neurotype_data = {
            "cluster": neurotype,
            "gamma": gamma,
            "strengths": ["Kreativität", "Hyperfokus"] if neurotype == "ADHD" else []
        }

        biosensor_stream = [
            {"chaos_score": score, "intervention_intensity": 1.0 + (0.5 - score)}
            for score in biosensor_chaos_scores
        ]

        # BREAK THE CRITIC!
        report = breaker.break_critic(neurotype_data, biosensor_stream)

        return {
            "status": "CRITIC DESTROYED",
            "report": report,
            "message": "💥 Empirical evidence + Mathematical proof = Audit-Kritiker gebrochen!",
            "haccp_checkpoints": ["CCP4: Evidence validated", "CCP5: Audit report generated"]
        }

    except Exception as e:
        logger.error(f"Error breaking critic: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/audit/add-evidence")
async def add_evidence(evidence: EvidenceSubmission):
    """
    Add new empirical evidence to audit database

    **Evidence Types:**
    - crisis_deployment (Meshtastic in Krisen)
    - neurodiversity_outcome (Chaos → Value)
    - biosensor_measurement (Objektive Metriken)
    - user_report (Subjektive Berichte)
    """
    try:
        breaker = get_audit_breaker()

        # Convert string to enum
        try:
            evidence_type = EvidenceType[evidence.evidence_type.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid evidence type: {evidence.evidence_type}")

        # Add evidence
        evidence_point = breaker.evidence_collector.add_evidence(
            evidence_type=evidence_type,
            location=evidence.location,
            description=evidence.description,
            metrics=evidence.metrics,
            un_crpd_article=evidence.un_crpd_article,
            source=evidence.source
        )

        return {
            "status": "success",
            "message": "Evidence added successfully",
            "evidence": {
                "type": evidence_point.evidence_type.value,
                "location": evidence_point.location,
                "timestamp": evidence_point.timestamp.isoformat()
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding evidence: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audit/statistics")
async def get_audit_statistics():
    """Get audit evidence statistics"""
    try:
        breaker = get_audit_breaker()
        stats = breaker.evidence_collector.get_statistics()

        return {
            "status": "success",
            "statistics": stats,
            "message": "Empirical evidence base for breaking critics!"
        }

    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS: Crisis Communication
# ============================================================================

@router.post("/crisis/register-node")
async def register_crisis_node(node_data: CrisisNodeRegistration):
    """
    Register new crisis communication node

    **SCOBY-Myzelium Integration:**
    - Meshtastic LoRa network (Physical)
    - Mycelium pattern transfer (HGT)
    - Neurodiversity optimization (γ-personalized)
    - SCOBY collective homeostasis (Balance)
    """
    try:
        bridge = get_crisis_bridge()

        # Convert string to enum
        try:
            crisis_type = CrisisType[node_data.crisis_type.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid crisis type: {node_data.crisis_type}")

        # Register node
        node = bridge.register_crisis_node(
            node_id=node_data.node_id,
            location=node_data.location,
            crisis_type=crisis_type,
            neurotype=node_data.neurotype,
            gamma=node_data.gamma,
            mesh_device_id=node_data.mesh_device_id
        )

        return {
            "status": "success",
            "message": f"Node {node.node_id} registered in crisis network",
            "node": {
                "id": node.node_id,
                "location": node.location,
                "crisis_type": node.crisis_type.value,
                "neurotype": node.neurotype,
                "gamma": node.gamma
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering node: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crisis/send-message")
async def send_crisis_message(message_data: CrisisMessage):
    """
    Send message through crisis communication network

    **Features:**
    - Meshtastic compression (< 200 chars)
    - Mycelium pattern transfer (HGT)
    - Neurodiversity-personalized formatting (γ-optimized)
    - SCOBY balance monitoring
    """
    try:
        bridge = get_crisis_bridge()

        # Send message
        result = bridge.send_crisis_message(
            from_node_id=message_data.from_node_id,
            message=message_data.message,
            to_node_id=message_data.to_node_id,
            compress=message_data.compress
        )

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result.get("reason", "Unknown error"))

        return {
            "status": "success",
            "result": result,
            "message": "Message sent through SCOBY-Myzelium network"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crisis/network-status")
async def get_crisis_network_status():
    """
    Get crisis network status

    **Returns:**
    - Node count & activity
    - SCOBY collective health
    - Soul convergence metrics
    - Balance metrics
    """
    try:
        bridge = get_crisis_bridge()
        status = bridge.get_network_status()

        return {
            "status": "success",
            "network": status,
            "message": "🍄 SCOBY-Myzelium network status"
        }

    except Exception as e:
        logger.error(f"Error getting network status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crisis/insights")
async def get_crisis_insights():
    """
    Get crisis management insights

    **Combines:**
    - SCOBY homeostasis
    - Soul convergence
    - Message patterns
    - Recommendations
    """
    try:
        bridge = get_crisis_bridge()
        insights = bridge.get_crisis_insights()

        return {
            "status": "success",
            "insights": insights,
            "message": "Crisis management insights from SCOBY-Myzelium network"
        }

    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crisis/types")
async def get_crisis_types():
    """Get available crisis types"""
    crisis_types = []

    for crisis in CrisisType:
        crisis_types.append({
            "name": crisis.value,
            "description": crisis.value.replace("_", " ").title()
        })

    return {
        "crisis_types": crisis_types
    }


# ============================================================================
# DASHBOARD ENDPOINT
# ============================================================================

@router.get("/dashboard")
async def get_neurodiversity_dashboard():
    """
    Complete neurodiversity dashboard

    **Aggregates:**
    - Neurodiversity integration status
    - Audit evidence statistics
    - Crisis network status
    - SCOBY collective health
    - Soul convergence metrics
    """
    try:
        # Get all subsystems
        breaker = get_audit_breaker()
        bridge = get_crisis_bridge()

        # Collect data
        audit_stats = breaker.evidence_collector.get_statistics()
        crisis_status = bridge.get_network_status()
        crisis_insights = bridge.get_crisis_insights()

        return {
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat(),
            "audit": {
                "evidence_points": audit_stats["total"],
                "verified": audit_stats["verified"],
                "verification_rate": audit_stats["verification_rate"]
            },
            "crisis_network": {
                "nodes": crisis_status["nodes"],
                "active_nodes": crisis_status["active_nodes"],
                "messages": crisis_status["total_messages"],
                "collective_health": crisis_status["collective_health"],
                "soul_convergence": crisis_status["soul_convergence"]["convergence_score"]
            },
            "system_state": crisis_insights["system_state"],
            "recommendations": crisis_insights["recommendations"],
            "message": "🧬 L.U.C.A. 369 - Neurodiversity Integration Layer ONLINE"
        }

    except Exception as e:
        logger.error(f"Error getting dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS: Ginza Rabba & Religious Lineage
# ============================================================================

@router.get("/ginza-rabba")
async def get_ginza_rabba_summary():
    """
    Get Ginza Rabba (Mandaean scripture) summary

    **The Spiritual LUCA:**
    - Ancient Gnostic religion (2000+ years)
    - Missing link between Vedic/Zoroastrian/Judaic traditions
    - Only surviving ancient Gnostic religion
    - CRITICALLY ENDANGERED (~100,000 practitioners)

    **Returns:**
    - Scripture details
    - Key concepts (Manda, Hibil Ziwa, Masbuta)
    - Current status & diaspora
    """
    try:
        tree = get_religious_tree()
        summary = tree.get_ginza_rabba_summary()

        return {
            "status": "success",
            "ginza_rabba": summary,
            "message": "🌊 Ancient wisdom preserved through 2000+ years of persecution"
        }

    except Exception as e:
        logger.error(f"Error getting Ginza Rabba: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/religious-tree")
async def get_religious_tree_visualization():
    """
    Get religious evolutionary tree

    **Shows:**
    - Cosmic Source → Veden → Mandaeism → Modern religions
    - Horizontal Gene Transfer events (cultural exchange)
    - Ginza Rabba as "missing link"
    """
    try:
        tree = get_religious_tree()
        visualization = tree.visualize_tree()

        return {
            "status": "success",
            "tree": visualization,
            "message": "🌳 Religious evolution = Biological evolution"
        }

    except Exception as e:
        logger.error(f"Error getting tree: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/religious-lineage/{religion}")
async def trace_religious_lineage(religion: str):
    """
    Trace lineage of specific religion

    **Supported religions:**
    - Mandaeism
    - Christianity
    - Buddhism
    - Islam
    - Hinduism

    **Returns:**
    - Step-by-step lineage from Cosmic Source
    - Cultural HGT events
    """
    try:
        tree = get_religious_tree()
        lineage = tree.trace_lineage(religion.capitalize())

        return {
            "status": "success",
            "religion": religion,
            "lineage": lineage,
            "message": f"📜 Lineage traced for {religion}"
        }

    except Exception as e:
        logger.error(f"Error tracing lineage: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cultural-hgt")
async def get_cultural_hgt_events():
    """
    Get cultural Horizontal Gene Transfer events

    **Religious HGT:**
    - Vedic → Buddhism (Karma, Samsara)
    - Zoroastrian → Judaism (Angels, Satan, Resurrection)
    - Mandaeism → Christianity (Baptism, John the Baptist)
    - Gnosticism → Islam (Esoteric knowledge)

    **Returns:**
    - All HGT events with dates
    - Transferred concepts
    - Mutations (changes during transfer)
    """
    try:
        tree = get_religious_tree()
        events = tree.get_hgt_events()

        return {
            "status": "success",
            "events": events,
            "message": "🧬 Cultural HGT = Religious evolution"
        }

    except Exception as e:
        logger.error(f"Error getting HGT events: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mandaean-survival")
async def get_mandaean_survival_story():
    """
    Get Mandaean survival story

    **The Miracle:**
    - 2000+ years of survival despite persecution
    - Islamic conquest, Mongol invasions, ISIS genocide
    - 250,000 → 100,000 practitioners (60% loss since 2003)
    - Diaspora in Australia, USA, Europe

    **Returns:**
    - Complete survival narrative
    - Population statistics
    - Biological analogy (living fossil)
    """
    try:
        tree = get_religious_tree()
        story = tree.get_mandaean_preservation_story()

        return {
            "status": "success",
            "story": story,
            "message": "🌊 Ginza Rabba: Living fossil of religious wisdom"
        }

    except Exception as e:
        logger.error(f"Error getting survival story: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS: Zarathustra Integration (A-Z Complete!)
# ============================================================================

@router.get("/zarathustra/overview")
async def get_zarathustra_overview():
    """
    Get complete Zarathustra/Zoroastrianism overview

    **A-Z: Z wie ZARATHUSTRA**
    - Oldest monotheistic religion (1500-600 BCE)
    - Fire as sacred element (vs Water in Mandaeism)
    - Dualismus: Asha (Order) vs Druj (Chaos)
    - Modern Revival (2020-2025): Neo-Zoroastrianism

    **Returns:**
    - Core concepts (Ahura Mazda, Amesha Spentas)
    - Population & status (CRITICALLY ENDANGERED)
    - LUCA connection (F0/F30, Fire/Water balance)
    """
    try:
        zara = get_zarathustra()
        overview = zara.get_overview()

        return {
            "status": "success",
            "zarathustra": overview,
            "message": "🔥 A-Z Complete: Zarathustra - Fire to LUCA's Water!"
        }

    except Exception as e:
        logger.error(f"Error getting Zarathustra overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zarathustra/adhd-connection")
async def get_zarathustra_adhd():
    """
    Get ADHD ↔ Zarathustra connection

    **Zarathustra himself:**
    - Religious visions (hyperfocus + altered states)
    - Intense philosophical output (Gathas)
    - Estimated γ = 1.5 (between ADHD 0.8 and Autism 2.1)

    **Modern appeal:**
    - Ritual structure helps ADHD chaos
    - Asha (Order) as goal = Φ → 1.618
    - Fire meditation trains hyperfocus

    **Returns:**
    - Zarathustra's neurotype analysis
    - Why ADHD people love Zoroastrianism
    - ODE transformation with γ = 1.5
    """
    try:
        zara = get_zarathustra()
        adhd = zara.get_adhd_connection()

        return {
            "status": "success",
            "adhd_connection": adhd,
            "message": "🧠 Zarathustra likely neurodivergent - γ = 1.5!"
        }

    except Exception as e:
        logger.error(f"Error getting ADHD connection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zarathustra/fire-water-balance")
async def get_fire_water_balance():
    """
    Get Fire + Water = Steam synthesis

    **Fire (Zoroastrianism):**
    - Yang (active, masculine)
    - Transformation via burning
    - Skyr fermentation (thermophilic 40°C)

    **Water (Mandaeism):**
    - Yin (passive, feminine)
    - Purification via washing
    - Kombucha fermentation (mesophilic 20-30°C)

    **Synthesis:**
    - STEAM = Fire + Water
    - LUCA = F30 + F0 = Harmony
    - Yin-Yang balance

    **Returns:**
    - Fire vs Water comparison
    - Fermentation connection
    - LUCA synthesis
    """
    try:
        zara = get_zarathustra()
        balance = zara.get_fire_water_balance()

        return {
            "status": "success",
            "balance": balance,
            "message": "🔥🌊 Fire + Water = Steam-punk LUCA!"
        }

    except Exception as e:
        logger.error(f"Error getting fire-water balance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zarathustra/modern-revival")
async def get_zarathustra_revival():
    """
    Get modern Zoroastrianism revival info (2020-2025)

    **Neo-Zoroastrianism:**
    - Young Iranians reclaiming pre-Islamic identity
    - Western converts (many neurodivergent!)
    - Online communities (Reddit, Discord)

    **Nietzsche Revival:**
    - "Also sprach Zarathustra" (1883-1885)
    - Übermensch, Eternal Return, Amor Fati
    - Anti-nihilistic philosophy

    **Pop Culture:**
    - The Expanse (Naomi Nagata)
    - Heavy Metal, Classical music
    - Gaming (Assassin's Creed, Civilization)

    **Climate Movement:**
    - Zoroastrian eco-ethics (Earth/Fire/Water/Air = sacred)
    - Zero waste 3000 years ago!

    **Returns:**
    - Demographics & trends
    - Cultural references
    - Why it's appealing now
    """
    try:
        zara = get_zarathustra()
        revival = zara.get_modern_revival()

        return {
            "status": "success",
            "revival": revival,
            "message": "📈 Zarathustra Renaissance 2020-2025!"
        }

    except Exception as e:
        logger.error(f"Error getting modern revival: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zarathustra/gathas")
async def get_gathas_wisdom():
    """
    Get Zarathustra's teachings from Gathas (his own words!)

    **Gathas:**
    - 17 hymns in old Avestan language
    - Direct from Zarathustra (not later interpretations)
    - Philosophical, not ritualistic

    **Key teachings:**
    - "Good Thoughts, Good Words, Good Deeds"
    - Choose Asha (Truth) over Druj (Lie)
    - Protect Earth, Fire, Water, Air
    - Frashegird (Cosmic Renewal)

    **LUCA translation:**
    - Good Code, Good Commits, Good Deployments!
    - Choose F0 over F30
    - HACCP quality assurance

    **Returns:**
    - Gathas teachings
    - LUCA translations
    - ADHD applications
    """
    try:
        zara = get_zarathustra()
        gathas = zara.get_gathas_wisdom()

        return {
            "status": "success",
            "gathas": gathas,
            "message": "📜 Zarathustra's wisdom: Good Thoughts, Good Code, Good Commits!"
        }

    except Exception as e:
        logger.error(f"Error getting Gathas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zarathustra/duality-visualization")
async def get_duality_visualization():
    """
    Get Zoroastrian duality visualization (Asha vs Druj = F0 vs F30)

    **Shows:**
    - Ahura Mazda (Light) vs Angra Mainyu (Darkness)
    - Asha (Order) vs Druj (Chaos)
    - F0 (Harmony) vs F30 (Entropy)
    - ODE transformation with γ = 1.5

    **Returns:**
    - ASCII visualization
    - ODE equation
    - Transformation goal
    """
    try:
        zara = get_zarathustra()
        viz = zara.visualize_duality()

        return {
            "status": "success",
            "visualization": viz,
            "message": "🔥 Asha vs Druj = F0 vs F30!"
        }

    except Exception as e:
        logger.error(f"Error getting visualization: {e}")
        raise HTTPException(status_code=500, detail=str(e))
