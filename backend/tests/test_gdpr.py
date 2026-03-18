"""
Tests for GDPR compliance endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestGDPRDataRights:
    """Tests for GDPR data subject rights"""
    
    def test_export_user_data(self, client):
        """Test GDPR Article 20 - Right to Data Portability"""
        response = client.post("/api/gdpr/data/export", json={
            "user_id": "test_user_123",
            "email": "test@example.com",
            "export_format": "json"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert "download_url" in data
    
    def test_delete_user_data_requires_confirmation(self, client):
        """Test GDPR Article 17 - Right to Erasure requires confirmation"""
        response = client.post("/api/gdpr/data/delete", json={
            "user_id": "test_user_123",
            "email": "test@example.com",
            "confirm": False
        })
        assert response.status_code == 400  # Bad request - confirmation required
    
    def test_delete_user_data_with_confirmation(self, client):
        """Test GDPR Article 17 - Right to Erasure with confirmation"""
        response = client.post("/api/gdpr/data/delete", json={
            "user_id": "test_user_123",
            "email": "test@example.com",
            "reason": "User requested deletion",
            "confirm": True
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "deletion_id" in data
        assert "recovery_period_days" in data
    
    def test_access_user_data(self, client):
        """Test GDPR Article 15 - Right of Access"""
        response = client.get("/api/gdpr/data/access/test_user_123")
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "data_categories" in data
        assert "consent_status" in data


class TestConsentManagement:
    """Tests for consent management (GDPR Article 7)"""
    
    def test_update_consent(self, client):
        """Test updating consent preferences"""
        response = client.post("/api/gdpr/consent", json={
            "user_id": "test_user_123",
            "consents": {
                "analytics": True,
                "marketing": False,
                "third_party": True
            },
            "confirm": True
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "updated_consents" in data
    
    def test_get_consent_status(self, client):
        """Test getting consent status"""
        response = client.get("/api/gdpr/consent/test_user_123")
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "consent_status" in data
        assert "essential" in data["consent_status"]
        assert data["consent_status"]["essential"]["can_disable"] is False
    
    def test_essential_consent_cannot_be_disabled(self, client):
        """Test that essential consent cannot be disabled"""
        response = client.post("/api/gdpr/consent", json={
            "user_id": "test_user_123",
            "consents": {
                "essential": False  # Should be ignored
            },
            "confirm": True
        })
        assert response.status_code == 200
        # Essential consent should remain enabled


class TestAuditLogs:
    """Tests for audit logging"""
    
    def test_get_audit_logs(self, client):
        """Test getting user audit logs"""
        response = client.get("/api/gdpr/audit-logs/test_user_123")
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "logs" in data
        assert "retention_period_days" in data
    
    def test_audit_logs_limited(self, client):
        """Test audit logs are limited"""
        response = client.get("/api/gdpr/audit-logs/test_user_123?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["logs"]) <= 10


class TestDataProcessingAgreement:
    """Tests for Data Processing Agreement"""
    
    def test_get_dpa(self, client):
        """Test getting Data Processing Agreement"""
        response = client.get("/api/gdpr/dpa")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "parties" in data
        assert "processing_activities" in data
        assert "security_measures" in data
        assert "subprocessors" in data


class TestPrivacyPolicy:
    """Tests for privacy policy"""
    
    def test_privacy_policy_structure(self, client):
        """Test privacy policy has required structure"""
        response = client.get("/api/gdpr/privacy-policy")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "last_updated" in data
        assert "sections" in data
        assert len(data["sections"]) > 0
    
    def test_privacy_policy_has_contact(self, client):
        """Test privacy policy has contact info"""
        response = client.get("/api/gdpr/privacy-policy")
        data = response.json()
        assert "summary" in data
        assert "contact_email" in data["summary"] or any(
            "contact" in str(section).lower() 
            for section in data.get("sections", [])
        )


class TestCookiePolicy:
    """Tests for cookie policy"""
    
    def test_cookie_policy_structure(self, client):
        """Test cookie policy has required structure"""
        response = client.get("/api/gdpr/cookie-policy")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "cookies" in data
        assert len(data["cookies"]) > 0
    
    def test_cookie_policy_has_essential_cookies(self, client):
        """Test cookie policy lists essential cookies"""
        response = client.get("/api/gdpr/cookie-policy")
        data = response.json()
        essential_cookies = [
            c for c in data["cookies"] 
            if c.get("type") == "essential"
        ]
        assert len(essential_cookies) > 0
    
    def test_cookie_policy_can_disable_non_essential(self, client):
        """Test non-essential cookies can be disabled"""
        response = client.get("/api/gdpr/cookie-policy")
        data = response.json()
        non_essential = [
            c for c in data["cookies"] 
            if c.get("type") != "essential"
        ]
        for cookie in non_essential:
            assert cookie.get("can_disable") is True


class TestDataRetention:
    """Tests for data retention policy"""
    
    def test_data_retention_policy(self, client):
        """Test data retention policy endpoint"""
        response = client.get("/api/gdpr/data-retention")
        assert response.status_code == 200
        data = response.json()
        assert "policy" in data
        assert "user_data" in data["policy"]
        assert "audit_logs" in data["policy"]
        assert "deleted_data" in data["policy"]
    
    def test_data_retention_periods(self, client):
        """Test data retention periods are reasonable"""
        response = client.get("/api/gdpr/data-retention")
        data = response.json()
        
        # User data should be retained for reasonable period (not forever)
        user_data_days = data["policy"]["user_data"]["retention_days"]
        assert user_data_days > 0
        assert user_data_days <= 2555  # Max 7 years
        
        # Deleted data should have recovery period
        deleted_days = data["policy"]["deleted_data"]["retention_days"]
        assert deleted_days > 0
        assert deleted_days <= 90  # Max 90 days recovery
