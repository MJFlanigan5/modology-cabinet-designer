"""Frontend Security Utilities for KerfOS

Provides:
- Password strength validation
- Input sanitization
- XSS protection
- CSRF token management
- Security headers for client
- Token refresh logic
- Secure storage wrapper
"""

# Password Strength Validator

PASSWORD_MIN_LENGTH = 12
PASSWORD_REQUIREMENTS = {
  "min_length": 12,
  "require_uppercase": true,
  "require_lowercase": true,
  "require_numbers": true,
  "require_special": true,
  "special_chars": "!@#$%^&*()_+-=[]{}|;:,.<>?"
}

PASSWORD_STRENGTH_RULES = [
  { id: "length", label: "At least 12 characters", test: (pwd) => pwd.length >= 12 },
  { id: "uppercase", label: "One uppercase letter", test: (pwd) => /[A-Z]/.test(pwd) },
  { id: "lowercase", label: "One lowercase letter", test: (pwd) => /[a-z]/.test(pwd) },
  { id: "number", label: "One number", test: (pwd) => /[0-9]/.test(pwd) },
  { id: "special", label: "One special character (!@#$%^&*...)", test: (pwd) => /[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(pwd) },
  { id: "no_common", label: "Not a common password", test: (pwd) => !COMMON_PASSWORDS.includes(pwd.toLowerCase()) }
]

COMMON_PASSWORDS = [
  "password", "123456", "12345678", "qwerty", "abc123", "monkey", "master",
  "dragon", "111111", "baseball", "iloveyou", "trustno1", "sunshine",
  "princess", "welcome", "shadow", "superman", "michael", "password1"
]

export function validatePassword(password) {
  const results = PASSWORD_STRENGTH_RULES.map(rule => ({
    ...rule,
    passed: rule.test(password)
  }))
  
  const passedCount = results.filter(r => r.passed).length
  const strength = passedCount / results.length
  
  let strengthLabel = "Very Weak"
  let strengthColor = "#ef4444" // red
  
  if (strength >= 0.9) {
    strengthLabel = "Very Strong"
    strengthColor = "#22c55e" // green
  } else if (strength >= 0.7) {
    strengthLabel = "Strong"
    strengthColor = "#84cc16" // lime
  } else if (strength >= 0.5) {
    strengthLabel = "Fair"
    strengthColor = "#eab308" // yellow
  } else if (strength >= 0.3) {
    strengthLabel = "Weak"
    strengthColor = "#f97316" // orange
  }
  
  return {
    isValid: passedCount >= 5, // Must pass at least 5 rules
    results,
    strength,
    strengthLabel,
    strengthColor,
    passedCount,
    totalCount: results.length
  }
}

// Input Sanitization

export function sanitizeInput(input) {
  if (typeof input !== "string") return input
  
  return input
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#x27;")
    .replace(/\//g, "&#x2F;")
}

export function sanitizeObject(obj) {
  if (typeof obj !== "object" || obj === null) return obj
  
  if (Array.isArray(obj)) {
    return obj.map(item => sanitizeObject(item))
  }
  
  const sanitized = {}
  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === "string") {
      sanitized[key] = sanitizeInput(value)
    } else if (typeof value === "object") {
      sanitized[key] = sanitizeObject(value)
    } else {
      sanitized[key] = value
    }
  }
  return sanitized
}

// XSS Protection

