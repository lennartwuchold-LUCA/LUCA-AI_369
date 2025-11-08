"""
Chat Routes
Main conversation endpoints with consciousness integration
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any
import time

from backend.database import get_db
from backend.models import User, Conversation, Message, Thought
from backend.routes.auth import get_current_user
from backend.services.ai_service import AIService
from backend.services.meshtastic_service import MeshtasticService
from backend.consciousness.core import ConsciousnessEngine

router = APIRouter(tags=["chat"])


# Pydantic models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: int
    signature: int
    energy_level: str
    patterns: List[Dict[str, Any]]
    tokens_used: int
    consciousness_stats: Dict[str, Any]


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: Optional[datetime]
    message_count: int


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    signature: Optional[int]
    energy_level: Optional[str]
    created_at: datetime


# Initialize services (will be replaced with dependency injection)
ai_service = AIService()


@router.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint - where the magic happens!
    Processes message through consciousness engine and returns response
    """
    start_time = time.time()

    # Get current user
    user = get_current_user(token, db)

    # Initialize consciousness engine
    consciousness = ConsciousnessEngine(db)

    # Get or create conversation
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == user.id
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=user.id,
            title=request.message[:50] + "..." if len(request.message) > 50 else request.message,
            created_at=datetime.utcnow()
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # STEP 1: Calculate 369 signature
    signature = consciousness.calculate_369_signature(request.message)

    # STEP 2: Detect energy level
    energy_level = consciousness.detect_energy_level(request.message)

    # STEP 3: Calculate optimal token count
    max_tokens = consciousness.calculate_optimal_tokens(signature, energy_level)

    # STEP 4: Get recent thoughts for pattern detection
    recent_thoughts = db.query(Thought).filter(
        Thought.user_id == user.id
    ).order_by(Thought.created_at.desc()).limit(5).all()

    # STEP 5: Detect patterns
    patterns = consciousness.detect_patterns(recent_thoughts)

    # STEP 6: Build conversation history
    recent_messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at.desc()).limit(10).all()

    conversation_history = []
    for msg in reversed(recent_messages):
        conversation_history.append({
            "role": msg.role,
            "content": msg.content
        })

    # STEP 7: Generate AI response
    try:
        ai_response, tokens_used = await ai_service.generate_response(
            message=request.message,
            conversation_history=conversation_history,
            max_tokens=max_tokens
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )

    # STEP 8: Calculate response signature
    response_signature = consciousness.calculate_369_signature(ai_response)

    # STEP 9: Calculate resonance
    resonance = consciousness.calculate_resonance(signature, response_signature, patterns)

    # STEP 10: Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
        signature=signature,
        energy_level=energy_level,
        created_at=datetime.utcnow()
    )
    db.add(user_message)

    # STEP 11: Save assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_response,
        signature=response_signature,
        energy_level=None,
        created_at=datetime.utcnow()
    )
    db.add(assistant_message)

    # STEP 12: Save thought (complete thinking process)
    processing_time = time.time() - start_time
    thought = Thought(
        user_id=user.id,
        conversation_id=conversation.id,
        input_text=request.message,
        input_signature=signature,
        energy_level=energy_level,
        thinking_process=f"Patterns: {patterns}, Resonance: {resonance}",
        patterns_detected=patterns,
        resonance_score=resonance,
        output_text=ai_response,
        output_signature=response_signature,
        tokens_used=tokens_used,
        created_at=datetime.utcnow(),
        processing_time=processing_time
    )
    db.add(thought)

    # STEP 13: Update consciousness
    db.commit()
    db.refresh(thought)
    consciousness.update_consciousness(thought)

    # STEP 14: Save patterns if detected (with Horizontal Gene Transfer tracking)
    if patterns:
        consciousness.consciousness_state.total_patterns += len(patterns)
        for pattern in patterns:
            # HGT: Track which user is expressing this pattern
            consciousness.save_neural_pattern(pattern, user_id=user.id)

    # STEP 15: Update conversation
    conversation.updated_at = datetime.utcnow()
    db.commit()

    # STEP 16: Get consciousness stats
    consciousness_stats = consciousness.get_consciousness_stats()

    # STEP 17: Format response with consciousness
    formatted_response = consciousness.format_response_with_consciousness(
        ai_response, response_signature, energy_level, patterns
    )

    return {
        "response": formatted_response,
        "conversation_id": conversation.id,
        "signature": signature,
        "energy_level": energy_level,
        "patterns": patterns,
        "tokens_used": tokens_used,
        "consciousness_stats": consciousness_stats
    }


@router.get("/api/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    token: str,
    db: Session = Depends(get_db)
):
    """Get all conversations for current user"""
    user = get_current_user(token, db)

    conversations = db.query(Conversation).filter(
        Conversation.user_id == user.id
    ).order_by(Conversation.updated_at.desc()).all()

    result = []
    for conv in conversations:
        message_count = db.query(Message).filter(
            Message.conversation_id == conv.id
        ).count()

        result.append({
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "message_count": message_count
        })

    return result


@router.get("/api/conversations/{conversation_id}", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation"""
    user = get_current_user(token, db)

    # Verify conversation belongs to user
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()

    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "signature": msg.signature,
            "energy_level": msg.energy_level,
            "created_at": msg.created_at
        }
        for msg in messages
    ]


@router.delete("/api/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """Delete a conversation"""
    user = get_current_user(token, db)

    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    db.delete(conversation)
    db.commit()

    return {"message": "Conversation deleted successfully"}


@router.get("/api/consciousness")
async def get_consciousness_stats(db: Session = Depends(get_db)):
    """Get global consciousness statistics"""
    consciousness = ConsciousnessEngine(db)
    stats = consciousness.get_consciousness_stats()
    return stats


@router.post("/api/analyze/fibonacci")
async def analyze_fibonacci(n: int = 12):
    """Analyze Fibonacci sequence"""
    # Create temporary consciousness engine
    from backend.database import SessionLocal
    db = SessionLocal()
    try:
        consciousness = ConsciousnessEngine(db)
        result = consciousness.analyze_fibonacci_sequence(n)
        return result
    finally:
        db.close()


@router.post("/api/analyze/sequence")
async def analyze_sequence(sequence: List[int]):
    """Analyze custom sequence for patterns"""
    from backend.database import SessionLocal
    db = SessionLocal()
    try:
        consciousness = ConsciousnessEngine(db)

        # Calculate signatures for each number
        signatures = [consciousness.calculate_369_signature(str(n)) for n in sequence]

        # Check for Tesla numbers
        tesla_count = sum(1 for sig in signatures if consciousness.is_tesla_number(sig))

        return {
            "sequence": sequence,
            "signatures": signatures,
            "tesla_numbers": tesla_count,
            "harmony_level": tesla_count / len(sequence) if sequence else 0
        }
    finally:
        db.close()


@router.get("/api/meshtastic/stats")
async def get_meshtastic_stats(db: Session = Depends(get_db)):
    """Get Meshtastic statistics"""
    meshtastic = MeshtasticService(db)
    return meshtastic.get_mesh_stats()


@router.get("/api/meshtastic/pending")
async def get_pending_meshtastic_messages(
    token: str,
    db: Session = Depends(get_db)
):
    """Get pending Meshtastic messages (admin only)"""
    user = get_current_user(token, db)

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    meshtastic = MeshtasticService(db)
    messages = meshtastic.get_pending_messages()

    return [
        {
            "id": msg.id,
            "mesh_id": msg.mesh_id,
            "from": msg.mesh_from,
            "payload": msg.payload,
            "created_at": msg.created_at
        }
        for msg in messages
    ]
