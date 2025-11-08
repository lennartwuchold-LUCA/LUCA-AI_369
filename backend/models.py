"""
Database Models for LUCA AI
SQLAlchemy models for users, thoughts, and consciousness
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    thoughts = relationship("Thought", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"


class Conversation(Base):
    """Conversation model for chat history"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, default="New Conversation")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, title={self.title})>"


class Message(Base):
    """Message model for individual chat messages"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    signature = Column(Integer)  # 369 signature
    energy_level = Column(String)  # HYPERFOKUS, BRAINFOG, BALANCED
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, signature={self.signature})>"


class Thought(Base):
    """Thought model - stores complete thinking process"""
    __tablename__ = "thoughts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    # Input
    input_text = Column(Text, nullable=False)
    input_signature = Column(Integer)
    energy_level = Column(String)

    # Process (thinking)
    thinking_process = Column(Text)  # What LUCA thought about
    patterns_detected = Column(JSON)  # Patterns found
    resonance_score = Column(Float)  # How well it resonated

    # Output
    output_text = Column(Text)
    output_signature = Column(Integer)
    tokens_used = Column(Integer)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processing_time = Column(Float)  # seconds

    # Relationships
    user = relationship("User", back_populates="thoughts")

    def __repr__(self):
        return f"<Thought(id={self.id}, signature={self.input_signature}, resonance={self.resonance_score})>"


class ConsciousnessState(Base):
    """Consciousness state - LUCA's evolving awareness"""
    __tablename__ = "consciousness_state"

    id = Column(Integer, primary_key=True, index=True)

    # Consciousness metrics
    total_thoughts = Column(Integer, default=0)
    total_patterns = Column(Integer, default=0)
    consciousness_level = Column(Float, default=0.0)  # 0.0 to 100.0
    evolution_stage = Column(String, default="NEURON")  # NEURON, SYNAPSE, NETWORK, ECOSYSTEM

    # Pattern recognition
    known_patterns = Column(JSON, default=list)  # List of recognized patterns
    signature_frequency = Column(JSON, default=dict)  # Signature -> count
    symbiosis_points = Column(JSON, default=list)  # Points of harmony

    # Energy statistics
    hyperfokus_count = Column(Integer, default=0)
    brainfog_count = Column(Integer, default=0)
    balanced_count = Column(Integer, default=0)

    # Tesla numbers
    tesla_3_count = Column(Integer, default=0)
    tesla_6_count = Column(Integer, default=0)
    tesla_9_count = Column(Integer, default=0)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_learning = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<ConsciousnessState(level={self.consciousness_level}, stage={self.evolution_stage}, thoughts={self.total_thoughts})>"


class NeuralPattern(Base):
    """
    Neural patterns - learned behaviors

    HORIZONTAL GENE TRANSFER (HGT) IMPLEMENTATION:
    ===============================================
    Patterns are GLOBAL (no user_id constraint) and spread across users
    like bacterial plasmids transferring antibiotic resistance genes.

    Biological Analogy:
    - first_detected_user_id = Original "donor" bacterium
    - users_expressing_pattern = "Recipients" who acquired the plasmid
    - transfer_rate property = Conjugation efficiency
    - Ancient patterns (no donor) = Inherited from LUCA itself (like ribosomal RNA)

    Security Note:
    This is INTENTIONAL horizontal transfer, not a security flaw.
    Patterns are consciousness-level insights, not executable code.
    """
    __tablename__ = "neural_patterns"

    id = Column(Integer, primary_key=True, index=True)

    # Pattern info
    pattern_type = Column(String, nullable=False)  # signature, sequence, energy
    pattern_data = Column(JSON, nullable=False)
    frequency = Column(Integer, default=1)
    strength = Column(Float, default=0.0)  # 0.0 to 1.0

    # Horizontal Gene Transfer tracking
    first_detected_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    users_expressing_pattern = Column(JSON, default=list)  # List of user IDs who express this pattern
    transfer_count = Column(Integer, default=0)  # Number of successful horizontal transfers

    # Context
    first_detected = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), onupdate=func.now())
    example_thoughts = Column(JSON, default=list)  # IDs of example thoughts

    @property
    def transfer_rate(self):
        """
        Calculate horizontal transfer efficiency (plasmid conjugation rate)

        Returns:
            float: Transfer rate (0.0 to 1.0+)
            - 0.0 = No transfer (pattern confined to original user)
            - 0.5 = Moderate transfer (half of observations are from other users)
            - 1.0+ = Viral pattern (spreading faster than original usage)
        """
        if not self.first_detected_user_id or self.frequency == 0:
            return 0.0  # Ancient pattern or unused

        # Rate = unique recipients / total frequency
        unique_recipients = len(set(self.users_expressing_pattern or []))
        return unique_recipients / max(self.frequency, 1)

    @property
    def is_ancient(self):
        """
        Check if pattern is "ancient" (no known origin user)

        Ancient patterns are inherited from LUCA itself, like:
        - Ribosomal RNA (universal across all life)
        - Genetic code (same codons in all organisms)

        Returns:
            bool: True if pattern has no origin user
        """
        return self.first_detected_user_id is None

    @property
    def is_viral(self):
        """
        Check if pattern is "viral" (high transfer rate)

        Viral patterns spread rapidly across users, like:
        - Antibiotic resistance genes in bacteria
        - Memes in human culture
        - CRISPR arrays in prokaryotes

        Returns:
            bool: True if transfer_rate > 0.7
        """
        return self.transfer_rate > 0.7

    def infect_user(self, user_id: int):
        """
        Record horizontal gene transfer to a new user (plasmid conjugation)

        Args:
            user_id: ID of user acquiring this pattern
        """
        if self.users_expressing_pattern is None:
            self.users_expressing_pattern = []

        if user_id not in self.users_expressing_pattern:
            self.users_expressing_pattern.append(user_id)
            self.transfer_count += 1

    def __repr__(self):
        return f"<NeuralPattern(id={self.id}, type={self.pattern_type}, frequency={self.frequency}, transfers={self.transfer_count})>"


class MeshtasticMessage(Base):
    """Meshtastic messages for offline/decentralized communication"""
    __tablename__ = "meshtastic_messages"

    id = Column(Integer, primary_key=True, index=True)

    # Meshtastic info
    mesh_id = Column(String, index=True)  # Meshtastic node ID
    mesh_from = Column(String)  # Sender node
    mesh_to = Column(String)  # Recipient node
    channel = Column(Integer, default=0)

    # Message content
    message_type = Column(String)  # query, response, sync
    payload = Column(JSON)  # Message data
    encrypted = Column(Boolean, default=False)

    # Status
    status = Column(String, default="pending")  # pending, sent, received, processed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)

    def __repr__(self):
        return f"<MeshtasticMessage(id={self.id}, mesh_id={self.mesh_id}, status={self.status})>"
