"""
Test configuration for KerfOS backend
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from main import app


# Test database (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_cabinet_data():
    """Sample cabinet data for testing"""
    return {
        "name": "Test Cabinet",
        "width": 24.0,
        "height": 34.5,
        "depth": 24.0,
        "material": "Plywood",
        "material_thickness": 0.75,
        "style": "shaker",
        "cabinet_type": "base",
        "components": []
    }


@pytest.fixture
def sample_material_data():
    """Sample material data for testing"""
    return {
        "name": "Birch Plywood",
        "type": "plywood",
        "thickness": 0.75,
        "price_per_sqft": 5.99,
        "supplier": "Home Depot"
    }
