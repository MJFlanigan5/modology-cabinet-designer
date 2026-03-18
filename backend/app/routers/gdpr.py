"""GDPR Compliance Router for KerfOS

Implements GDPR data subject rights:
- Right to Access (Article 15)
- Right to Rectification (Article 16)
- Right to Erasure (Article 17)
- Right to Data Portability (Article 20)
- Right to Object (Article 21)
- Consent Management (Article 7)

Also includes:
- Audit logging for compliance
- Data retention policies
- Cookie consent management
"""
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid

router = APIRouter(prefix="/api/gdpr", tags=["GDPR Compliance"])


# ============================================
# MODELS
# ============================================

class ConsentType(str, Enum):
    ESSENTIAL = "essential"  # Required for app to function
    ANALYTICS = "analytics"  # Usage analytics
    MARKETING = "marketing"  # Marketing emails
    THIRD_PARTY = "third_party"  # Third-party integrations


class ConsentStatus(BaseModel):
    consent_id: str
    consent_type: ConsentType
    granted: bool
    granted_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class DataExportRequest(BaseModel):
    user_id: str
    email: str
    export_format: str = "json"  # json, csv
    include_deleted: bool = False


class DataDeletionRequest(BaseModel):
    user_id: str
    email: str
    reason: Optional[str] = None
    confirm: bool = False  # Must be True to proceed


class ConsentUpdateRequest(BaseModel):
    user_id: str
    consents: Dict[str, bool]  # { "analytics": true, "marketing": false }
    confirm: bool = True


class AuditLogEntry(BaseModel):
    log_id: str
    timestamp: datetime
    action: str
    user_id: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    details: Dict[str, Any]
    data_subject_request: bool = False


# ============================================
# IN-MEMORY STORAGE (Replace with Database in Production)
# ============================================

# In production, these would be database tables
_consent_records: Dict[str, List[ConsentStatus]] = {}
_audit_logs: List[AuditLogEntry] = []
_data_retention_days = {
    "user_data": 730,  # 2 years
    "audit_logs": 365,  # 1 year
    "deleted_data": 30,  # 30 days recovery period
}


# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_id() -> str:
    return str(uuid.uuid4())


def log_audit(
    action: str,
    user_id: str,
    request: Request,
    details: Dict[str, Any],
    data_subject_request: bool = False
) -> AuditLogEntry:
    """Create an audit log entry"""
    entry = AuditLogEntry(
        log_id=generate_id(),
        timestamp=datetime.utcnow(),
        action=action,
        user_id=user_id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        details=details,
        data_subject_request=data_subject_request
    )
    _audit_logs.append(entry)
    return entry


def get_user_consents(user_id: str) -> List[ConsentStatus]:
    """Get all consent records for a user"""
    return _consent_records.get(user_id, [])


def has_valid_consent(user_id: str, consent_type: ConsentType) -> bool:
    """Check if user has valid consent for a specific type"""
    consents = get_user_consents(user_id)
    for consent in consents:
        if consent.consent_type == consent_type:
            return consent.granted and consent.revoked_at is None
    return False


# ============================================
# DATA SUBJECT RIGHTS ENDPOINTS
# ============================================

@router.get("/privacy-policy")
async def get_privacy_policy():
    """Return the privacy policy"""
    return {
        "title": "KerfOS Privacy Policy",
        "last_updated": "2026-03-17",
        "version": "1.0.0",
        "policy_url": "https://kerfos.com/privacy",
        "summary": {
            "data_controller": "KerfOS",
            "contact_email": "privacy@kerfos.com",
            "dpo_email": "dpo@kerfos.com",
            "jurisdiction": "United States",
            "gdpr_compliant": True,
            "ccpa_compliant": True,
        },
        "sections": [
            {
                "title": "Data We Collect",
                "content": "We collect account information (name, email), project data (cabinet designs, cut lists), usage analytics, and payment information (processed by Stripe)."
            },
            {
                "title": "How We Use Your Data",
                "content": "Your data is used to provide cabinet design services, process payments, improve our product, and communicate with you about your account."
            },
            {
                "title": "Data Sharing",
                "content": "We share data with Stripe for payments, and analytics providers (with your consent). We never sell your personal data."
            },
            {
                "title": "Your Rights",
                "content": "You have the right to access, correct, delete, and export your data. You can withdraw consent at any time."
            },
            {
                "title": "Data Retention",
                "content": "We retain user data for 2 years after account closure. Audit logs are retained for 1 year. Deleted data has a 30-day recovery period."
            },
            {
                "title": "Security",
                "content": "We use industry-standard encryption, secure coding practices, and regular security audits to protect your data."
            }
        ]
    }


