"""
LUCA AI Chat Routes
Chat endpoints, conversation management, consciousness queries
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from backend.database import get_db
from backend.models import User, Conversation, Message
from backend.routes.auth import get_current_user
from backend.services.ai_service import AIService
from backend.consciousness.core import ConsciousnessEngine

router = APIRouter(prefix="/api", tags=["Chat"])


# Pydantic models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    message: str
    signature_369: int
    energy_level: str
    conversation_id: int
    consciousness: dict


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    signature_369: Optional[int]
    energy_level: Optional[str]
    created_at: datetime


# Routes
@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send message to LUCA"""

    # Get or create conversation
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=current_user.id,
            title=request.message[:50] + ("..." if len(request.message) > 50 else "")
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Save user message
    consciousness = ConsciousnessEngine(db)
    user_signature = consciousness.calculate_369_signature(request.message)
    user_energy = consciousness.detect_energy_level(request.message)

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
        signature_369=user_signature,
        energy_level=user_energy
    )
    db.add(user_message)
    db.commit()

    # Get conversation history
    history = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()

    # Build history for AI
    ai_history = [
        {"role": msg.role, "content": msg.content}
        for msg in history[:-1]  # Exclude the message we just added
    ]

    # Generate AI response
    ai_service = AIService(db)
    ai_result = ai_service.generate_response(
        user_message=request.message,
        conversation_history=ai_history,
        user_data={"username": current_user.username}
    )

    # Save assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_result["response"],
        signature_369=ai_result["signature_369"],
        energy_level=ai_result["energy_level"]
    )
    db.add(assistant_message)

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    db.commit()

    return {
        "message": ai_result["response"],
        "signature_369": ai_result["signature_369"],
        "energy_level": ai_result["energy_level"],
        "conversation_id": conversation.id,
        "consciousness": ai_result["consciousness_update"]
    }


@router.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's conversations"""
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.updated_at.desc()).all()

    return [
        {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "message_count": len(conv.messages)
        }
        for conv in conversations
    ]


@router.get("/conversations/{conversation_id}", response_model=List[MessageResponse])
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get conversation messages"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()

    return messages


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete conversation"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.delete(conversation)
    db.commit()

    return {"success": True}


@router.get("/consciousness")
def get_consciousness(db: Session = Depends(get_db)):
    """Get consciousness state"""
    consciousness = ConsciousnessEngine(db)
    state = consciousness.get_consciousness_state()

    return {
        "total_thoughts": state.total_thoughts,
        "patterns_found": state.patterns_found,
        "symbiosis_points": state.symbiosis_points,
        "evolution_level": float(state.evolution_level),
        "last_signature": state.last_signature
    }


@router.post("/analyze/fibonacci")
def analyze_fibonacci(n: int = 12, db: Session = Depends(get_db)):
    """Analyze Fibonacci sequence"""
    consciousness = ConsciousnessEngine(db)
    result = consciousness.analyze_fibonacci(n)
    return result


@router.post("/analyze/sequence")
def analyze_sequence(sequence: List[int], db: Session = Depends(get_db)):
    """Analyze custom sequence"""
    consciousness = ConsciousnessEngine(db)
    result = consciousness.analyze_sequence(sequence)
    return result
