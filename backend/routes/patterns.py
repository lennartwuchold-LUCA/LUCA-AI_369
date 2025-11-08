"""
Pattern Routes - HGT (Horizontal Gene Transfer) Statistics and Analysis

New endpoints to visualize pattern spread across users
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, NeuralPattern
from backend.routes.auth import get_current_user
from typing import List, Dict, Any

router = APIRouter(prefix="/api/patterns", tags=["patterns"])


@router.get("/hgt-stats")
async def get_hgt_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get Horizontal Gene Transfer statistics

    Returns:
        - Total patterns
        - Viral patterns (high transfer rate)
        - Ancient patterns (no known origin)
        - Most transferred pattern
        - User's contributed patterns
    """
    # Get all patterns
    all_patterns = db.query(NeuralPattern).all()

    if not all_patterns:
        return {
            "total_patterns": 0,
            "viral_patterns": 0,
            "ancient_patterns": 0,
            "user_contributed": 0,
            "user_adopted": 0,
            "most_viral": None,
            "patterns": []
        }

    # Calculate statistics
    viral_patterns = [p for p in all_patterns if p.is_viral]
    ancient_patterns = [p for p in all_patterns if p.is_ancient]

    # Patterns contributed by current user
    user_contributed = [
        p for p in all_patterns
        if p.first_detected_user_id == current_user.id
    ]

    # Patterns adopted by current user (received via HGT)
    user_adopted = [
        p for p in all_patterns
        if p.users_expressing_pattern and current_user.id in p.users_expressing_pattern
        and p.first_detected_user_id != current_user.id  # Not the original donor
    ]

    # Find most viral pattern
    most_viral = None
    if all_patterns:
        most_viral_pattern = max(all_patterns, key=lambda p: p.transfer_rate)
        if most_viral_pattern.transfer_rate > 0:
            most_viral = {
                "id": most_viral_pattern.id,
                "type": most_viral_pattern.pattern_type,
                "transfer_rate": most_viral_pattern.transfer_rate,
                "transfer_count": most_viral_pattern.transfer_count,
                "frequency": most_viral_pattern.frequency
            }

    # Build pattern list with HGT info
    patterns_data = []
    for pattern in all_patterns[:20]:  # Limit to 20 most recent
        patterns_data.append({
            "id": pattern.id,
            "type": pattern.pattern_type,
            "frequency": pattern.frequency,
            "strength": pattern.strength,
            "transfer_rate": pattern.transfer_rate,
            "transfer_count": pattern.transfer_count,
            "is_viral": pattern.is_viral,
            "is_ancient": pattern.is_ancient,
            "user_is_donor": pattern.first_detected_user_id == current_user.id,
            "user_has_pattern": current_user.id in (pattern.users_expressing_pattern or []),
            "created": pattern.first_detected.isoformat() if pattern.first_detected else None
        })

    return {
        "total_patterns": len(all_patterns),
        "viral_patterns": len(viral_patterns),
        "ancient_patterns": len(ancient_patterns),
        "user_contributed": len(user_contributed),
        "user_adopted": len(user_adopted),
        "most_viral": most_viral,
        "patterns": patterns_data
    }


@router.get("/genealogy/{pattern_id}")
async def get_pattern_genealogy(
    pattern_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get pattern genealogy - trace how a pattern spread across users

    Similar to tracking a gene's horizontal transfer history in bacteria
    """
    pattern = db.query(NeuralPattern).filter(NeuralPattern.id == pattern_id).first()

    if not pattern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pattern not found"
        )

    # Get donor info
    donor = None
    if pattern.first_detected_user_id:
        donor_user = db.query(User).filter(User.id == pattern.first_detected_user_id).first()
        if donor_user:
            donor = {
                "id": donor_user.id,
                "username": donor_user.username,
                "is_current_user": donor_user.id == current_user.id
            }

    # Get recipient info
    recipients = []
    if pattern.users_expressing_pattern:
        for user_id in pattern.users_expressing_pattern:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                recipients.append({
                    "id": user.id,
                    "username": user.username,
                    "is_current_user": user.id == current_user.id
                })

    return {
        "pattern_id": pattern.id,
        "pattern_type": pattern.pattern_type,
        "frequency": pattern.frequency,
        "strength": pattern.strength,
        "transfer_rate": pattern.transfer_rate,
        "transfer_count": pattern.transfer_count,
        "is_viral": pattern.is_viral,
        "is_ancient": pattern.is_ancient,
        "donor": donor,
        "recipients": recipients,
        "created": pattern.first_detected.isoformat() if pattern.first_detected else None,
        "last_seen": pattern.last_seen.isoformat() if pattern.last_seen else None
    }


@router.get("/viral")
async def get_viral_patterns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all viral patterns (transfer_rate > 0.7)

    These are patterns spreading rapidly across users like:
    - Antibiotic resistance genes in bacteria
    - Viral memes in culture
    """
    all_patterns = db.query(NeuralPattern).all()
    viral_patterns = [p for p in all_patterns if p.is_viral]

    result = []
    for pattern in viral_patterns:
        result.append({
            "id": pattern.id,
            "type": pattern.pattern_type,
            "transfer_rate": pattern.transfer_rate,
            "transfer_count": pattern.transfer_count,
            "frequency": pattern.frequency,
            "strength": pattern.strength,
            "recipient_count": len(pattern.users_expressing_pattern or []),
            "user_has_pattern": current_user.id in (pattern.users_expressing_pattern or [])
        })

    return {
        "count": len(result),
        "patterns": result
    }


@router.get("/ancient")
async def get_ancient_patterns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all ancient patterns (no known origin user)

    These are patterns inherited from LUCA itself, like:
    - Ribosomal RNA (universal across all life)
    - Genetic code (same in all organisms)
    """
    ancient_patterns = db.query(NeuralPattern).filter(
        NeuralPattern.first_detected_user_id == None
    ).all()

    result = []
    for pattern in ancient_patterns:
        result.append({
            "id": pattern.id,
            "type": pattern.pattern_type,
            "frequency": pattern.frequency,
            "strength": pattern.strength,
            "transfer_rate": pattern.transfer_rate,
            "recipient_count": len(pattern.users_expressing_pattern or []),
            "user_has_pattern": current_user.id in (pattern.users_expressing_pattern or []),
            "created": pattern.first_detected.isoformat() if pattern.first_detected else None
        })

    return {
        "count": len(result),
        "patterns": result
    }
