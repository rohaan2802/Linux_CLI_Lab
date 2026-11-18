# Online banking threat model

The banking application is the conceptual case study in the original submission. The repository contains its threat model and a risk register. The executable lab demonstrates Linux command-line workflows.

## Assets and trust boundaries

Customer identities, account balances, transaction instructions, session tokens, signing keys, source code and audit records require protection. A typical request crosses the browser-to-edge, application-to-database, application-to-payment-provider and operator-to-administration boundaries.

## Misuse cases and controls

| Scenario | Weakness | Controls | Verification |
| --- | --- | --- | --- |
| Account takeover | Reused passwords and weak recovery | MFA, secure recovery, per-account throttling, alerting | Exercise recovery and throttling in a test environment. |
| Cross-account access | Missing object authorization | Check ownership and role on every read and write | Request another test account's statement and require denial. |
| SQL injection | Query text includes untrusted input | Parameterized SQL and least-privilege database roles | Confirm inputs remain bound values in a test query. |
| Transaction replay | Missing replay control | Idempotency keys and transaction-state validation | Re-submit one test transfer and verify one debit. |
| Session theft | Weak cookie settings or long-lived tokens | Secure, HttpOnly and appropriate SameSite cookies; rotation and expiry | Inspect cookies and verify expiry/logout. |
| Log leakage | Sensitive fields written to logs | Structured redaction and access-controlled retention | Confirm credentials and full account data are absent. |
| Dependency compromise | Unsupported packages | Dependency inventory, update process and review | Review the dependency report and patch evidence. |
| Service disruption | Unbounded costly operations | Rate controls, capacity planning and recovery exercises | Measure behavior under an authorized load test. |

## Risk scoring

The CSV uses a small illustrative 1–5 likelihood and impact scale. Priority equals likelihood times impact. These are design-review estimates. Re-score with actual architecture, usage and incident evidence before an operational assessment.

## Corrections to the original discussion

Use password hashing such as Argon2id under a documented configuration and migration policy. Parameterized queries address the SQL/data boundary. SameSite and anti-CSRF measures complement session cookie settings. Distributed denial-of-service protection also requires network and infrastructure planning.

## Residual risks

A control description is a proposal. Effectiveness requires implementation and verification in the target application. The original PDFs remain available for historical evidence.

References

- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