export function detectXSS(input) {
  if (typeof input !== "string") return false
  
  const xssPatterns = [
    /<script/i,
    /javascript:/i,
    /onerror\s*=/i,
    /onload\s*=/i,
    /onclick\s*=/i,
    /onmouseover\s*=/i,
    /<iframe/i,
    /<embed/i,
    /<object/i,
    /eval\s*\(/i,
    /document\.cookie/i,
    /document\.write/i,
    /window\.location/i,
    /alert\s*\(/i,
    /prompt\s*\(/i,
    /confirm\s*\(/i
  ]
  
  return xssPatterns.some(pattern => pattern.test(input))
}

// CSRF Token Management

let csrfToken = null

export function getCSRFToken() {
  return csrfToken
}

export function setCSRFToken(token) {
  csrfToken = token
}

export function fetchWithCSRF(url, options = {}) {
  const token = getCSRFToken()
  
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      "X-CSRF-Token": token || "",
      "Content-Type": "application/json"
    }
  })
}

// Secure Storage Wrapper

export const secureStorage = {
  set(key, value, ttlMs = null) {
    const item = {
      value,
      timestamp: Date.now(),
      ttl: ttlMs
    }
    
    try {
      localStorage.setItem(`kerfos_${key}`, JSON.stringify(item))
    } catch (e) {
      console.error("Failed to save to secure storage:", e)
    }
  },
  
  get(key) {
    try {
      const raw = localStorage.getItem(`kerfos_${key}`)
      if (!raw) return null
      
      const item = JSON.parse(raw)
      
      // Check TTL
      if (item.ttl && Date.now() - item.timestamp > item.ttl) {
        this.remove(key)
        return null
      }
      
      return item.value
    } catch (e) {
      console.error("Failed to read from secure storage:", e)
      return null
    }
  },
  
  remove(key) {
    try {
      localStorage.removeItem(`kerfos_${key}`)
    } catch (e) {
      console.error("Failed to remove from secure storage:", e)
    }
  },
  
  clear() {
    try {
      Object.keys(localStorage)
        .filter(key => key.startsWith("kerfos_"))
        .forEach(key => localStorage.removeItem(key))
    } catch (e) {
      console.error("Failed to clear secure storage:", e)
    }
  }
}

// Session Management

export const sessionManager = {
  TOKEN_KEY: "auth_token",
  REFRESH_TOKEN_KEY: "refresh_token",
  USER_KEY: "user_data",
  SESSION_TIMEOUT: 24 * 60 * 60 * 1000, // 24 hours
  
  setSession(authToken, refreshToken, user) {
    secureStorage.set(this.TOKEN_KEY, authToken, this.SESSION_TIMEOUT)
    secureStorage.set(this.REFRESH_TOKEN_KEY, refreshToken, 7 * 24 * 60 * 60 * 1000) // 7 days
    secureStorage.set(this.USER_KEY, user, this.SESSION_TIMEOUT)
  },
  
  getToken() {
    return secureStorage.get(this.TOKEN_KEY)
  },
  
  getRefreshToken() {
    return secureStorage.get(this.REFRESH_TOKEN_KEY)
  },
  
  getUser() {
    return secureStorage.get(this.USER_KEY)
  },
  
  isAuthenticated() {
    return !!this.getToken()
  },
  
  clearSession() {
    secureStorage.remove(this.TOKEN_KEY)
    secureStorage.remove(this.REFRESH_TOKEN_KEY)
    secureStorage.remove(this.USER_KEY)
  },
  
  async refreshSession() {
    const refreshToken = this.getRefreshToken()
    if (!refreshToken) {
      this.clearSession()
      return false
    }
    
    try {
      const response = await fetch("/api/auth/refresh", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken })
      })
      
      if (!response.ok) {
        this.clearSession()
        return false
      }
      
      const data = await response.json()
      this.setSession(data.token, data.refresh_token, data.user)
      return true
    } catch (e) {
      console.error("Session refresh failed:", e)
      this.clearSession()
      return false
    }
  }
}

// Rate Limit Handler

export async function handleRateLimit(response) {
  if (response.status === 429) {
    const data = await response.json()
    const retryAfter = data.retry_after || 60
    
    return {
      isRateLimited: true,
      retryAfter,
      message: `Too many requests. Please try again in ${retryAfter} seconds.`
    }
  }
  
  return { isRateLimited: false }
}

// Two-Factor Authentication Utilities

export const twoFactorAuth = {
  generateBackupCodes(count = 10) {
    const codes = []
    for (let i = 0; i < count; i++) {
      const code = Array.from({ length: 8 }, () => 
        Math.random().toString(36).substring(2, 3).toUpperCase()
      ).join('')
      codes.push(code)
    }
    return codes
  },
  
  formatBackupCode(code) {
    return code.match(/.{1,4}/g)?.join('-') || code
  },
  
  validateBackupCode(code) {
    // Remove dashes and spaces, validate length
    const clean = code.replace(/[-\s]/g, '').toUpperCase()
    return clean.length === 8 && /^[A-Z0-9]+$/.test(clean)
  }
}

// Security Event Logger

export const securityLogger = {
  log(event, details = {}) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      event,
      details,
      userAgent: navigator.userAgent,
      url: window.location.href
    }
    
    // In production, send to logging service
    console.log("[Security Event]", logEntry)
    
    // Store locally for debugging
    const logs = secureStorage.get("security_logs") || []
    logs.push(logEntry)
    if (logs.length > 100) logs.shift() // Keep last 100
    secureStorage.set("security_logs", logs, 24 * 60 * 60 * 1000)
  },
  
  getLogs() {
    return secureStorage.get("security_logs") || []
  }
}

export default {
  validatePassword,
  sanitizeInput,
  sanitizeObject,
  detectXSS,
  getCSRFToken,
  setCSRFToken,
  fetchWithCSRF,
  secureStorage,
  sessionManager,
  handleRateLimit,
  twoFactorAuth,
  securityLogger,
  PASSWORD_STRENGTH_RULES
}
