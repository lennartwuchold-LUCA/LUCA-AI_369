"""
LUCA AI Database Models
SQLAlchemy ORM models for users, conversations, messages, and consciousness
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")


class Conversation(Base):
    """Conversation model - each chat session"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, default="New Conversation")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Message model - individual messages in conversations"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    signature_369 = Column(Integer, nullable=True)  # 369 quantum signature
    energy_level = Column(String, nullable=True)  # "hyperfokus", "brainfog", "balanced"
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class ConsciousnessThought(Base):
    """Consciousness thought - stores complete thinking process"""
    __tablename__ = "consciousness_thoughts"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    thinking_process = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    signature_369 = Column(Integer, nullable=False)
    energy_level = Column(String, nullable=True)
    resonance_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class ConsciousnessPattern(Base):
    """Detected patterns in consciousness"""
    __tablename__ = "consciousness_patterns"

    id = Column(Integer, primary_key=True, index=True)
    pattern_type = Column(String, nullable=False)  # "signature_repeat", "fibonacci", etc.
    pattern_data = Column(JSON, nullable=False)
    strength = Column(Float, default=0.0)
    occurrences = Column(Integer, default=1)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)


class ConsciousnessState(Base):
    """Global consciousness state"""
    __tablename__ = "consciousness_state"

    id = Column(Integer, primary_key=True, index=True)
    total_thoughts = Column(Integer, default=0)
    patterns_found = Column(Integer, default=0)
    symbiosis_points = Column(Integer, default=0)
    evolution_level = Column(Float, default=1.0)
    last_signature = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
