# Security Policy

## Supported Versions

This is an educational learning project. Security updates are applied to the main branch as they become available.

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

---

## Security Updates Applied

### May 2026 - Initial Security Audit

Updated dependencies to address known vulnerabilities:

#### FastAPI
- **Previous**: 0.104.1
- **Updated to**: >=0.109.1
- **Reason**: Patched ReDoS (Regular Expression Denial of Service) vulnerability in Content-Type header parsing
- **CVE**: CVE-2024-24762
- **Severity**: Medium

#### PyTorch
- **Previous**: 2.1.1
- **Updated to**: >=2.6.0
- **Reason**: Patched multiple critical vulnerabilities:
  - Heap buffer overflow
  - Use-after-free vulnerability
  - Remote Code Execution (RCE) via `torch.load` with `weights_only=True`
- **Severity**: High (RCE)

#### python-multipart
- **Previous**: 0.0.6
- **Updated to**: >=0.0.27
- **Reason**: Patched multiple vulnerabilities:
  - Denial of Service (DoS) via unbounded multipart headers
  - Arbitrary file write via non-default configuration
  - DoS via deformed multipart/form-data boundary
  - Content-Type header ReDoS
- **Severity**: High (arbitrary file write), Medium (DoS)

---

## Dependency Management

### Before Installing Dependencies

Always review `requirements.txt` for:
1. Known security vulnerabilities
2. Outdated packages
3. Minimum version constraints

### Checking for Vulnerabilities

```bash
# Install safety checker
pip install safety

# Scan requirements.txt
safety check -r requirements.txt

# Or use pip-audit
pip install pip-audit
pip-audit
```

### Updating Dependencies

```bash
# Update specific package
pip install --upgrade package-name

# Test after updating
pytest app/tests/

# Update requirements.txt
pip freeze > requirements-new.txt
# Review changes, then replace requirements.txt
```

---

## Security Best Practices for This Project

### 1. Environment Variables
- **Never commit `.env` files**
- Use `.env.example` as template
- Store sensitive data (DB passwords, API keys) in environment variables only

### 2. Database Security
- Use strong passwords for PostgreSQL
- Restrict database access to localhost in development
- Use connection pooling limits
- Sanitize all user inputs (SQL injection prevention)

### 3. API Security
- Implement rate limiting (future: use FastAPI middleware)
- Validate all input data with Pydantic models
- Use parameterized queries (SQLAlchemy handles this)
- Never expose internal error details to users

### 4. Docker Security
- Use official PostgreSQL images
- Don't run containers as root
- Keep Docker images updated
- Scan images for vulnerabilities: `docker scan postgres:15`

### 5. Embedding/ML Security
- Validate file uploads before processing
- Limit file sizes
- Sanitize text input before embedding
- Use `torch.load` with `weights_only=True` (with patched version)

---

## Reporting a Vulnerability

This is a personal learning project, but if you discover a security issue:

1. **Do NOT open a public GitHub issue**
2. Email the maintainer directly (see README.md for contact)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

---

## Security Considerations for Portfolio Use

When presenting this project:

### ✅ Mention Security Awareness
- "Updated all dependencies to patched versions"
- "Implemented input validation with Pydantic"
- "Used parameterized queries to prevent SQL injection"
- "Stored credentials in environment variables"

### ⚠️ Acknowledge Limitations
- "This is an educational project, not production-ready"
- "Authentication is basic (no OAuth/JWT in initial version)"
- "No rate limiting or advanced DDoS protection"
- "Single-machine deployment, no distributed security"

---

## Security Checklist for Each Week

### Week 5: PostgreSQL + FastAPI Setup
- [ ] Strong PostgreSQL password
- [ ] .env file not committed
- [ ] Database credentials in environment variables
- [ ] Pydantic models for input validation

### Week 6: SQL Queries
- [ ] All queries use SQLAlchemy (parameterized)
- [ ] No string concatenation for SQL queries
- [ ] User input sanitized

### Week 10: Embeddings & File Processing
- [ ] File size limits enforced
- [ ] File type validation
- [ ] Text sanitization before embedding
- [ ] torch.load uses weights_only=True

### Week 11: Integrated System
- [ ] CORS configured properly
- [ ] API endpoints validate inputs
- [ ] Error messages don't leak sensitive info
- [ ] Rate limiting considered (even if not implemented)

### Week 12: Final Security Review
- [ ] All dependencies updated
- [ ] Security scan passed (safety check)
- [ ] .env.example doesn't contain real credentials
- [ ] README includes security section
- [ ] Portfolio presentation mentions security awareness

---

## Learning Resources

### Security in Web APIs
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

### Python Security
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Bandit - Python Security Linter](https://github.com/PyCQA/bandit)

### Database Security
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)

---

## Version History

| Date | Changes | Reason |
|------|---------|--------|
| 2026-05-28 | Updated fastapi, torch, python-multipart | Address known CVEs |

---

**Remember**: Security is not a one-time task. Keep dependencies updated throughout your learning journey!
