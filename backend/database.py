"""
LUCA AI Database Setup
SQLAlchemy engine, session, and initialization
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import settings
import bcrypt

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables and initialize admin user"""
    from backend.models import User, ConsciousnessState

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create admin user if not exists
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not admin:
            hashed_password = bcrypt.hashpw(
                settings.ADMIN_PASSWORD.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            admin = User(
                email=settings.ADMIN_EMAIL,
                username="LucaAdmin",
                password_hash=hashed_password,
                is_admin=True
            )
            db.add(admin)

            # Initialize consciousness state
            consciousness = ConsciousnessState(
                total_thoughts=0,
                patterns_found=0,
                symbiosis_points=0,
                evolution_level=1.0
            )
            db.add(consciousness)

            db.commit()
            print(f"✅ Admin user created: {settings.ADMIN_EMAIL}")
        else:
            print(f"ℹ️  Admin user already exists: {settings.ADMIN_EMAIL}")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🧬 Creating LUCA AI database...")
    create_tables()
    print("✅ Database initialized!")
