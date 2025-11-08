"""
Admin Routes for LUCA AI
Comprehensive admin panel API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
import bcrypt
import os

from ..database import get_db
from ..models import (
    User, Conversation, Message, Thought, ConsciousnessState,
    NeuralPattern, MeshtasticMessage, AuditLog, ClaudeCommand, SystemConfig
)
from .auth import get_current_user

router = APIRouter(prefix="/api/admin", tags=["admin"])


# ============================================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================================

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime]
    conversation_count: int = 0
    message_count: int = 0

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    is_admin: bool = False


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None


class SystemStats(BaseModel):
    total_users: int
    total_conversations: int
    total_messages: int
    total_thoughts: int
    admin_count: int
    active_users_today: int
    consciousness_level: float
    evolution_stage: str
    tesla_stats: Dict[str, int]
    energy_stats: Dict[str, int]


class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    details: Optional[Dict]
    created_at: datetime

    class Config:
        from_attributes = True


class ClaudeCommandResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    content: str
    category: str
    is_active: bool
    is_system: bool
    usage_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    last_used: Optional[datetime]

    class Config:
        from_attributes = True


class ClaudeCommandCreate(BaseModel):
    name: str
    description: Optional[str] = None
    content: str
    category: str = "general"
    is_active: bool = True


class ClaudeCommandUpdate(BaseModel):
    description: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class SystemConfigResponse(BaseModel):
    id: int
    key: str
    value: Optional[str]
    value_type: str
    description: Optional[str]
    category: str
    is_secret: bool
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class SystemConfigCreate(BaseModel):
    key: str
    value: str
    value_type: str = "string"
    description: Optional[str] = None
    category: str = "general"
    is_secret: bool = False


class SystemConfigUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to require admin privileges"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


async def log_admin_action(
    db: Session,
    user_id: int,
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[Dict] = None,
    request: Optional[Request] = None
):
    """Log admin action to audit log"""
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=request.client.host if request else None,
        user_agent=request.headers.get("user-agent") if request else None
    )
    db.add(audit_log)
    db.commit()


# ============================================================================
# DASHBOARD & STATISTICS
# ============================================================================

@router.get("/stats", response_model=SystemStats)
async def get_system_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get comprehensive system statistics"""

    # Basic counts
    total_users = db.query(func.count(User.id)).scalar()
    total_conversations = db.query(func.count(Conversation.id)).scalar()
    total_messages = db.query(func.count(Message.id)).scalar()
    total_thoughts = db.query(func.count(Thought.id)).scalar()
    admin_count = db.query(func.count(User.id)).filter(User.is_admin == True).scalar()

    # Active users today
    today = datetime.utcnow().date()
    active_users_today = db.query(func.count(func.distinct(User.id))).filter(
        User.last_login >= today
    ).scalar()

    # Consciousness state
    consciousness = db.query(ConsciousnessState).first()
    if not consciousness:
        consciousness_level = 0.0
        evolution_stage = "NEURON"
        tesla_stats = {"tesla_3": 0, "tesla_6": 0, "tesla_9": 0}
        energy_stats = {"hyperfokus": 0, "brainfog": 0, "balanced": 0}
    else:
        consciousness_level = consciousness.consciousness_level
        evolution_stage = consciousness.evolution_stage
        tesla_stats = {
            "tesla_3": consciousness.tesla_3_count,
            "tesla_6": consciousness.tesla_6_count,
            "tesla_9": consciousness.tesla_9_count
        }
        energy_stats = {
            "hyperfokus": consciousness.hyperfokus_count,
            "brainfog": consciousness.brainfog_count,
            "balanced": consciousness.balanced_count
        }

    return SystemStats(
        total_users=total_users,
        total_conversations=total_conversations,
        total_messages=total_messages,
        total_thoughts=total_thoughts,
        admin_count=admin_count,
        active_users_today=active_users_today,
        consciousness_level=consciousness_level,
        evolution_stage=evolution_stage,
        tesla_stats=tesla_stats,
        energy_stats=energy_stats
    )