@router.get("/terms-of-service")
async def get_terms_of_service():
    """Return the terms of service"""
    return {
        "title": "KerfOS Terms of Service",
        "last_updated": "2026-03-17",
        "version": "1.0.0",
        "terms_url": "https://kerfos.com/terms",
        "sections": [
            {
                "title": "Acceptance of Terms",
                "content": "By using KerfOS, you agree to these terms of service."
            },
            {
                "title": "Description of Service",
                "content": "KerfOS provides cabinet design software for woodworkers and DIY enthusiasts."
            },
            {
                "title": "User Accounts",
                "content": "You are responsible for maintaining the security of your account and all activities under your account."
            },
            {
                "title": "Payment Terms",
                "content": "Subscriptions are billed monthly or annually. You can cancel at any time."
            },
            {
                "title": "Intellectual Property",
                "content": "You own your designs. KerfOS owns the software and platform."
            },
            {
                "title": "Limitation of Liability",
                "content": "KerfOS is provided as-is. We are not liable for any damages arising from use of the service."
            },
            {
                "title": "Termination",
                "content": "We may terminate accounts that violate these terms. You may delete your account at any time."
            },
            {
                "title": "Governing Law",
                "content": "These terms are governed by the laws of the United States."
            }
        ]
    }


@router.get("/cookie-policy")
async def get_cookie_policy():
    """Return the cookie policy"""
    return {
        "title": "KerfOS Cookie Policy",
        "last_updated": "2026-03-17",
        "version": "1.0.0",
        "policy_url": "https://kerfos.com/cookies",
        "cookies": [
            {
                "name": "session",
                "type": "essential",
                "purpose": "Maintains your login session",
                "duration": "24 hours",
                "can_disable": False
            },
            {
                "name": "preferences",
                "type": "essential",
                "purpose": "Stores your preferences (units, theme)",
                "duration": "1 year",
                "can_disable": False
            },
            {
                "name": "csrf_token",
                "type": "essential",
                "purpose": "Prevents cross-site request forgery",
                "duration": "Session",
                "can_disable": False
            },
            {
                "name": "_ga",
                "type": "analytics",
                "purpose": "Google Analytics - distinguishes users",
                "duration": "2 years",
                "can_disable": True
            },
            {
                "name": "_gid",
                "type": "analytics",
                "purpose": "Google Analytics - distinguishes users",
                "duration": "24 hours",
                "can_disable": True
            }
        ],
        "manage_consent_url": "/api/gdpr/consent"
    }


@router.post("/data/export")
async def export_user_data(request: Request, export_req: DataExportRequest):
    """
    GDPR Article 20 - Right to Data Portability
    
    Export all user data in a machine-readable format.
    """
    # Log the request
    log_audit(
        action="data_export_requested",
        user_id=export_req.user_id,
        request=request,
        details={"format": export_req.export_format},
        data_subject_request=True
    )
    
    # In production, fetch from actual database
    user_data = {
        "export_metadata": {
            "export_id": generate_id(),
            "exported_at": datetime.utcnow().isoformat(),
            "format": export_req.export_format,
            "user_id": export_req.user_id,
        },
        "user_profile": {
            "user_id": export_req.user_id,
            "email": export_req.email,
            "created_at": "2025-01-15T10:00:00Z",
            "last_login": datetime.utcnow().isoformat(),
        },
        "projects": [
            {
                "project_id": "proj_123",
                "name": "Kitchen Renovation",
                "created_at": "2025-02-01T10:00:00Z",
                "cabinets": []
            }
        ],
        "cabinets": [],
        "cut_lists": [],
        "materials": [],
        "consent_history": [c.model_dump() for c in get_user_consents(export_req.user_id)],
        "account_activity": {
            "login_count": 42,
            "projects_created": 5,
            "last_active": datetime.utcnow().isoformat(),
        }
    }
    
    log_audit(
        action="data_export_completed",
        user_id=export_req.user_id,
        request=request,
        details={"export_id": user_data["export_metadata"]["export_id"]},
        data_subject_request=True
    )
    
    return {
        "status": "success",
        "message": "Data export completed",
        "data": user_data,
        "download_url": f"/api/gdpr/data/download/{user_data['export_metadata']['export_id']}",
        "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat(),
    }


