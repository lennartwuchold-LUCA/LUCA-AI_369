"""
LUCA Global Knowledge Service
Handles global knowledge updates by verified identities

Philosophy:
- Privacy-by-Design: Only with explicit consent
- Facts, not opinions
- Transparent audit trail
- Community validation for public figures
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from backend.models_verified_identity import (
    UserIdentity,
    GlobalKnowledge,
    KnowledgeCorrectionLog,
    CommunityValidation,
    KnowledgeScope,
    VerificationStatus
)


class KnowledgeService:
    """Service for managing global knowledge updates"""

    def __init__(self, db: Session):
        self.db = db

    def can_update_knowledge(
        self,
        identity_id: int,
        subject_identifier: str
    ) -> tuple[bool, Optional[str]]:
        """
        Check if an identity can update knowledge about a subject.

        Rules:
        1. Identity must be verified (approved status)
        2. For self-knowledge: subject_identifier must match verified identity
        3. For others: requires high trust score or community validation

        Returns:
            (can_update, reason_if_not)
        """
        identity = self.db.query(UserIdentity).filter(
            UserIdentity.id == identity_id
        ).first()

        if not identity:
            return False, "Identity not found"

        if identity.verification_status != "approved":
            return False, f"Identity not verified (status: {identity.verification_status})"

        # Check if updating own information
        is_self = (
            subject_identifier == identity.verified_email or
            subject_identifier == identity.verified_domain or
            subject_identifier == identity.verified_name
        )

        if is_self:
            return True, None

        # For updating others: require high trust score
        if identity.trust_score < 0.8:
            return False, "Insufficient trust score to update others' information"

        return True, None

    def create_knowledge_update(
        self,
        identity_id: int,
        subject_type: str,
        subject_identifier: str,
        knowledge_scope: str,
        knowledge_key: str,
        knowledge_value: str,
        knowledge_context: Optional[Dict[str, Any]] = None,
        source_url: Optional[str] = None,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create or update global knowledge.

        Args:
            identity_id: Verified identity making the update
            subject_type: "person", "organization", "concept"
            subject_identifier: Email, domain, or unique identifier
            knowledge_scope: KnowledgeScope value
            knowledge_key: Specific fact being updated
            knowledge_value: The information
            knowledge_context: Additional context
            source_url: Reference URL
            reason: Reason for update/correction

        Returns:
            Dict with update result
        """
        # Check permission
        can_update, reason_denied = self.can_update_knowledge(identity_id, subject_identifier)
        if not can_update:
            return {
                "success": False,
                "error": reason_denied
            }

        # Check if knowledge already exists
        existing = self.db.query(GlobalKnowledge).filter(
            and_(
                GlobalKnowledge.subject_identifier == subject_identifier,
                GlobalKnowledge.knowledge_key == knowledge_key,
                GlobalKnowledge.is_current == True
            )
        ).first()

        action_type = "create"
        old_value = None

        if existing:
            # Update existing knowledge
            action_type = "update"
            old_value = existing.knowledge_value

            # Mark old as not current
            existing.is_current = False
            existing.updated_at = datetime.utcnow()

        # Create new knowledge entry
        new_knowledge = GlobalKnowledge(
            subject_type=subject_type,
            subject_identifier=subject_identifier,
            knowledge_scope=knowledge_scope,
            knowledge_key=knowledge_key,
            knowledge_value=knowledge_value,
            knowledge_context=knowledge_context,
            verified_by_id=identity_id,
            source_url=source_url,
            version=existing.version + 1 if existing else 1,
            previous_value=old_value,
            is_current=True
        )

        self.db.add(new_knowledge)
        self.db.flush()

        # Create correction log
        log = KnowledgeCorrectionLog(
            knowledge_id=new_knowledge.id,
            identity_id=identity_id,
            action_type=action_type,
            old_value=old_value,
            new_value=knowledge_value,
            reason=reason
        )

        self.db.add(log)
        self.db.commit()

        return {
            "success": True,
            "action": action_type,
            "knowledge_id": new_knowledge.id,
            "version": new_knowledge.version,
            "requires_review": False
        }

    def get_knowledge(
        self,
        subject_identifier: str,
        knowledge_key: Optional[str] = None,
        include_history: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get knowledge about a subject.

        Args:
            subject_identifier: Subject to look up
            knowledge_key: Specific fact (optional, returns all if None)
            include_history: Include historical versions

        Returns:
            List of knowledge entries
        """
        query = self.db.query(GlobalKnowledge).filter(
            GlobalKnowledge.subject_identifier == subject_identifier
        )

        if knowledge_key:
            query = query.filter(GlobalKnowledge.knowledge_key == knowledge_key)

        if not include_history:
            query = query.filter(GlobalKnowledge.is_current == True)

        knowledge_entries = query.order_by(
            GlobalKnowledge.knowledge_key,
            GlobalKnowledge.version.desc()
        ).all()

        result = []
        for entry in knowledge_entries:
            result.append({
                "id": entry.id,
                "subject_type": entry.subject_type,
                "subject_identifier": entry.subject_identifier,
                "scope": entry.knowledge_scope,
                "key": entry.knowledge_key,
                "value": entry.knowledge_value,
                "context": entry.knowledge_context,
                "version": entry.version,
                "confidence_score": entry.confidence_score,
                "community_validations": entry.community_validations,
                "community_disputes": entry.community_disputes,
                "source_url": entry.source_url,
                "created_at": entry.created_at.isoformat(),
                "updated_at": entry.updated_at.isoformat(),
                "is_current": entry.is_current
            })

        return result

    def get_correction_history(
        self,
        subject_identifier: Optional[str] = None,
        identity_id: Optional[int] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get correction history.

        Args:
            subject_identifier: Filter by subject (optional)
            identity_id: Filter by identity (optional)
            limit: Maximum entries to return

        Returns:
            List of correction log entries
        """
        query = self.db.query(KnowledgeCorrectionLog).join(
            GlobalKnowledge
        )

        if subject_identifier:
            query = query.filter(
                GlobalKnowledge.subject_identifier == subject_identifier
            )

        if identity_id:
            query = query.filter(
                KnowledgeCorrectionLog.identity_id == identity_id
            )

        logs = query.order_by(
            KnowledgeCorrectionLog.created_at.desc()
        ).limit(limit).all()

        result = []
        for log in logs:
            result.append({
                "id": log.id,
                "knowledge_id": log.knowledge_id,
                "identity_id": log.identity_id,
                "action_type": log.action_type,
                "old_value": log.old_value,
                "new_value": log.new_value,
                "reason": log.reason,
                "created_at": log.created_at.isoformat(),
                "reviewed": log.reviewed,
                "review_decision": log.review_decision
            })

        return result

    def add_community_validation(
        self,
        knowledge_id: int,
        validator_identity_id: int,
        validation_type: str,
        reason: Optional[str] = None,
        evidence: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add community validation for a knowledge entry.

        Args:
            knowledge_id: Knowledge to validate
            validator_identity_id: Identity performing validation
            validation_type: "confirm", "dispute", "request_evidence"
            reason: Reason for validation
            evidence: Supporting evidence

        Returns:
            Dict with validation result
        """
        # Get validator identity
        validator = self.db.query(UserIdentity).filter(
            UserIdentity.id == validator_identity_id
        ).first()

        if not validator or validator.verification_status != "approved":
            return {
                "success": False,
                "error": "Validator must be verified"
            }

        # Get knowledge entry
        knowledge = self.db.query(GlobalKnowledge).filter(
            GlobalKnowledge.id == knowledge_id
        ).first()

        if not knowledge:
            return {
                "success": False,
                "error": "Knowledge entry not found"
            }

        # Check if already validated by this identity
        existing = self.db.query(CommunityValidation).filter(
            and_(
                CommunityValidation.knowledge_id == knowledge_id,
                CommunityValidation.validator_id == validator_identity_id
            )
        ).first()

        if existing:
            return {
                "success": False,
                "error": "Already validated by this identity"
            }

        # Create validation
        validation = CommunityValidation(
            knowledge_id=knowledge_id,
            validator_id=validator_identity_id,
            validation_type=validation_type,
            validation_reason=reason,
            evidence_provided=evidence,
            weight=validator.trust_score
        )

        self.db.add(validation)

        # Update knowledge entry counts
        if validation_type == "confirm":
            knowledge.community_validations += 1
        elif validation_type == "dispute":
            knowledge.community_disputes += 1

        # Recalculate confidence score
        total_weight = knowledge.community_validations + knowledge.community_disputes
        if total_weight > 0:
            knowledge.confidence_score = knowledge.community_validations / total_weight

        self.db.commit()

        return {
            "success": True,
            "validation_id": validation.id,
            "new_confidence_score": knowledge.confidence_score,
            "validations": knowledge.community_validations,
            "disputes": knowledge.community_disputes
        }

    def search_knowledge(
        self,
        query: str,
        subject_type: Optional[str] = None,
        knowledge_scope: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search global knowledge.

        Args:
            query: Search query
            subject_type: Filter by subject type
            knowledge_scope: Filter by scope
            limit: Maximum results

        Returns:
            List of matching knowledge entries
        """
        db_query = self.db.query(GlobalKnowledge).filter(
            and_(
                GlobalKnowledge.is_current == True,
                or_(
                    GlobalKnowledge.subject_identifier.like(f"%{query}%"),
                    GlobalKnowledge.knowledge_key.like(f"%{query}%"),
                    GlobalKnowledge.knowledge_value.like(f"%{query}%")
                )
            )
        )

        if subject_type:
            db_query = db_query.filter(GlobalKnowledge.subject_type == subject_type)

        if knowledge_scope:
            db_query = db_query.filter(GlobalKnowledge.knowledge_scope == knowledge_scope)

        results = db_query.limit(limit).all()

        return [self._knowledge_to_dict(k) for k in results]

    def _knowledge_to_dict(self, knowledge: GlobalKnowledge) -> Dict[str, Any]:
        """Convert knowledge entry to dict"""
        return {
            "id": knowledge.id,
            "subject_type": knowledge.subject_type,
            "subject_identifier": knowledge.subject_identifier,
            "scope": knowledge.knowledge_scope,
            "key": knowledge.knowledge_key,
            "value": knowledge.knowledge_value,
            "context": knowledge.knowledge_context,
            "version": knowledge.version,
            "confidence_score": knowledge.confidence_score,
            "community_validations": knowledge.community_validations,
            "community_disputes": knowledge.community_disputes,
            "source_url": knowledge.source_url,
            "created_at": knowledge.created_at.isoformat(),
            "updated_at": knowledge.updated_at.isoformat()
        }

    def increase_trust_score(
        self,
        identity_id: int,
        amount: float = 0.05
    ) -> float:
        """
        Increase trust score for helpful contributions.

        Args:
            identity_id: Identity to reward
            amount: Amount to increase (default 0.05)

        Returns:
            New trust score
        """
        identity = self.db.query(UserIdentity).filter(
            UserIdentity.id == identity_id
        ).first()

        if identity:
            identity.trust_score = min(1.0, identity.trust_score + amount)
            self.db.commit()
            return identity.trust_score

        return 0.0

    def decrease_trust_score(
        self,
        identity_id: int,
        amount: float = 0.1
    ) -> float:
        """
        Decrease trust score for disputed contributions.

        Args:
            identity_id: Identity to penalize
            amount: Amount to decrease (default 0.1)

        Returns:
            New trust score
        """
        identity = self.db.query(UserIdentity).filter(
            UserIdentity.id == identity_id
        ).first()

        if identity:
            identity.trust_score = max(0.0, identity.trust_score - amount)
            self.db.commit()
            return identity.trust_score

        return 0.0
