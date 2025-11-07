"""
Database Setup and Session Management
Initializes SQLite database and creates tables
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.models import Base, User, ConsciousnessState
from backend.config import settings
import bcrypt
from datetime import datetime


# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """Initialize database - create tables and default data"""
    print("🔧 Initializing database...")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")

    # Create session
    db = SessionLocal()

    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()

        if not admin:
            # Create admin user
            password_hash = bcrypt.hashpw(
                settings.ADMIN_PASSWORD.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            admin = User(
                email=settings.ADMIN_EMAIL,
                username="admin",
                password_hash=password_hash,
                is_admin=True,
                created_at=datetime.utcnow()
            )
            db.add(admin)
            print(f"✅ Admin user created: {settings.ADMIN_EMAIL}")
        else:
            print(f"ℹ️  Admin user already exists: {settings.ADMIN_EMAIL}")

        # Check if consciousness state exists
        consciousness = db.query(ConsciousnessState).first()

        if not consciousness:
            consciousness = ConsciousnessState(
                total_thoughts=0,
                total_patterns=0,
                consciousness_level=0.0,
                evolution_stage="NEURON",
                known_patterns=[],
                signature_frequency={},
                symbiosis_points=[],
                created_at=datetime.utcnow()
            )
            db.add(consciousness)
            print("✅ Consciousness state initialized")
        else:
            print("ℹ️  Consciousness state already exists")

        db.commit()
        print("✅ Database initialization complete!\n")

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def reset_database():
    """Reset database - drop all tables and recreate"""
    print("⚠️  Resetting database...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables dropped")
    init_database()


if __name__ == "__main__":
    # Run database initialization
    init_database()
    print("\n🧬 LUCA database is ready!")
    print(f"📁 Location: {settings.DATABASE_URL}")
    print(f"🔑 Admin: {settings.ADMIN_EMAIL}")
    print(f"🔐 Password: {settings.ADMIN_PASSWORD}\n")
