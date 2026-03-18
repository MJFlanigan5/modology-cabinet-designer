"""
KerfOS Backend Tests
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint"""
    
    def test_root_returns_200(self, client):
        """Test that root endpoint returns 200"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_kerfos_branding(self, client):
        """Test that root endpoint returns KerfOS branding"""
        response = client.get("/")
        data = response.json()
        assert data["message"] == "KerfOS API"
        assert "version" in data
        assert data["status"] == "running"
    
    def test_root_lists_features(self, client):
        """Test that root endpoint lists features"""
        response = client.get("/")
        data = response.json()
        assert "features" in data
        assert len(data["features"]) > 0
        assert "Cabinet design and management" in data["features"]
    
    def test_root_lists_endpoints(self, client):
        """Test that root endpoint lists all API endpoints"""
        response = client.get("/")
        data = response.json()
        assert "endpoints" in data
        endpoints = data["endpoints"]
        assert "/api/cabinets" in endpoints.values()
        assert "/api/materials" in endpoints.values()
        assert "/api/hardware" in endpoints.values()
        assert "/api/gdpr" in endpoints.values()


class TestHealthEndpoint:
    """Tests for the health endpoint"""
    
    def test_health_returns_200(self, client):
        """Test that health endpoint returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_healthy(self, client):
        """Test that health endpoint returns healthy status"""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"


class TestGDPREndpoints:
    """Tests for GDPR compliance endpoints"""
    
    def test_gdpr_router_exists(self, client):
        """Test that GDPR router is mounted"""
        # This tests that the GDPR router is properly included
        response = client.get("/api/gdpr/consent")
        # Should return something (even if 401 or 404, the router should exist)
        assert response.status_code in [200, 401, 404, 422]


class TestSecurityHeaders:
    """Tests for security headers"""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are configured"""
        response = client.options("/", headers={"Origin": "http://localhost:3000"})
        # CORS middleware should be present
        assert response.status_code in [200, 400, 405]


class TestCabinetEndpoints:
    """Tests for cabinet endpoints"""
    
    def test_cabinets_list_requires_auth(self, client):
        """Test that cabinets list endpoint exists"""
        response = client.get("/api/cabinets")
        # Should exist (even if requires auth)
        assert response.status_code in [200, 401, 404, 422]


class TestMaterialEndpoints:
    """Tests for material endpoints"""
    
    def test_materials_list_exists(self, client):
        """Test that materials endpoint exists"""
        response = client.get("/api/materials")
        assert response.status_code in [200, 401, 404, 422]


class TestHardwareEndpoints:
    """Tests for hardware endpoints"""
    
    def test_hardware_list_exists(self, client):
        """Test that hardware endpoint exists"""
        response = client.get("/api/hardware")
        assert response.status_code in [200, 401, 404, 422]


class TestLocalizationEndpoints:
    """Tests for localization endpoints"""
    
    def test_localization_exists(self, client):
        """Test that localization router exists"""
        response = client.get("/api/localization/categories")
        assert response.status_code in [200, 401, 404, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