@router.post("/data/delete")
async def delete_user_data(request: Request, delete_req: DataDeletionRequest):
    """
    GDPR Article 17 - Right to Erasure (Right to be Forgotten)
    
    Delete all user data.
    """
    if not delete_req.confirm:
        raise HTTPException(
            status_code=400,
            detail="Deletion must be confirmed with confirm=true"
        )
    
    # Log the request
    log_audit(
        action="data_deletion_requested",
        user_id=delete_req.user_id,
        request=request,
        details={"reason": delete_req.reason},
        data_subject_request=True
    )
    
    # In production, perform actual deletion
    # This would delete from all tables and mark for permanent deletion after retention period
    
    deletion_id = generate_id()
    
    log_audit(
        action="data_deletion_completed",
        user_id=delete_req.user_id,
        request=request,
        details={
            "deletion_id": deletion_id,
            "recovery_period_days": _data_retention_days["deleted_data"]
        },
        data_subject_request=True
    )
    
    return {
        "status": "success",
        "message": "Data deletion scheduled",
        "deletion_id": deletion_id,
        "recovery_period_days": _data_retention_days["deleted_data"],
        "permanent_deletion_date": (datetime.utcnow() + timedelta(days=_data_retention_days["deleted_data"])).isoformat(),
        "note": "You can recover your account within the recovery period by contacting support."
    }


@router.get("/data/access/{user_id}")
async def access_user_data(request: Request, user_id: str):
    """
    GDPR Article 15 - Right of Access
    
    Get a summary of what data is stored about the user.
    """
    log_audit(
        action="data_access_requested",
        user_id=user_id,
        request=request,
        details={},
        data_subject_request=True
    )
    
    return {
        "user_id": user_id,
        "data_categories": [
            {
                "category": "account",
                "description": "Account information",
                "data_points": ["email", "name", "created_at"],
                "retention_period_days": _data_retention_days["user_data"]
            },
            {
                "category": "projects",
                "description": "Cabinet design projects",
                "data_points": ["project_name", "cabinets", "materials", "cut_lists"],
                "retention_period_days": _data_retention_days["user_data"]
            },
            {
                "category": "preferences",
                "description": "User preferences",
                "data_points": ["units", "theme", "default_material"],
                "retention_period_days": _data_retention_days["user_data"]
            },
            {
                "category": "consent",
                "description": "Consent records",
                "data_points": ["consent_type", "granted_at", "revoked_at"],
                "retention_period_days": _data_retention_days["audit_logs"]
            },
            {
                "category": "payment",
                "description": "Payment history (via Stripe)",
                "data_points": ["subscription_status", "payment_history"],
                "retention_period_days": "Managed by Stripe"
            }
        ],
        "consent_status": {c.consent_type.value: c.granted for c in get_user_consents(user_id)},
        "last_updated": datetime.utcnow().isoformat()
    }


