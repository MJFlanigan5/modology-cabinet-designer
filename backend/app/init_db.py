"""
Database initialization script for creating all tables
Run this script once to set up your database schema
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from app.models import Base


def init_database():
    """
    Create all tables in the database.
    This is idempotent - running it multiple times won't cause issues.
    """
    print("Creating database tables...")
    
    # Create all tables defined in models.py
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully!")
    print("\nTables created:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")
    
    print("\nYou can now start using the database.")


if __name__ == "__main__":
    init_database()