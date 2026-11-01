# ProofPath Threat Model

## Assets

| Asset | Sensitivity | Notes |
|-------|-------------|-------|
| User questions | Medium | May contain indirect PII; scrubbed before LLM calls |
| Source documents | High | Official policy documents; integrity critical |
| Eligibility rules | High | Must be versioned, maker≠checker approved |
| Audit log | High | Tamper-evident hash chain |
| User credentials | High | Argon2id hashed; JWT short-lived |
| LLM API keys | High | Never logged; env-var only |

## Threats and Mitigations

### T1: Prompt Injection via User Questions
- **Threat**: User embeds instructions in question to hijack LLM behavior.
- **Mitigation**: Retrieved/uploaded text wrapped in `<source_data>` delimiters. LLM has no tools. Output parsed into Pydantic model or retried/fallen back. PII scrubbed before any LLM call.

### T2: Policy Fabrication
- **Threat**: LLM invents eligibility rules not present in source documents.
- **Mitigation**: LLM NEVER decides eligibility. The deterministic rule engine decides. LLM only judges claim-vs-passage stance. Quote guard validates all citations verbatim.

### T3: Citation Hallucination
- **Threat**: LLM generates plausible-sounding but false citations.
- **Mitigation**: `quote_guard.validate()` requires verbatim match after NFKC/casefold normalisation (6+ words, 25–400 chars). Failed quotes are dropped, not shown.

### T4: PII Leakage
- **Threat**: User PII (phone, Aadhaar, name) in questions leaks to LLM providers or logs.
- **Mitigation**: `pii.scrub()` runs before every external call. No PII in cache keys.

### T5: Privilege Escalation
- **Threat**: Viewer-role user performs author/checker/admin actions.
- **Mitigation**: Role-based `Depends` on every admin endpoint. JWT claims validated.

### T6: Rule Tampering
- **Threat**: Malicious actor modifies eligibility rules directly.
- **Mitigation**: Maker≠checker approval workflow. Audit log with SHA-256 hash chain. Rule versioning.

### T7: Fake "Admission Confirmed" Output
- **Threat**: System outputs a guarantee of admission, job, salary, placement or scholarship.
- **Mitigation**: Explain validator checks output against banned phrases. Enforced by tests. "Meets checked conditions" is the strongest statement allowed.

### T8: Stale Data Displayed as Current
- **Threat**: Superseded source document used to answer questions.
- **Mitigation**: Sources have `status` field (pending/approved/superseded). Retrieval filters on `approved`. Stale rules show `RULE_STALE_NEEDS_REVIEW`.

### T9: SQL Injection
- **Threat**: Malicious input in API parameters causes SQL injection.
- **Mitigation**: SQLAlchemy ORM with parameterized queries throughout. No raw SQL with user input.

### T10: Rate Limit Bypass / DoS
- **Threat**: Flood of requests exhausts LLM budget or overwhelms API.
- **Mitigation**: slowapi rate limiting (20/min per IP for /ask, 100/min global). Daily LLM budget cap. Cloudflare Turnstile CAPTCHA (in production).

## Trust Boundaries

```
[User Browser] → (HTTPS) → [Cloudflare CDN] → [Render API] → [Supabase DB]
                                                    │
                                              [LLM Provider]
                                         (Gemini / Groq — external)
```

- User input is untrusted beyond the browser.
- LLM output is untrusted until parsed by Pydantic.
- Source document text is DATA, not instructions.
- All external calls go through httpx with timeouts.

## Out of Scope

- Physical security of hosting providers
- Supply chain attacks on npm/PyPI packages (mitigated by lock files + CI)
- Sophisticated state-actor adversaries