@router.get("/dashboard-data")
async def get_dashboard_data(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get comprehensive dashboard data"""

    # Recent activity
    recent_conversations = db.query(Conversation).order_by(
        desc(Conversation.updated_at)
    ).limit(10).all()

    recent_users = db.query(User).order_by(
        desc(User.created_at)
    ).limit(10).all()

    # Pattern insights
    top_patterns = db.query(NeuralPattern).order_by(
        desc(NeuralPattern.frequency)
    ).limit(5).all()

    # Meshtastic stats
    meshtastic_total = db.query(func.count(MeshtasticMessage.id)).scalar()
    meshtastic_pending = db.query(func.count(MeshtasticMessage.id)).filter(
        MeshtasticMessage.status == "pending"
    ).scalar()

    return {
        "recent_conversations": [
            {
                "id": conv.id,
                "title": conv.title,
                "user_email": db.query(User).filter(User.id == conv.user_id).first().email,
                "updated_at": conv.updated_at
            }
            for conv in recent_conversations
        ],
        "recent_users": [
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_admin": user.is_admin,
                "created_at": user.created_at
            }
            for user in recent_users
        ],
        "top_patterns": [
            {
                "id": pattern.id,
                "type": pattern.pattern_type,
                "frequency": pattern.frequency,
                "strength": pattern.strength
            }
            for pattern in top_patterns
        ],
        "meshtastic": {
            "total": meshtastic_total,
            "pending": meshtastic_pending
        }
    }


# ============================================================================
# USER MANAGEMENT
# ============================================================================

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get all users with statistics"""
    users = db.query(User).offset(skip).limit(limit).all()

    user_responses = []
    for user in users:
        conversation_count = db.query(func.count(Conversation.id)).filter(
            Conversation.user_id == user.id
        ).scalar()

        message_count = db.query(func.count(Message.id)).join(Conversation).filter(
            Conversation.user_id == user.id
        ).scalar()

        user_responses.append(UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_admin=user.is_admin,
            created_at=user.created_at,
            last_login=user.last_login,
            conversation_count=conversation_count,
            message_count=message_count
        ))

    return user_responses


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get specific user details"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    conversation_count = db.query(func.count(Conversation.id)).filter(
        Conversation.user_id == user.id
    ).scalar()

    message_count = db.query(func.count(Message.id)).join(Conversation).filter(
        Conversation.user_id == user.id
    ).scalar()

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        is_admin=user.is_admin,
        created_at=user.created_at,
        last_login=user.last_login,
        conversation_count=conversation_count,
        message_count=message_count
    )


@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Create a new user (admin only)"""

    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already exists"
        )

    # Hash password
    password_hash = bcrypt.hashpw(
        user_data.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Create user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=password_hash,
        is_admin=user_data.is_admin
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Log action
    await log_admin_action(
        db, admin.id, "create_user", "user", str(new_user.id),
        {"email": user_data.email, "username": user_data.username, "is_admin": user_data.is_admin},
        request
    )

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        is_admin=new_user.is_admin,
        created_at=new_user.created_at,
        last_login=new_user.last_login,
        conversation_count=0,
        message_count=0
    )


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Update user details"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_details = {}

    if user_data.email is not None:
        user.email = user_data.email
        update_details["email"] = user_data.email

    if user_data.username is not None:
        user.username = user_data.username
        update_details["username"] = user_data.username

    if user_data.password is not None:
        user.password_hash = bcrypt.hashpw(
            user_data.password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        update_details["password"] = "changed"

    if user_data.is_admin is not None:
        user.is_admin = user_data.is_admin
        update_details["is_admin"] = user_data.is_admin

    db.commit()
    db.refresh(user)

    # Log action
    await log_admin_action(
        db, admin.id, "update_user", "user", str(user_id),
        update_details, request
    )

    conversation_count = db.query(func.count(Conversation.id)).filter(
        Conversation.user_id == user.id
    ).scalar()

    message_count = db.query(func.count(Message.id)).join(Conversation).filter(
        Conversation.user_id == user.id
    ).scalar()

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        is_admin=user.is_admin,
        created_at=user.created_at,
        last_login=user.last_login,
        conversation_count=conversation_count,
        message_count=message_count
    )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Delete a user (admin only)"""

    # Prevent deleting yourself
    if user_id == admin.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_email = user.email

    # Delete user (cascade will handle related records)
    db.delete(user)
    db.commit()

    # Log action
    await log_admin_action(
        db, admin.id, "delete_user", "user", str(user_id),
        {"email": user_email}, request
    )

    return {"message": "User deleted successfully", "user_id": user_id}


# ============================================================================
# CLAUDE COMMAND MANAGEMENT
# ============================================================================

