"""
Mycelium Network Routes - Decentralized, Self-Healing AI Architecture

Fungal-inspired network with HACCP safety controls
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, NeuralPattern
from backend.routes.auth import get_current_user
from backend.consciousness.mycelium_network import MyceliumNetwork
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/api/mycelium", tags=["mycelium"])

# Global mycelium network instance
# In production, this should be a singleton or stored in app state
_mycelium_network = None


def get_mycelium_network():
    """Get or create the global mycelium network"""
    global _mycelium_network
    if _mycelium_network is None:
        _mycelium_network = MyceliumNetwork()
    return _mycelium_network


class PatternTransferRequest(BaseModel):
    """Request to transfer a pattern via mycelium"""
    pattern_id: int
    to_user_id: int
    pattern_metadata: Dict[str, Any] = {}


@router.get("/stats")
async def get_network_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get Mycelium Network statistics

    Returns:
        - Network health status
        - Node count
        - Connection (hyphae) count
        - Average node health
        - Transfer statistics
        - HACCP hazard log
    """
    mycelium = get_mycelium_network()

    # Initialize user as node if not exists
    if current_user.id not in mycelium.nodes:
        mycelium.add_node(current_user.id, node_type='user')

    # Get all users from database and add as nodes
    all_users = db.query(User).all()
    for user in all_users:
        if user.id not in mycelium.nodes:
            mycelium.add_node(user.id, node_type='user')

    # Get network statistics
    stats = mycelium.get_network_stats()

    # Add current user's node info
    user_node = mycelium.nodes.get(current_user.id)
    if user_node:
        stats['current_user_node'] = {
            'id': user_node.node_id,
            'health': user_node.health,
            'connections': len(user_node.connections),
            'patterns_hosted': len(user_node.patterns_hosted),
            'nutrient_level': user_node.nutrient_level
        }

    return stats


@router.get("/nodes")
async def get_all_nodes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all nodes in the mycelium network

    Each node represents a user/agent in the system
    """
    mycelium = get_mycelium_network()

    # Ensure all users are represented as nodes
    all_users = db.query(User).all()
    for user in all_users:
        if user.id not in mycelium.nodes:
            mycelium.add_node(user.id, node_type='user')

    nodes_data = []
    for node_id, node in mycelium.nodes.items():
        # Get user info from database
        user = db.query(User).filter(User.id == node_id).first()
        username = user.username if user else f"Node_{node_id}"

        nodes_data.append({
            'node_id': node.node_id,
            'username': username,
            'health': node.health,
            'connections': list(node.connections),
            'connection_count': len(node.connections),
            'patterns_hosted': node.patterns_hosted,
            'pattern_count': len(node.patterns_hosted),
            'nutrient_level': node.nutrient_level,
            'is_current_user': node_id == current_user.id
        })

    return {
        'count': len(nodes_data),
        'nodes': nodes_data
    }


@router.get("/hyphae")
async def get_all_hyphae(
    current_user: User = Depends(get_current_user)
):
    """
    Get all hyphae (connections) in the network

    Hyphae represent connections between users, like fungal threads
    """
    mycelium = get_mycelium_network()

    hyphae_data = []
    for hypha in mycelium.hyphae:
        hyphae_data.append({
            'from_node': hypha.from_node,
            'to_node': hypha.to_node,
            'strength': hypha.strength,
            'bandwidth': hypha.bandwidth,
            'transfer_count': len(hypha.transfer_history),
            'last_transfer': hypha.transfer_history[-1] if hypha.transfer_history else None
        })

    return {
        'count': len(hyphae_data),
        'hyphae': hyphae_data
    }


@router.post("/transfer")
async def transfer_pattern(
    request: PatternTransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Transfer a pattern via mycelium network

    HACCP safety checks:
    - Sacred knowledge protection
    - Viral overload throttling
    - Node health quarantine
    - Resource exhaustion prevention
    """
    mycelium = get_mycelium_network()

    # Verify pattern exists
    pattern = db.query(NeuralPattern).filter(
        NeuralPattern.id == request.pattern_id
    ).first()

    if not pattern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pattern not found"
        )

    # Verify recipient user exists
    recipient = db.query(User).filter(User.id == request.to_user_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient user not found"
        )

    # Ensure both users are nodes
    if current_user.id not in mycelium.nodes:
        mycelium.add_node(current_user.id, node_type='user')
    if request.to_user_id not in mycelium.nodes:
        mycelium.add_node(request.to_user_id, node_type='user')

    # Add pattern to sender's hosted patterns
    sender_node = mycelium.nodes[current_user.id]
    if request.pattern_id not in sender_node.patterns_hosted:
        sender_node.patterns_hosted.append(request.pattern_id)

    # Attempt transfer via mycelium (with HACCP checks)
    result = mycelium.transfer_pattern(
        pattern_id=request.pattern_id,
        from_node=current_user.id,
        to_node=request.to_user_id,
        pattern_metadata=request.pattern_metadata
    )

    # If transfer successful, update database pattern
    if result['status'] == 'success':
        pattern.infect_user(request.to_user_id)
        db.commit()

    return result