@router.post("/consent")
async def update_consent(request: Request, consent_req: ConsentUpdateRequest):
    """
    GDPR Article 7 - Consent Management
    
    Update user consent preferences.
    """
    updated_consents = []
    
    for consent_type_str, granted in consent_req.consents.items():
        try:
            consent_type = ConsentType(consent_type_str)
        except ValueError:
            continue
        
        # Don't allow revoking essential consent
        if consent_type == ConsentType.ESSENTIAL and not granted:
            continue
        
        consent_record = ConsentStatus(
            consent_id=generate_id(),
            consent_type=consent_type,
            granted=granted,
            granted_at=datetime.utcnow() if granted else None,
            revoked_at=datetime.utcnow() if not granted else None,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        
        if consent_req.user_id not in _consent_records:
            _consent_records[consent_req.user_id] = []
        _consent_records[consent_req.user_id].append(consent_record)
        updated_consents.append(consent_record)
    
    log_audit(
        action="consent_updated",
        user_id=consent_req.user_id,
        request=request,
        details={"consents": consent_req.consents},
        data_subject_request=False
    )
    
    return {
        "status": "success",
        "message": "Consent preferences updated",
        "updated_consents": [c.model_dump() for c in updated_consents],
        "note": "Essential cookies cannot be disabled as they are required for the app to function."
    }


@router.get("/consent/{user_id}")
async def get_consent_status(user_id: str):
    """Get current consent status for a user"""
    consents = get_user_consents(user_id)
    
    # Build status for all consent types
    status = {}
    for ct in ConsentType:
        latest = None
        for c in consents:
            if c.consent_type == ct:
                if latest is None or c.granted_at > latest.granted_at:
                    latest = c
        
        status[ct.value] = {
            "granted": latest.granted if latest else False,
            "can_disable": ct != ConsentType.ESSENTIAL,
            "description": {
                ConsentType.ESSENTIAL: "Required for the app to function properly",
                ConsentType.ANALYTICS: "Help us improve by tracking usage patterns",
                ConsentType.MARKETING: "Receive updates about new features and offers",
                ConsentType.THIRD_PARTY: "Share data with integrated services (e.g., Stripe)"
            }.get(ct, "")
        }
    
    return {
        "user_id": user_id,
        "consent_status": status,
        "last_updated": datetime.utcnow().isoformat()
    }


# ============================================
# AUDIT LOG ENDPOINTS
# ============================================

@router.get("/audit-logs/{user_id}")
async def get_user_audit_logs(request: Request, user_id: str, limit: int = 50):
    """
    Get audit logs for a user (GDPR transparency).
    """
    user_logs = [log for log in _audit_logs if log.user_id == user_id]
    user_logs.sort(key=lambda x: x.timestamp, reverse=True)
    
    return {
        "user_id": user_id,
        "total_logs": len(user_logs),
        "logs": [log.model_dump() for log in user_logs[:limit]],
        "retention_period_days": _data_retention_days["audit_logs"]
    }


@router.get("/data-retention")
async def get_data_retention_policy():
    """Get the data retention policy"""
    return {
        "policy": {
            "user_data": {
                "retention_days": _data_retention_days["user_data"],
                "description": "User account data, projects, and preferences"
            },
            "audit_logs": {
                "retention_days": _data_retention_days["audit_logs"],
                "description": "Audit logs for compliance and security"
            },
            "deleted_data": {
                "retention_days": _data_retention_days["deleted_data"],
                "description": "Recovery period for deleted accounts"
            }
        },
        "last_updated": "2026-03-17",
        "contact": "privacy@kerfos.com"
    }


# ============================================
# DATA PROCESSING AGREEMENT
# ============================================

@router.get("/dpa")
async def get_data_processing_agreement():
    """Return the Data Processing Agreement template"""
    return {
        "title": "Data Processing Agreement",
        "version": "1.0.0",
        "last_updated": "2026-03-17",
        "parties": {
            "data_controller": {
                "name": "User",
                "description": "The user who owns the data"
            },
            "data_processor": {
                "name": "KerfOS",
                "description": "The service that processes user data"
            }
        },
        "processing_activities": [
            "Storing cabinet designs and cut lists",
            "Processing payments via Stripe",
            "Generating analytics (with consent)",
            "Sending notifications (with consent)"
        ],
        "security_measures": [
            "Encryption at rest (AES-256)",
            "Encryption in transit (TLS 1.3)",
            "Access controls and authentication",
            "Regular security audits",
            "Audit logging"
        ],
        "subprocessors": [
            {
                "name": "Stripe",
                "purpose": "Payment processing",
                "dpa_url": "https://stripe.com/dpa"
            },
            {
                "name": "Railway",
                "purpose": "Cloud hosting",
                "dpa_url": "https://railway.app/legal/dpa"
            }
        ],
        "contact": "dpo@kerfos.com"
    }
