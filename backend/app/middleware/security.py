"""Security Middleware Enhancements for KerfOS

Additional security features:
- Password strength validation
- Two-factor authentication support
- Session management
- API key rotation
- Security event logging
"""
from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, validator
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import secrets
import re
import hashlib
import json


# ============================================
# PASSWORD VALIDATION
# ============================================

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", "monkey", "master",
    "dragon", "111111", "baseball", "iloveyou", "trustno1", "sunshine",
    "princess", "welcome", "shadow", "superman", "michael", "password1",
    "kerfos", "cabinet", "woodwork"
}

class PasswordStrength(BaseModel):
    is_valid: bool
    score: float  # 0.0 to 1.0
    strength_label: str
    requirements: Dict[str, bool]
    suggestions: List[str]

def validate_password_strength(password: str) -> PasswordStrength:
    """
    Validate password strength against security requirements.
    
    Requirements:
    - Minimum 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    - Not a common password
    """
    requirements = {
        "length": len(password) >= 12,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "number": bool(re.search(r"[0-9]", password)),
        "special": bool(re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password)),
        "not_common": password.lower() not in COMMON_PASSWORDS
    }
    
    passed = sum(requirements.values())
    total = len(requirements)
    score = passed / total
    
    suggestions = []
    if not requirements["length"]:
        suggestions.append("Use at least 12 characters")
    if not requirements["uppercase"]:
        suggestions.append("Add an uppercase letter")
    if not requirements["lowercase"]:
        suggestions.append("Add a lowercase letter")
    if not requirements["number"]:
        suggestions.append("Add a number")
    if not requirements["special"]:
        suggestions.append("Add a special character (!@#$%^&*...)")
    if not requirements["not_common"]:
        suggestions.append("Avoid common passwords")
    
    strength_label = "Very Weak"
    if score >= 0.9:
        strength_label = "Very Strong"
    elif score >= 0.7:
        strength_label = "Strong"
    elif score >= 0.5:
        strength_label = "Fair"
    elif score >= 0.3:
        strength_label = "Weak"
    
    return PasswordStrength(
        is_valid=passed >= 5,  # Must pass at least 5 requirements
        score=score,
        strength_label=strength_label,
        requirements=requirements,
        suggestions=suggestions
    )


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    hash_value = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}:${hash_value}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored hash"""
    try:
        salt, hash_value = stored_hash.split("$")
        computed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
        return secrets.compare_digest(computed, hash_value)
    except:
        return False


# ============================================
# TWO-FACTOR AUTHENTICATION
# ============================================

class TwoFactorSetup(BaseModel):
    secret: str
    qr_code_url: str
    backup_codes: List[str]

class TwoFactorVerify(BaseModel):
    user_id: str
    code: str
    is_backup_code: bool = False

def generate_2fa_secret() -> str:
    """Generate a new 2FA secret"""
    return secrets.token_hex(20)

def generate_backup_codes(count: int = 10) -> List[str]:
    """Generate backup codes for 2FA"""
    codes = []
    for _ in range(count):
        code = "".join(secrets.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(8))
        codes.append(code)
    return codes

def verify_2fa_code(code: str, secret: str) -> bool:
    """
    Verify a TOTP code.
    In production, this would use pyotp or similar library.
    """
    # Placeholder - implement actual TOTP verification
    # For now, just check format
    return len(code) == 6 and code.isdigit()


# ============================================
# SESSION MANAGEMENT
# ============================================

class SessionInfo(BaseModel):
    session_id: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    is_valid: bool

class SessionManager:
    """Manage user sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, SessionInfo] = {}
        self.max_sessions_per_user = 5
        self.session_timeout = timedelta(hours=24)
    
    def create_session(
        self,
        user_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> str:
        """Create a new session"""
        # Clean up expired sessions
        self._cleanup_expired()
        
        # Check max sessions per user
        user_sessions = [
            s for s in self.sessions.values()
            if s.user_id == user_id and s.is_valid
        ]
        
        if len(user_sessions) >= self.max_sessions_per_user:
            # Remove oldest session
            oldest = min(user_sessions, key=lambda s: s.last_activity)
            self.sessions[oldest.session_id].is_valid = False
        
        # Create new session
        session_id = secrets.token_urlsafe(32)
        now = datetime.utcnow()
        
        self.sessions[session_id] = SessionInfo(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            last_activity=now,
            ip_address=ip_address,
            user_agent=user_agent,
            is_valid=True
        )
        
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[SessionInfo]:
        """Validate a session and update last activity"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        if not session.is_valid:
            return None
        
        # Check timeout
        if datetime.utcnow() - session.last_activity > self.session_timeout:
            session.is_valid = False
            return None
        
        # Update activity
        session.last_activity = datetime.utcnow()
        return session
    
    def invalidate_session(self, session_id: str):
        """Invalidate a session"""
        if session_id in self.sessions:
            self.sessions[session_id].is_valid = False
    
    def invalidate_all_user_sessions(self, user_id: str):
        """Invalidate all sessions for a user"""
        for session in self.sessions.values():
            if session.user_id == user_id:
                session.is_valid = False
    
    def _cleanup_expired(self):
        """Remove expired sessions"""
        now = datetime.utcnow()
        expired = [
            sid for sid, s in self.sessions.items()
            if not s.is_valid or now - s.last_activity > self.session_timeout
        ]
        for sid in expired:
            del self.sessions[sid]


# ============================================
# API KEY MANAGEMENT
# ============================================

class APIKey(BaseModel):
    key_id: str
    key_hash: str
    user_id: str
    name: str
    created_at: datetime
    last_used: Optional[datetime]
    expires_at: Optional[datetime]
    is_active: bool

class APIKeyManager:
    """Manage API keys for integrations"""
    
    def __init__(self):
        self.keys: Dict[str, APIKey] = {}  # key_id -> APIKey
        self.key_prefix = "kf_"  # KerfOS API key prefix
    
    def generate_key(self, user_id: str, name: str, expires_days: Optional[int] = None) -> tuple[str, str]:
        """
        Generate a new API key.
        Returns (key_id, raw_key) - raw_key is shown once and never stored.
        """
        key_id = f"key_{secrets.token_hex(8)}"
        raw_key = f"{self.key_prefix}{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        now = datetime.utcnow()
        expires_at = now + timedelta(days=expires_days) if expires_days else None
        
        self.keys[key_id] = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            user_id=user_id,
            name=name,
            created_at=now,
            last_used=None,
            expires_at=expires_at,
            is_active=True
        )
        
        return key_id, raw_key
    
    def verify_key(self, raw_key: str) -> Optional[APIKey]:
        """Verify an API key"""
        if not raw_key.startswith(self.key_prefix):
            return None
        
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        for key in self.keys.values():
            if key.key_hash == key_hash and key.is_active:
                # Check expiration
                if key.expires_at and datetime.utcnow() > key.expires_at:
                    key.is_active = False
                    return None
                
                # Update last used
                key.last_used = datetime.utcnow()
                return key
        
        return None
    
    def revoke_key(self, key_id: str):
        """Revoke an API key"""
        if key_id in self.keys:
            self.keys[key_id].is_active = False
    
    def rotate_key(self, key_id: str) -> tuple[str, str]:
        """Rotate an API key (revoke old, generate new)"""
        if key_id not in self.keys:
            raise ValueError("Key not found")
        
        old_key = self.keys[key_id]
        old_key.is_active = False
        
        return self.generate_key(old_key.user_id, old_key.name)


# ============================================
# SECURITY EVENT LOGGING
# ============================================

class SecurityEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime
    user_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    details: Dict
    severity: str  # "low", "medium", "high", "critical"

class SecurityEventLogger:
    """Log security-related events"""
    
    def __init__(self):
        self.events: List[SecurityEvent] = []
        self.max_events = 10000
    
    def log(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict] = None,
        severity: str = "low"
    ) -> SecurityEvent:
        """Log a security event"""
        event = SecurityEvent(
            event_id=secrets.token_hex(8),
            event_type=event_type,
            timestamp=datetime.utcnow(),
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details or {},
            severity=severity
        )
        
        self.events.append(event)
        
        # Trim old events
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
        
        # In production: send to logging service (Datadog, Logflare, etc.)
        if severity in ["high", "critical"]:
            # Send alert
            pass
        
        return event
    
    def get_events(
        self,
        user_id: Optional[str] = None,
        event_type: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100
    ) -> List[SecurityEvent]:
        """Get filtered security events"""
        filtered = self.events
        
        if user_id:
            filtered = [e for e in filtered if e.user_id == user_id]
        if event_type:
            filtered = [e for e in filtered if e.event_type == event_type]
        if severity:
            filtered = [e for e in filtered if e.severity == severity]
        
        return sorted(filtered, key=lambda e: e.timestamp, reverse=True)[:limit]


# Global instances
session_manager = SessionManager()
api_key_manager = APIKeyManager()
security_logger = SecurityEventLogger()
