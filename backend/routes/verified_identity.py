"""
LUCA Verified Identity Routes
API endpoints for identity verification and global knowledge management

Endpoints:
- Verification requests
- Knowledge updates
- Community validation
- Admin review
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime

from backend.database import get_db
from backend.routes.auth import get_current_user
from backend.models import User
from backend.models_verified_identity import (
    UserIdentity,
    VerificationRequest,
    GlobalKnowledge,
    KnowledgeCorrectionLog,
    CommunityValidation,
    VerificationStatus
)
from backend.services.verification_service import VerificationService
from backend.services.knowledge_service import KnowledgeService


router = APIRouter(prefix="/api/verified-identity", tags=["verified-identity"])


# === Pydantic Models ===

class VerificationInstructionsRequest(BaseModel):
    method: str  # domain, signature, github, linkedin, etc.
    identifier: str  # domain, username, etc.


class DomainVerificationRequest(BaseModel):
    domain: str
    verification_token: str


class SignatureVerificationRequest(BaseModel):
    public_key: str
    signature: str
    message: str
    key_type: str = "ssh"  # ssh or pgp


class PublicProfileVerificationRequest(BaseModel):
    provider: str  # github, linkedin, twitter
    username: str
    proof_url: Optional[str] = None


class KnowledgeUpdateRequest(BaseModel):
    subject_type: str  # person, organization, concept
    subject_identifier: str  # email, domain, name
    knowledge_scope: str  # personal_facts, professional, etc.
    knowledge_key: str  # birth_date, affiliation, etc.
    knowledge_value: str
    knowledge_context: Optional[Dict[str, Any]] = None
    source_url: Optional[str] = None
    reason: Optional[str] = None


class CommunityValidationRequest(BaseModel):
    knowledge_id: int
    validation_type: str  # confirm, dispute, request_evidence
    reason: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None


class AdminReviewRequest(BaseModel):
    request_id: int
    decision: str  # approve, reject
    notes: Optional[str] = None


# === Verification Endpoints ===

@router.post("/verification/instructions")
async def get_verification_instructions(
    request: VerificationInstructionsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get instructions for identity verification.

    Returns verification token and step-by-step instructions.
    """
    service = VerificationService(db)
    instructions = service.get_verification_instructions(
        user_id=current_user.id,
        method=request.method,
        identifier=request.identifier
    )

    return {
        "success": True,
        "user_id": current_user.id,
        "method": request.method,
        "identifier": request.identifier,
        **instructions
    }


