# ProofPath

**Evidence-grounded vocational pathway and eligibility verification platform.**

ProofPath answers family questions about vocational and technical education pathways with claim-level evidence. LLMs explain; documents prove; a deterministic engine decides; humans review.

## Quick Start

```bash
cp .env.example .env
make dev          # starts db + api + web with hot reload
```

Open http://localhost:5173

## Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start all services with hot reload |
| `make check` | Run all linters, type-checkers and tests |
| `make migrate` | Run Alembic migrations |
| `make seed` | Load demo corpus, rules, benchmark |
| `make eval-replay` | Run eval harness against recorded cassettes |
| `make gen-api` | Export OpenAPI spec and regenerate TS client |
| `make fmt` | Auto-format Python and TypeScript |

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────┐
│  React Frontend │───▶│   FastAPI Backend │───▶│ PostgreSQL   │
│  (Vite + TS)    │    │  (Python 3.11+)   │    │ + pgvector   │
└─────────────────┘    └──────────────────┘    └──────────────┘
                              │
                    ┌─────────┴──────────┐
                    │  Pipeline          │
                    │  understand →      │
                    │  retrieve →        │
                    │  verify →          │
                    │  rule_engine →     │
                    │  explain           │
                    └────────────────────┘
```

## Key Design Invariants

1. **No hard-coded policy** — rules live in the database, versioned and maker≠checker approved
2. **LLM never decides eligibility** — the deterministic rule engine decides
3. **Quote guard** — every citation must pass verbatim match (6+ words, 25–400 chars)
4. **Abstention is a feature** — missing evidence → INSUFFICIENT_EVIDENCE, never a guess
5. **No banned outputs** — no guarantees of admission, jobs, salary, placement or scholarships
6. **No PII** — scrubbed before any LLM call or log

## Stack

- **Frontend**: React 18, Vite, TypeScript (strict), Tailwind CSS, shadcn/ui, TanStack Query, Zustand, React Router, React Flow, Recharts, react-i18next
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic, asyncpg, PyMuPDF, structlog, argon2-cffi, PyJWT, slowapi
- **Data**: PostgreSQL 16 + pgvector
- **Infra**: Docker Compose (dev), GitHub Actions (CI), Cloudflare Pages (web), Render (api), Supabase (db)

## Project Structure

```
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── api/v1/  # REST endpoints
│   │   ├── core/    # Config, logging, errors, security
│   │   ├── db/      # Models and sessions
│   │   ├── pipeline/# Ask pipeline (understand→verify→explain)
│   │   ├── rules/   # DSL + three-valued Kleene engine
│   │   ├── llm/     # LLM adapters + cassette replay
│   │   ├── ingestion/# PDF extraction + chunking + embedding
│   │   ├── retrieval/# Hybrid BM25 + vector + RRF
│   │   ├── eval/    # Metrics harness + eval gate
│   │   └── security/# Passwords, tokens, audit chain
│   └── tests/       # unit, property, integration
├── frontend/         # React application
│   ├── src/
│   │   ├── features/ # Feature-folder pages
│   │   ├── components/# Shared UI components
│   │   ├── lib/      # API client, auth, i18n
│   │   └── locales/  # en + hinglish translations
│   └── e2e/          # Playwright end-to-end tests
├── data/demo/        # Fictional demo rules/benchmark
└── docs/             # Architecture, threat model, runbook
```

## Disclaimer

This is decision support, not official advice. "Meets checked conditions" is never an admission decision.
Demo data uses fictional policy text — not official guidance.