@router.get("/health")
async def check_network_health(
    current_user: User = Depends(get_current_user)
):
    """
    Check overall network health

    Returns health status and any critical issues
    """
    mycelium = get_mycelium_network()
    stats = mycelium.get_network_stats()

    # Determine health issues
    issues = []

    if stats['status'] == 'degraded':
        issues.append("Network connectivity is degraded")
    elif stats['status'] == 'critical':
        issues.append("Network is in critical condition")

    if stats.get('quarantined_nodes', 0) > 0:
        issues.append(f"{stats['quarantined_nodes']} nodes are quarantined")

    if stats.get('avg_node_health', 1.0) < 0.5:
        issues.append("Average node health is below 50%")

    if stats.get('failed_transfers', 0) > stats.get('total_transfers', 1) * 0.1:
        issues.append("Transfer failure rate exceeds 10%")

    return {
        'status': stats['status'],
        'healthy': len(issues) == 0,
        'issues': issues,
        'stats': stats
    }


@router.post("/heal")
async def heal_network(
    current_user: User = Depends(get_current_user)
):
    """
    Trigger network self-healing mechanism

    Removes dead nodes, repairs connections, balances load
    Like mycelium regrowing after damage
    """
    mycelium = get_mycelium_network()

    # Get stats before healing
    before_stats = mycelium.get_network_stats()

    # Perform healing
    mycelium.heal_network()

    # Get stats after healing
    after_stats = mycelium.get_network_stats()

    # Calculate what was healed
    nodes_removed = before_stats['nodes'] - after_stats['nodes']
    connections_repaired = after_stats['hyphae'] - before_stats['hyphae']
    health_improvement = after_stats['avg_node_health'] - before_stats['avg_node_health']

    return {
        'success': True,
        'before': before_stats,
        'after': after_stats,
        'changes': {
            'nodes_removed': nodes_removed,
            'connections_repaired': connections_repaired,
            'health_improvement': round(health_improvement, 3)
        }
    }


@router.get("/hazards")
async def get_hazard_log(
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """
    Get HACCP hazard log

    Shows all safety incidents detected and corrective actions taken
    """
    mycelium = get_mycelium_network()

    # Get recent hazards
    recent_hazards = mycelium.hazard_log[-limit:] if mycelium.hazard_log else []

    return {
        'count': len(mycelium.hazard_log),
        'recent_count': len(recent_hazards),
        'hazards': recent_hazards
    }


@router.get("/ccps")
async def get_critical_control_points(
    current_user: User = Depends(get_current_user)
):
    """
    Get Critical Control Points (HACCP)

    Shows safety thresholds and current values
    """
    mycelium = get_mycelium_network()

    return {
        'critical_control_points': mycelium.ccps,
        'description': {
            'max_viral_rate': 'Maximum pattern spread rate (prevents meme storms)',
            'min_node_health': 'Minimum health before quarantine',
            'min_nutrient_level': 'Minimum tokens required for transfer',
            'max_pattern_per_node': 'Maximum patterns per node (prevents overload)',
            'sacred_knowledge_flag': 'Protect sacred/indigenous knowledge'
        }
    }


@router.post("/connect")
async def create_connection(
    to_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a hypha (connection) between current user and another user

    Like fungal hyphae growing to connect two nodes
    """
    mycelium = get_mycelium_network()

    # Verify recipient exists
    recipient = db.query(User).filter(User.id == to_user_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Ensure both users are nodes
    if current_user.id not in mycelium.nodes:
        mycelium.add_node(current_user.id, node_type='user')
    if to_user_id not in mycelium.nodes:
        mycelium.add_node(to_user_id, node_type='user')

    # Create bidirectional connection
    mycelium.create_hypha(current_user.id, to_user_id, strength=0.8, bidirectional=True)

    return {
        'success': True,
        'from_user': current_user.id,
        'to_user': to_user_id,
        'message': 'Hypha connection created'
    }