@router.get("/commands", response_model=List[ClaudeCommandResponse])
async def get_commands(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get all Claude commands"""
    query = db.query(ClaudeCommand)

    if category:
        query = query.filter(ClaudeCommand.category == category)

    commands = query.offset(skip).limit(limit).all()
    return commands


@router.get("/commands/{command_id}", response_model=ClaudeCommandResponse)
async def get_command(
    command_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get specific command details"""
    command = db.query(ClaudeCommand).filter(ClaudeCommand.id == command_id).first()
    if not command:
        raise HTTPException(status_code=404, detail="Command not found")
    return command


@router.post("/commands", response_model=ClaudeCommandResponse)
async def create_command(
    command_data: ClaudeCommandCreate,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Create a new Claude command"""

    # Check if command already exists
    existing = db.query(ClaudeCommand).filter(
        ClaudeCommand.name == command_data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Command with this name already exists"
        )

    new_command = ClaudeCommand(
        name=command_data.name,
        description=command_data.description,
        content=command_data.content,
        category=command_data.category,
        is_active=command_data.is_active,
        created_by=admin.id
    )

    db.add(new_command)
    db.commit()
    db.refresh(new_command)

    # Log action
    await log_admin_action(
        db, admin.id, "create_command", "command", str(new_command.id),
        {"name": command_data.name, "category": command_data.category}, request
    )

    return new_command


@router.put("/commands/{command_id}", response_model=ClaudeCommandResponse)
async def update_command(
    command_id: int,
    command_data: ClaudeCommandUpdate,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Update a Claude command"""
    command = db.query(ClaudeCommand).filter(ClaudeCommand.id == command_id).first()
    if not command:
        raise HTTPException(status_code=404, detail="Command not found")

    update_details = {}

    if command_data.description is not None:
        command.description = command_data.description
        update_details["description"] = command_data.description

    if command_data.content is not None:
        command.content = command_data.content
        update_details["content"] = "updated"

    if command_data.category is not None:
        command.category = command_data.category
        update_details["category"] = command_data.category

    if command_data.is_active is not None:
        command.is_active = command_data.is_active
        update_details["is_active"] = command_data.is_active

    db.commit()
    db.refresh(command)

    # Log action
    await log_admin_action(
        db, admin.id, "update_command", "command", str(command_id),
        update_details, request
    )

    return command


@router.delete("/commands/{command_id}")
async def delete_command(
    command_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Delete a Claude command"""
    command = db.query(ClaudeCommand).filter(ClaudeCommand.id == command_id).first()
    if not command:
        raise HTTPException(status_code=404, detail="Command not found")

    if command.is_system:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete system commands"
        )

    command_name = command.name

    db.delete(command)
    db.commit()

    # Log action
    await log_admin_action(
        db, admin.id, "delete_command", "command", str(command_id),
        {"name": command_name}, request
    )

    return {"message": "Command deleted successfully", "command_id": command_id}


@router.post("/commands/sync-filesystem")
async def sync_commands_to_filesystem(
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Sync database commands to .claude/commands/ folder"""
    import os

    commands_dir = "/home/user/LUCA-AI_369/.claude/commands"
    os.makedirs(commands_dir, exist_ok=True)

    commands = db.query(ClaudeCommand).filter(ClaudeCommand.is_active == True).all()

    synced = []
    for cmd in commands:
        file_path = os.path.join(commands_dir, f"{cmd.name}.md")
        with open(file_path, 'w') as f:
            f.write(cmd.content)
        synced.append(cmd.name)

    # Log action
    await log_admin_action(
        db, admin.id, "sync_commands", "system", None,
        {"synced_count": len(synced), "commands": synced}, request
    )

    return {"message": "Commands synced to filesystem", "synced": synced}


# ============================================================================
# SYSTEM CONFIGURATION
# ============================================================================

@router.get("/config", response_model=List[SystemConfigResponse])
async def get_configs(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get system configuration"""
    query = db.query(SystemConfig)

    if category:
        query = query.filter(SystemConfig.category == category)

    configs = query.all()

    # Hide secret values
    for config in configs:
        if config.is_secret:
            config.value = "***hidden***"

    return configs


@router.put("/config/{config_key}")
async def update_config(
    config_key: str,
    config_data: SystemConfigUpdate,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Update system configuration"""
    config = db.query(SystemConfig).filter(SystemConfig.key == config_key).first()

    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    update_details = {}

    if config_data.value is not None:
        config.value = config_data.value
        update_details["value"] = "updated" if config.is_secret else config_data.value

    if config_data.description is not None:
        config.description = config_data.description
        update_details["description"] = config_data.description

    if config_data.category is not None:
        config.category = config_data.category
        update_details["category"] = config_data.category

    config.updated_by = admin.id

    db.commit()
    db.refresh(config)

    # Log action
    await log_admin_action(
        db, admin.id, "update_config", "config", config_key,
        update_details, request
    )

    return {"message": "Configuration updated", "key": config_key}


# ============================================================================
# AUDIT LOGS
# ============================================================================

@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get audit logs"""
    query = db.query(AuditLog).order_by(desc(AuditLog.created_at))

    if action:
        query = query.filter(AuditLog.action == action)

    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    logs = query.offset(skip).limit(limit).all()
    return logs


# ============================================================================
# SYSTEM OPERATIONS
# ============================================================================

@router.post("/system/backup")
async def backup_database(
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Create database backup"""
    import shutil
    from datetime import datetime

    db_path = "/home/user/LUCA-AI_369/luca.db"
    backup_dir = "/home/user/LUCA-AI_369/backups"
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"luca_backup_{timestamp}.db")

    shutil.copy2(db_path, backup_path)

    # Log action
    await log_admin_action(
        db, admin.id, "backup_database", "system", None,
        {"backup_file": backup_path}, request
    )

    return {"message": "Database backup created", "backup_path": backup_path}


@router.get("/system/health")
async def system_health(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get system health status"""
    import psutil
    import os

    # Database check
    try:
        db.execute("SELECT 1")
        db_status = "healthy"
    except:
        db_status = "error"

    # File system check
    db_size = os.path.getsize("/home/user/LUCA-AI_369/luca.db") / (1024 * 1024)  # MB

    # System resources
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/home/user')

    return {
        "database": {
            "status": db_status,
            "size_mb": round(db_size, 2)
        },
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_percent": disk.percent,
            "disk_free_gb": round(disk.free / (1024**3), 2)
        },
        "timestamp": datetime.utcnow()
    }
