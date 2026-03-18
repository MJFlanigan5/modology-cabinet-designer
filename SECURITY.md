# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.2.x   | :white_check_mark: |
| < 2.2   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them securely using one of these methods:

### Preferred Method: GitHub Security Advisories

1. Go to [KerfOS Security Advisories](https://github.com/MJFlanigan5/modology-cabinet-designer/security/advisories)
2. Click "Report a vulnerability"
3. Fill out the form with details

### Alternative Method: Email

Send an email to: **security@kerfos.com**

Include the following information:
- Type of vulnerability (e.g., XSS, SQL injection, authentication bypass)
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

## Response Timeline

| Status | Timeline |
| ------ | -------- |
| Acknowledgment | Within 24 hours |
| Initial Assessment | Within 72 hours |
| Fix Development | 7-14 days (depending on severity) |
| Patch Release | As soon as possible after fix |

## Security Measures

KerfOS implements the following security measures:

### Backend Security
- Rate limiting (DoS protection)
- CSRF protection
- XSS prevention
- SQL injection prevention
- Input validation and sanitization
- Security headers (OWASP recommendations)
- Request logging for auditing

### Authentication Security
- Password strength requirements (12+ characters, mixed case, numbers, special)
- Secure password hashing (SHA-256 with salt)
- Session management with timeout
- Two-factor authentication (coming soon)

### Data Security
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Data retention policies
- GDPR compliance (data export, deletion, consent management)

### Infrastructure Security
- Secure environment variable management
- API key rotation support
- Dependency scanning
- Regular security audits

## Security Best Practices for Users

1. **Use strong passwords** - Minimum 12 characters with mixed case, numbers, and special characters
2. **Enable 2FA** - When available, enable two-factor authentication
3. **Review permissions** - Regularly review API keys and integrations
4. **Report suspicious activity** - Contact security@kerfos.com if you notice anything unusual

## Hall of Fame

We would like to thank the following researchers for responsibly disclosing vulnerabilities:

*No disclosures yet - be the first!*

---

**Contact:** security@kerfos.com
**GPG Key:** [Coming soon]
