"""
LUCA Verified Identity Models
Extends the core models with verified identity capabilities

Philosophy: "Flow over Force" - Only verified identities can update global knowledge
3-6-9 Principle: if identification == true → global_knowledge_update_enabled
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base
import enum


class VerificationMethod(enum.Enum):
    """Supported verification methods"""
    DOMAIN = "domain"              # Domain ownership verification
    SIGNATURE = "signature"        # Cryptographic signature (PGP, SSH, etc.)
    PUBLIC_PROFILE = "public_profile"  # OAuth with public profiles (GitHub, LinkedIn)
    BIOMETRIC = "biometric"        # Biometric verification
    GOVERNMENT_ID = "government_id"   # Government-issued ID
    COMMUNITY = "community"        # Community validation for public figures
    MESHTASTIC_NODE = "meshtastic_node"  # Verified mesh network node


class VerificationStatus(enum.Enum):
    """Verification status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    REVOKED = "revoked"


class KnowledgeScope(enum.Enum):
    """Scope of knowledge that can be updated"""
    PERSONAL_FACTS = "personal_facts"      # Birth date, location, affiliations
    PROFESSIONAL = "professional"          # Work history, skills, publications
    PUBLIC_STATEMENTS = "public_statements"  # Quotes, positions, statements
    CORRECTIONS = "corrections"            # Corrections to misinformation
    PREFERENCES = "preferences"            # Preferred names, pronouns, contact


class UserIdentity(Base):
    """
    Extended identity verification for users.
    Enables verified users to correct global knowledge about themselves.
    """
    __tablename__ = "user_identities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Verification details
    verification_method = Column(String, nullable=False)  # VerificationMethod enum value
    verification_status = Column(String, default="pending")  # VerificationStatus enum value

    # Identity information
    verified_name = Column(String, nullable=True)  # Real name
    verified_email = Column(String, nullable=True)  # Verified email
    verified_domain = Column(String, nullable=True)  # For domain verification

    # Cryptographic proofs
    public_key = Column(Text, nullable=True)  # PGP/SSH public key
    signature_proof = Column(Text, nullable=True)  # Cryptographic proof

    # External verification
    provider = Column(String, nullable=True)  # GitHub, LinkedIn, Veriff, etc.
    provider_user_id = Column(String, nullable=True)  # ID from provider
    provider_profile_url = Column(String, nullable=True)  # Public profile URL

    # Metadata
    verification_metadata = Column(JSON, nullable=True)  # Additional proof data
    verification_proof_url = Column(String, nullable=True)  # URL to public proof

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)  # Some verifications expire

    # Admin review
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Admin who reviewed
    review_notes = Column(Text, nullable=True)

    # Trust score (0.0 - 1.0)
    trust_score = Column(Float, default=0.5)  # Increases with contributions

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="identities")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    knowledge_updates = relationship("GlobalKnowledge", back_populates="verified_by")
    correction_logs = relationship("KnowledgeCorrectionLog", back_populates="identity")


class GlobalKnowledge(Base):
    """
    Global knowledge base that can be updated by verified identities.
    Privacy-by-Design: Only facts, not opinions. Only with explicit consent.
    """
    __tablename__ = "global_knowledge"

    id = Column(Integer, primary_key=True, index=True)

    # Subject of knowledge (who/what this is about)
    subject_type = Column(String, nullable=False)  # person, organization, concept
    subject_identifier = Column(String, nullable=False, index=True)  # email, domain, name

    # Knowledge content
    knowledge_scope = Column(String, nullable=False)  # KnowledgeScope enum value
    knowledge_key = Column(String, nullable=False)  # e.g., "birth_date", "affiliation"
    knowledge_value = Column(Text, nullable=False)  # The actual information
    knowledge_context = Column(JSON, nullable=True)  # Additional context

    # Source and verification
    verified_by_id = Column(Integer, ForeignKey("user_identities.id"), nullable=False)
    source_type = Column(String, default="self_reported")  # self_reported, document, public_record
    source_url = Column(String, nullable=True)  # Reference URL

    # Confidence and validation
    confidence_score = Column(Float, default=1.0)  # 0.0 - 1.0
    community_validations = Column(Integer, default=0)  # Number of confirmations
    community_disputes = Column(Integer, default=0)  # Number of disputes

    # Version control
    version = Column(Integer, default=1)
    previous_value = Column(Text, nullable=True)  # Previous version
    is_current = Column(Boolean, default=True)  # Is this the current version?

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    verified_by = relationship("UserIdentity", back_populates="knowledge_updates")
    correction_logs = relationship("KnowledgeCorrectionLog", back_populates="knowledge")


class KnowledgeCorrectionLog(Base):
    """
    Transparency log: Who corrected what and when.
    Immutable audit trail for all knowledge corrections.
    """
    __tablename__ = "knowledge_correction_logs"

    id = Column(Integer, primary_key=True, index=True)

    # What was corrected
    knowledge_id = Column(Integer, ForeignKey("global_knowledge.id"), nullable=False)

    # Who corrected it
    identity_id = Column(Integer, ForeignKey("user_identities.id"), nullable=False)

    # Details of correction
    action_type = Column(String, nullable=False)  # create, update, delete, dispute
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)  # Why was this corrected?

    # Evidence
    evidence_urls = Column(JSON, nullable=True)  # Supporting evidence
    evidence_metadata = Column(JSON, nullable=True)

    # Admin review
    requires_review = Column(Boolean, default=False)
    reviewed = Column(Boolean, default=False)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_decision = Column(String, nullable=True)  # approved, rejected, flagged
    review_notes = Column(Text, nullable=True)

    # Timestamps (immutable)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    knowledge = relationship("GlobalKnowledge", back_populates="correction_logs")
    identity = relationship("UserIdentity", back_populates="correction_logs")
    reviewer = relationship("User", foreign_keys=[reviewed_by])


class CommunityValidation(Base):
    """
    Community validation for public figures and disputed knowledge.
    Enables community consensus on factual information.
    """
    __tablename__ = "community_validations"

    id = Column(Integer, primary_key=True, index=True)

    # What is being validated
    knowledge_id = Column(Integer, ForeignKey("global_knowledge.id"), nullable=False)

    # Who is validating
    validator_id = Column(Integer, ForeignKey("user_identities.id"), nullable=False)

    # Validation
    validation_type = Column(String, nullable=False)  # confirm, dispute, request_evidence
    validation_reason = Column(Text, nullable=True)
    evidence_provided = Column(JSON, nullable=True)

    # Voting weight (based on trust score and expertise)
    weight = Column(Float, default=1.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    knowledge = relationship("GlobalKnowledge")
    validator = relationship("UserIdentity")


class VerificationRequest(Base):
    """
    Pending verification requests from users.
    Admin workflow for reviewing identity verification.
    """
    __tablename__ = "verification_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Request details
    verification_method = Column(String, nullable=False)
    requested_name = Column(String, nullable=True)
    requested_email = Column(String, nullable=True)

    # Submitted proof
    proof_data = Column(JSON, nullable=False)  # Submitted evidence
    proof_urls = Column(JSON, nullable=True)  # URLs to verification

    # Status
    status = Column(String, default="pending")  # pending, approved, rejected

    # Admin review
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])


# Update User model relationship (to be added to models.py)
# Add to User class:
# identities = relationship("UserIdentity", foreign_keys="UserIdentity.user_id", back_populates="user")
