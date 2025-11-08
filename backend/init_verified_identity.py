"""
Initialize Verified Identity Database Tables

Run this script to add verified identity tables to your existing LUCA database.
This will NOT delete existing data.

Usage:
    python -m backend.init_verified_identity
"""

import sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from backend.database import Base, SQLALCHEMY_DATABASE_URL
from backend.models import User  # Import existing models
from backend.models_verified_identity import (  # Import new models
    UserIdentity,
    GlobalKnowledge,
    KnowledgeCorrectionLog,
    CommunityValidation,
    VerificationRequest
)


def init_verified_identity_tables():
    """Initialize verified identity tables"""
    print("🔐 LUCA Verified Identity Initialization")
    print("=" * 50)

    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    inspector = inspect(engine)

    # Get existing tables
    existing_tables = inspector.get_table_names()
    print(f"\n📊 Existing tables: {len(existing_tables)}")
    for table in existing_tables:
        print(f"  ✓ {table}")

    # Import all models to ensure they're registered
    from backend.models_verified_identity import Base as IdentityBase

    # Create new tables (will skip existing ones)
    print("\n🔨 Creating verified identity tables...")

    new_tables = [
        "user_identities",
        "global_knowledge",
        "knowledge_correction_logs",
        "community_validations",
        "verification_requests"
    ]

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Check what was created
    print("\n✅ Verification complete!")
    all_tables = inspector.get_table_names()
    print(f"\n📊 Total tables: {len(all_tables)}")

    for table in new_tables:
        if table in all_tables:
            print(f"  ✓ {table} - Ready")
        else:
            print(f"  ✗ {table} - Not found")

    print("\n" + "=" * 50)
    print("🎉 Verified Identity system initialized!")
    print("\nNext steps:")
    print("1. Restart your LUCA backend")
    print("2. Users can now verify their identities")
    print("3. Verified users can update global knowledge")
    print("4. Check admin dashboard for verification requests")
    print("\nDocumentation: See VERIFIED_IDENTITY.md")


if __name__ == "__main__":
    try:
        init_verified_identity_tables()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
