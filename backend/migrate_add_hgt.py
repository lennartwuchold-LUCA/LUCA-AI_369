"""
Database Migration: Add Horizontal Gene Transfer (HGT) fields to NeuralPattern

This script safely adds the new HGT tracking fields to existing databases.
Works with both SQLite and MySQL.

Run this ONCE after pulling the HGT update.
"""

from sqlalchemy import create_engine, inspect, text
from backend.config import DATABASE_URL
import sys

def migrate_add_hgt_fields():
    """
    Add HGT fields to neural_patterns table if they don't exist

    New fields:
    - first_detected_user_id (INT, nullable, FK to users.id)
    - users_expressing_pattern (JSON, default [])
    - transfer_count (INT, default 0)
    """
    print("🧬 Starting HGT Migration...")
    print(f"Database: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")

    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)

    # Check if neural_patterns table exists
    if 'neural_patterns' not in inspector.get_table_names():
        print("⚠️  neural_patterns table doesn't exist yet - no migration needed")
        print("   Run: python backend/database.py first")
        return

    # Get existing columns
    existing_columns = [col['name'] for col in inspector.get_columns('neural_patterns')]
    print(f"📋 Existing columns: {existing_columns}")

    # Determine which fields need to be added
    fields_to_add = []

    if 'first_detected_user_id' not in existing_columns:
        fields_to_add.append('first_detected_user_id')

    if 'users_expressing_pattern' not in existing_columns:
        fields_to_add.append('users_expressing_pattern')

    if 'transfer_count' not in existing_columns:
        fields_to_add.append('transfer_count')

    if not fields_to_add:
        print("✅ All HGT fields already exist - no migration needed!")
        return

    print(f"➕ Adding fields: {fields_to_add}")

    # Connect and add fields
    with engine.connect() as conn:
        # Detect database type
        is_mysql = 'mysql' in DATABASE_URL.lower()

        # Add first_detected_user_id
        if 'first_detected_user_id' in fields_to_add:
            try:
                if is_mysql:
                    conn.execute(text("""
                        ALTER TABLE neural_patterns
                        ADD COLUMN first_detected_user_id INT NULL,
                        ADD FOREIGN KEY (first_detected_user_id) REFERENCES users(id)
                    """))
                else:  # SQLite
                    conn.execute(text("""
                        ALTER TABLE neural_patterns
                        ADD COLUMN first_detected_user_id INTEGER
                    """))
                conn.commit()
                print("   ✅ Added first_detected_user_id")
            except Exception as e:
                print(f"   ⚠️  first_detected_user_id: {e}")

        # Add users_expressing_pattern
        if 'users_expressing_pattern' in fields_to_add:
            try:
                if is_mysql:
                    conn.execute(text("""
                        ALTER TABLE neural_patterns
                        ADD COLUMN users_expressing_pattern JSON
                    """))
                else:  # SQLite (stores JSON as TEXT)
                    conn.execute(text("""
                        ALTER TABLE neural_patterns
                        ADD COLUMN users_expressing_pattern TEXT DEFAULT '[]'
                    """))
                conn.commit()
                print("   ✅ Added users_expressing_pattern")
            except Exception as e:
                print(f"   ⚠️  users_expressing_pattern: {e}")

        # Add transfer_count
        if 'transfer_count' in fields_to_add:
            try:
                if is_mysql:
                    conn.execute(text("""
                        ALTER TABLE neural_patterns
                        ADD COLUMN transfer_count INT DEFAULT 0
                    """))
                else:  # SQLite
                    conn.execute(text("""
                        ALTER TABLE neural_patterns
                        ADD COLUMN transfer_count INTEGER DEFAULT 0
                    """))
                conn.commit()
                print("   ✅ Added transfer_count")
            except Exception as e:
                print(f"   ⚠️  transfer_count: {e}")

    # Verify migration
    inspector = inspect(engine)
    new_columns = [col['name'] for col in inspector.get_columns('neural_patterns')]
    print(f"\n📋 Updated columns: {new_columns}")

    # Check all HGT fields present
    hgt_fields = ['first_detected_user_id', 'users_expressing_pattern', 'transfer_count']
    all_present = all(field in new_columns for field in hgt_fields)

    if all_present:
        print("\n🎉 HGT Migration Complete!")
        print("   All horizontal gene transfer fields added successfully")
        print("\n📊 What changed:")
        print("   - Patterns now track original 'donor' user")
        print("   - Patterns track all users who express them")
        print("   - Transfer rate can be calculated (viral vs. endemic patterns)")
    else:
        missing = [f for f in hgt_fields if f not in new_columns]
        print(f"\n⚠️  Migration incomplete - missing fields: {missing}")
        print("   You may need to drop and recreate the database")
        print("   Backup first: python scripts/backup_mysql.sh")

    engine.dispose()

if __name__ == "__main__":
    try:
        migrate_add_hgt_fields()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure database is running")
        print("2. Check DATABASE_URL in .env")
        print("3. Backup data before trying again")
        sys.exit(1)
