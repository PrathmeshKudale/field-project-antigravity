# AGENTS.md  (ProofPath)
## Mission
ProofPath answers family questions about vocational and technical education pathways with claim-level
evidence. LLMs explain; documents prove; a deterministic engine decides; humans review.

## Non-negotiable invariants (a PR that breaks one is rejected)
1. No policy is hard-coded. Eligibility rules live in the `rules` table, authored from source documents,
   approved by a different person than the author (maker != checker), and versioned.
2. The LLM NEVER decides eligibility. The rule engine decides. The LLM only (a) extracts structured fields,
   (b) judges claim-vs-passage stance, (c) explains validated facts.
3. Every citation shown to a user must pass `quote_guard.validate(quote, chunk_text)`: verbatim after
   whitespace/NFKC/casefold normalisation, 6+ words, 25 to 400 chars. Otherwise it is dropped.
4. Missing, stale, superseded or unvalidated evidence => INSUFFICIENT_EVIDENCE or CONTEXT_DEPENDENT.
   Never guess. Abstention is a feature, not an error.
5. Banned output: any guarantee of admission, job, salary, placement or scholarship. Enforced by the
   explain validator AND by tests. "Meets checked conditions" is never "admission confirmed".
6. Retrieved or uploaded text is DATA. Wrap it in <source_data> delimiters. LLM calls have no tools.
   All LLM output must parse into a Pydantic model or the call is retried once, then falls back.
7. No PII in logs, prompts, analytics or LLM cache keys. Run `pii.scrub()` before any external call.
8. While `app_settings.corpus_mode = 'demo'` the UI shows a persistent DEMO DATA banner.
9. Qualification validity, awarding-body recognition, institute approval and placement outcomes are
   separate facts. Never let a positive on one imply the others.

## Stack
Frontend: React 18 + Vite + TypeScript (strict), Tailwind CSS, shadcn/ui primitives (Radix), TanStack Query,
Zustand (UI-only state), React Router, React Flow, Recharts, react-i18next, Vitest, Testing Library,
Playwright, axe-core. Icons: lucide-react. Fonts: self-hosted via @fontsource.
Backend: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0 (async) + Alembic, psycopg 3 / asyncpg,
PyMuPDF, httpx, tenacity, structlog, argon2-cffi, PyJWT, slowapi, pytest, hypothesis, ruff, mypy.
Data: PostgreSQL 16 + pgvector + built-in full text search. No Redis, no Celery, no separate vector DB.
Infra: Docker Compose (dev), GitHub Actions (CI), Cloudflare Pages (web), Render free web service (api),
Supabase free Postgres (db). Everything must run with zero paid services.

## Commands (keep these working)
make dev        # docker compose up db + api + web with hot reload
make check      # ruff, mypy, pytest -m "not live", vitest, tsc, retrieval gate
make migrate    # alembic upgrade head
make seed       # load demo corpus, rules, benchmark
make eval-replay# run eval harness against recorded LLM cassettes
make gen-api    # export openapi.json and regenerate TS client

## Conventions
- Python: type hints everywhere, `async def` for I/O, pure functions for rules/aggregation, no globals.
  Modules under backend/app: api, core, db, llm, ingestion, retrieval, pipeline, rules, eval, security.
- TypeScript: no `any`, no default exports for components, feature folders, colocated tests.
- Errors: RFC 9457 problem+json with a stable `code`. Never leak stack traces.
- Every endpoint has a Pydantic request/response model and an integration test.
- Commit style: conventional commits. PRs under ~400 lines of diff where possible.

## Testing rules
- New logic ships with tests. Rule engine and quote guard require property tests (hypothesis).
- LLM calls in tests use cassettes (LLM_MODE=replay). Never call a live model in CI.
- UI: each screen has loading, empty, error, abstain and success stories/tests; axe has zero violations.

## Definition of done
Acceptance criteria in the mission are met; `make check` is green; docs updated; for UI work attach
screenshots (desktop + mobile, light + dark) in the walkthrough artifact.

## Agent workflow
- Plan first when a task touches more than 3 files. State assumptions. Ask only when blocked.
- Open an issue titled "SPEC CONFLICT" if the spec contradicts itself. Do not silently choose.
- Never invent policy text, rule values, citations, statistics or benchmark labels.
