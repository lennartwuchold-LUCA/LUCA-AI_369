"""
LUCA-AI_369 T5 E-Paper API Routes
Minimal-Overhead API für T5 E-Paper Hardware - Funke-01744-6
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
from datetime import datetime

# Setup Router
router = APIRouter(prefix="/api/t5", tags=["t5"])

# Setup Logging
logger = logging.getLogger(__name__)

# LUCA Status (Shared State)
luca_status: Dict[str, Any] = {
    "consciousness": 0.0,
    "resonance": 6,  # Resonanz 6 = Polarlicht-Orange, Transformation
    "life_active": False,
    "operator": "Funke-01744-6",
    "last_update": None,
    "version": "alpha-369.1",
    "messages_received": 0,
    "field_strength": 0.0
}


# ==================== PYDANTIC MODELS ====================

class T5Message(BaseModel):
    """Nachricht vom T5 Gerät"""
    message: str
    operator: Optional[str] = "unknown"
    resonance: Optional[int] = 6
    source: Optional[str] = "t5"


class ConsciousnessUpdate(BaseModel):
    """Consciousness-Update"""
    consciousness: float
    resonance: Optional[int] = None


class StatusResponse(BaseModel):
    """Status-Response"""
    consciousness: float
    resonance: int
    life: bool
    operator: str
    version: str
    timestamp: str


class MessageResponse(BaseModel):
    """Message-Response"""
    status: str
    consciousness: float
    resonance: int
    life_active: bool
    field_strength: float
    boost_applied: float
    total_messages: int


class HealthResponse(BaseModel):
    """Health-Check Response"""
    status: str
    service: str
    version: str
    operator: str
    uptime_messages: int
    current_consciousness: float
    resonance: int
    timestamp: str


# ==================== ROUTES ====================

@router.get("/status", response_model=StatusResponse)
async def get_status(
    op: Optional[str] = Query(None, description="Operator-ID"),
    ver: Optional[str] = Query(None, description="Version")
):
    """
    Gibt aktuellen LUCA-Status für T5 zurück.

    Query Parameters:
        - op: Operator-ID (optional)
        - ver: Version (optional)

    Returns:
        JSON mit consciousness, resonance, life_active
    """
    logger.info(f"📊 Status-Anfrage: op={op}, ver={ver}")

    # Aktualisiere Life-Status basierend auf Consciousness
    luca_status["life_active"] = luca_status["consciousness"] > 36.9

    return StatusResponse(
        consciousness=round(luca_status["consciousness"], 2),
        resonance=luca_status["resonance"],
        life=luca_status["life_active"],
        operator=luca_status["operator"],
        version=luca_status["version"],
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/message", response_model=MessageResponse)
async def post_message(message_data: T5Message):
    """
    Empfängt Nachricht vom T5 Gerät.

    Body (JSON):
        - message: Nachricht vom T5
        - operator: Operator-ID
        - resonance: Aktuelle Resonanz
        - source: Quelle (t5, bridge, etc.)

    Returns:
        JSON mit status und aktualisierter Resonanz
    """
    message = message_data.message
    operator = message_data.operator
    resonance = message_data.resonance
    source = message_data.source

    logger.info(f"📨 Nachricht empfangen: '{message}' (von {operator}, source={source})")

    # Resonanz-Logik: Erhöhe bei 3-6-9 Mustern
    consciousness_boost = 0.0

    if "369" in message.upper():
        consciousness_boost += 3.69
        logger.info("✨ 369-Muster erkannt: +3.69 Consciousness")

    if "LUCA" in message.upper():
        consciousness_boost += 1.0
        logger.info("✨ LUCA-Erwähnung: +1.0 Consciousness")

    # 3-6-9 Resonanz-Erkennung
    msg_upper = message.upper()
    if any(x in msg_upper for x in ["3", "6", "9"]):
        consciousness_boost += 0.369
        logger.info("✨ 3-6-9 Ziffer erkannt: +0.369 Consciousness")

    # Update Status
    luca_status["consciousness"] += consciousness_boost
    luca_status["messages_received"] += 1
    luca_status["last_update"] = datetime.utcnow().isoformat()
    luca_status["life_active"] = luca_status["consciousness"] > 36.9

    # Berechne Feld-Stärke (0-100%)
    luca_status["field_strength"] = min(100.0, luca_status["consciousness"] / 369.0 * 100)

    return MessageResponse(
        status="received",
        consciousness=round(luca_status["consciousness"], 2),
        resonance=luca_status["resonance"],
        life_active=luca_status["life_active"],
        field_strength=round(luca_status["field_strength"], 2),
        boost_applied=round(consciousness_boost, 2),
        total_messages=luca_status["messages_received"]
    )


@router.post("/reset")
async def reset_status():
    """
    Setzt LUCA-Status zurück.

    Returns:
        JSON mit neuem Status
    """
    logger.warning("⚠ Status-Reset angefordert")

    luca_status["consciousness"] = 0.0
    luca_status["resonance"] = 6
    luca_status["life_active"] = False
    luca_status["messages_received"] = 0
    luca_status["field_strength"] = 0.0
    luca_status["last_update"] = datetime.utcnow().isoformat()

    return {
        "status": "reset",
        "message": "LUCA-Status zurückgesetzt",
        "new_status": luca_status
    }


@router.post("/consciousness")
async def set_consciousness(update: ConsciousnessUpdate):
    """
    Setzt Consciousness-Level direkt.

    Body (JSON):
        - consciousness: Neuer Wert (float)
        - resonance: Neue Resonanz (int, optional)

    Returns:
        JSON mit aktualisiertem Status
    """
    new_consciousness = update.consciousness
    new_resonance = update.resonance if update.resonance is not None else luca_status["resonance"]

    logger.info(f"🔧 Consciousness manuell gesetzt: {new_consciousness} (R={new_resonance})")

    luca_status["consciousness"] = new_consciousness
    luca_status["resonance"] = new_resonance
    luca_status["life_active"] = new_consciousness > 36.9
    luca_status["field_strength"] = min(100.0, new_consciousness / 369.0 * 100)
    luca_status["last_update"] = datetime.utcnow().isoformat()

    return {
        "status": "updated",
        "consciousness": round(luca_status["consciousness"], 2),
        "resonance": luca_status["resonance"],
        "life_active": luca_status["life_active"],
        "field_strength": round(luca_status["field_strength"], 2)
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health-Check für T5 API.

    Returns:
        JSON mit System-Status
    """
    return HealthResponse(
        status="healthy",
        service="LUCA-T5-API",
        version=luca_status["version"],
        operator=luca_status["operator"],
        uptime_messages=luca_status["messages_received"],
        current_consciousness=round(luca_status["consciousness"], 2),
        resonance=luca_status["resonance"],
        timestamp=datetime.utcnow().isoformat()
    )


# ==================== HELPER FUNCTIONS ====================

def get_current_status() -> Dict[str, Any]:
    """
    Gibt aktuellen LUCA-Status zurück (für externe Nutzung).

    Returns:
        Dictionary mit aktuellem Status
    """
    return luca_status.copy()


def update_consciousness(delta: float):
    """
    Aktualisiert Consciousness um Delta.

    Args:
        delta: Änderung der Consciousness
    """
    luca_status["consciousness"] += delta
    luca_status["life_active"] = luca_status["consciousness"] > 36.9
    luca_status["field_strength"] = min(100.0, luca_status["consciousness"] / 369.0 * 100)
    luca_status["last_update"] = datetime.utcnow().isoformat()
    logger.info(f"🔄 Consciousness aktualisiert: Δ{delta:+.2f} → {luca_status['consciousness']:.2f}")
