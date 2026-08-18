# Security Policy — CrDB SkillForge

## Security Model & Design Principles

CrDB SkillForge executes queries and diagnostic commands against database environments. Security and safety are central to our design.

### Safe Parameterization
- All SQL tools strictly enforce safe query parameterization.
- Arbitrary untrusted text concatenation into SQL statements is prohibited.

### Execution Boundaries & Mutation Controls
- Diagnostic tools default to **Read-Only** access.
- Destructive actions (such as index drops, table alters, node decommissioning, or schema mutations) require explicit confirmation flags (`confirm=True`) and elevated permissions.
- SQL error outputs are sanitized to prevent credential leakage in logs or agent traces.

---

## Reporting a Vulnerability

If you discover a security vulnerability within CrDB SkillForge (such as SQL injection risks in diagnostic queries, credential leaks, or unauthorized execution pathways), please report it responsibly:

1. **Email**: Send vulnerability details to `security@crdb-skillforge.org`.
2. **Details**: Include steps to reproduce, affected version, and potential impact.
3. **Response**: We will acknowledge receipt within 48 hours and work with you to patch the issue prior to public disclosure.

Do not file public GitHub issues for undisclosed security vulnerabilities.
