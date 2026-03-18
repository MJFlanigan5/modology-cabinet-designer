"""Compliance Components Index for KerfOS

Exports:
- CookieConsent - GDPR cookie consent banner
- PrivacySettings - User privacy management page
- useCookieConsent - Hook for consent status
"""

export { default as CookieConsent } from './CookieConsent'
export { default as PrivacySettings } from './PrivacySettings'
export { useCookieConsent } from './CookieConsent'