@router.post("/verification/domain")
async def verify_domain(
    request: DomainVerificationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify domain ownership via DNS TXT or well-known file.
    """
    service = VerificationService(db)
    result = await service.verify_domain_ownership(
        user_id=current_user.id,
        domain=request.domain,
        verification_token=request.verification_token
    )

    if result["success"]:
        # Create verified identity
        identity = UserIdentity(
            user_id=current_user.id,
            verification_method="domain",
            verification_status="approved",
            verified_domain=request.domain,
            verified_at=result["verified_at"],
            verification_metadata=result
        )
        db.add(identity)
        db.commit()
        db.refresh(identity)

        return {
            "success": True,
            "message": "Domain verified successfully",
            "identity_id": identity.id,
            "domain": request.domain,
            "verified_at": result["verified_at"]
        }
    else:
        return {
            "success": False,
            "error": result.get("error", "Verification failed")
        }


@router.post("/verification/signature")
async def verify_signature(
    request: SignatureVerificationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify cryptographic signature (SSH or PGP).
    """
    service = VerificationService(db)
    result = await service.verify_cryptographic_signature(
        user_id=current_user.id,
        public_key=request.public_key,
        signature=request.signature,
        message=request.message,
        key_type=request.key_type
    )

    if result["success"]:
        # Create verified identity
        identity = UserIdentity(
            user_id=current_user.id,
            verification_method="signature",
            verification_status="approved",
            public_key=request.public_key,
            signature_proof=request.signature,
            verified_at=result["verified_at"],
            verification_metadata=result
        )
        db.add(identity)
        db.commit()
        db.refresh(identity)

        return {
            "success": True,
            "message": "Signature verified successfully",
            "identity_id": identity.id,
            "key_type": request.key_type,
            "verified_at": result["verified_at"]
        }
    else:
        return {
            "success": False,
            "error": result.get("error", "Verification failed")
        }


@router.post("/verification/public-profile")
async def verify_public_profile(
    request: PublicProfileVerificationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify public profile (GitHub, LinkedIn, etc.).
    """
    service = VerificationService(db)
    result = await service.verify_public_profile(
        user_id=current_user.id,
        provider=request.provider,
        username=request.username,
        proof_url=request.proof_url
    )

    if result.get("requires_manual_review"):
        # Create verification request for admin review
        verification_request = VerificationRequest(
            user_id=current_user.id,
            verification_method="public_profile",
            proof_data=result,
            proof_urls=[request.proof_url] if request.proof_url else []
        )
        db.add(verification_request)
        db.commit()

        return {
            "success": False,
            "requires_manual_review": True,
            "message": result.get("instructions", "Verification request submitted for admin review"),
            "request_id": verification_request.id
        }

    if result["success"]:
        # Create verified identity
        identity = UserIdentity(
            user_id=current_user.id,
            verification_method="public_profile",
            verification_status="approved",
            provider=request.provider,
            provider_user_id=request.username,
            provider_profile_url=result.get("profile_url"),
            verification_proof_url=request.proof_url,
            verified_at=result["verified_at"],
            verification_metadata=result
        )
        db.add(identity)
        db.commit()
        db.refresh(identity)

        return {
            "success": True,
            "message": f"{request.provider.title()} profile verified successfully",
            "identity_id": identity.id,
            "username": request.username,
            "verified_at": result["verified_at"]
        }
    else:
        return {
            "success": False,
            "error": result.get("error", "Verification failed")
        }


@router.get("/verification/status")
async def get_verification_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's verification status.
    """
    identities = db.query(UserIdentity).filter(
        UserIdentity.user_id == current_user.id
    ).all()

    return {
        "user_id": current_user.id,
        "verified_identities": [
            {
                "id": identity.id,
                "method": identity.verification_method,
                "status": identity.verification_status,
                "verified_name": identity.verified_name,
                "verified_email": identity.verified_email,
                "verified_domain": identity.verified_domain,
                "provider": identity.provider,
                "trust_score": identity.trust_score,
                "verified_at": identity.verified_at.isoformat() if identity.verified_at else None
            }
            for identity in identities
        ],
        "has_verified_identity": any(
            identity.verification_status == "approved" for identity in identities
        )
    }


# === Knowledge Management Endpoints ===

@router.post("/knowledge/update")
async def update_knowledge(
    request: KnowledgeUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update global knowledge (requires verified identity).
    """
    # Get verified identity
    identity = db.query(UserIdentity).filter(
        UserIdentity.user_id == current_user.id,
        UserIdentity.verification_status == "approved"
    ).first()

    if not identity:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Verified identity required to update global knowledge"
        )

    service = KnowledgeService(db)
    result = service.create_knowledge_update(
        identity_id=identity.id,
        subject_type=request.subject_type,
        subject_identifier=request.subject_identifier,
        knowledge_scope=request.knowledge_scope,
        knowledge_key=request.knowledge_key,
        knowledge_value=request.knowledge_value,
        knowledge_context=request.knowledge_context,
        source_url=request.source_url,
        reason=request.reason
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=result.get("error", "Knowledge update failed")
        )

    return {
        "success": True,
        "message": "Knowledge updated successfully",
        **result
    }


@router.get("/knowledge/search")
async def search_knowledge(
    query: str,
    subject_type: Optional[str] = None,
    knowledge_scope: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Search global knowledge (public endpoint).
    """
    service = KnowledgeService(db)
    results = service.search_knowledge(
        query=query,
        subject_type=subject_type,
        knowledge_scope=knowledge_scope,
        limit=limit
    )

    return {
        "query": query,
        "count": len(results),
        "results": results
    }


@router.get("/knowledge/subject/{subject_identifier}")
async def get_knowledge_by_subject(
    subject_identifier: str,
    knowledge_key: Optional[str] = None,
    include_history: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get knowledge about a specific subject (public endpoint).
    """
    service = KnowledgeService(db)
    knowledge = service.get_knowledge(
        subject_identifier=subject_identifier,
        knowledge_key=knowledge_key,
        include_history=include_history
    )

    return {
        "subject_identifier": subject_identifier,
        "count": len(knowledge),
        "knowledge": knowledge
    }


@router.get("/knowledge/corrections")
async def get_correction_history(
    subject_identifier: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get correction history (transparency log).
    """
    service = KnowledgeService(db)

    # Users can see all corrections, or filter by subject
    corrections = service.get_correction_history(
        subject_identifier=subject_identifier,
        limit=limit
    )

    return {
        "count": len(corrections),
        "corrections": corrections
    }


@router.post("/knowledge/validate")
async def validate_knowledge(
    request: CommunityValidationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add community validation for knowledge entry.
    """
    # Get verified identity
    identity = db.query(UserIdentity).filter(
        UserIdentity.user_id == current_user.id,
        UserIdentity.verification_status == "approved"
    ).first()

    if not identity:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Verified identity required for community validation"
        )

    service = KnowledgeService(db)
    result = service.add_community_validation(
        knowledge_id=request.knowledge_id,
        validator_identity_id=identity.id,
        validation_type=request.validation_type,
        reason=request.reason,
        evidence=request.evidence
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Validation failed")
        )

    return {
        "success": True,
        "message": "Validation recorded successfully",
        **result
    }


# === Admin Endpoints ===

def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependency to ensure user is admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.get("/admin/verification-requests", dependencies=[Depends(get_current_admin)])
async def get_verification_requests(
    status_filter: Optional[str] = "pending",
    db: Session = Depends(get_db)
):
    """
    Get pending verification requests (admin only).
    """
    query = db.query(VerificationRequest)

    if status_filter:
        query = query.filter(VerificationRequest.status == status_filter)

    requests = query.order_by(VerificationRequest.created_at.desc()).all()

    return {
        "count": len(requests),
        "requests": [
            {
                "id": req.id,
                "user_id": req.user_id,
                "verification_method": req.verification_method,
                "requested_name": req.requested_name,
                "requested_email": req.requested_email,
                "proof_data": req.proof_data,
                "proof_urls": req.proof_urls,
                "status": req.status,
                "created_at": req.created_at.isoformat()
            }
            for req in requests
        ]
    }


@router.post("/admin/review-verification", dependencies=[Depends(get_current_admin)])
async def review_verification(
    request: AdminReviewRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Review and approve/reject verification request (admin only).
    """
    verification_request = db.query(VerificationRequest).filter(
        VerificationRequest.id == request.request_id
    ).first()

    if not verification_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification request not found"
        )

    if request.decision == "approve":
        # Create verified identity
        identity = UserIdentity(
            user_id=verification_request.user_id,
            verification_method=verification_request.verification_method,
            verification_status="approved",
            verified_name=verification_request.requested_name,
            verified_email=verification_request.requested_email,
            verified_at=datetime.utcnow(),
            reviewed_by=current_user.id,
            review_notes=request.notes,
            verification_metadata=verification_request.proof_data
        )
        db.add(identity)

        verification_request.status = "approved"
        verification_request.reviewed_by = current_user.id
        verification_request.review_notes = request.notes
        verification_request.reviewed_at = datetime.utcnow()

        db.commit()

        return {
            "success": True,
            "message": "Verification approved",
            "identity_id": identity.id
        }

    elif request.decision == "reject":
        verification_request.status = "rejected"
        verification_request.reviewed_by = current_user.id
        verification_request.review_notes = request.notes
        verification_request.rejection_reason = request.notes
        verification_request.reviewed_at = datetime.utcnow()

        db.commit()

        return {
            "success": True,
            "message": "Verification rejected"
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid decision. Must be 'approve' or 'reject'"
        )


@router.get("/admin/statistics", dependencies=[Depends(get_current_admin)])
async def get_admin_statistics(
    db: Session = Depends(get_db)
):
    """
    Get statistics for admin dashboard.
    """
    total_identities = db.query(UserIdentity).count()
    verified_identities = db.query(UserIdentity).filter(
        UserIdentity.verification_status == "approved"
    ).count()
    pending_requests = db.query(VerificationRequest).filter(
        VerificationRequest.status == "pending"
    ).count()
    total_knowledge = db.query(GlobalKnowledge).filter(
        GlobalKnowledge.is_current == True
    ).count()
    total_corrections = db.query(KnowledgeCorrectionLog).count()

    return {
        "total_identities": total_identities,
        "verified_identities": verified_identities,
        "pending_requests": pending_requests,
        "total_knowledge_entries": total_knowledge,
        "total_corrections": total_corrections
    }
