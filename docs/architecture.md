# ProofPath Architecture

## Overview

ProofPath is a monorepo with a React frontend and FastAPI backend, backed by PostgreSQL with pgvector.

## System Diagram

```
User Browser
     │
     ▼
┌─────────────────────────────────────┐
│  React 18 + Vite + TypeScript       │
│  Tailwind CSS + shadcn/ui (Radix)   │
│  TanStack Query (server state)      │
│  Zustand (UI-only state)            │
│  React Router v6                    │
│  React Flow (pathway graph)         │
│  Recharts (eval charts)             │
│  react-i18next (en + hinglish)      │
└──────────────┬──────────────────────┘
               │ REST + SSE  /api/v1/*
               ▼
┌─────────────────────────────────────┐
│  FastAPI (Python 3.11+)             │
│  Pydantic v2 (request/response)     │
│  slowapi (rate limiting)            │
│  argon2-cffi + PyJWT (auth)         │
│  structlog (structured logging)     │
└────────┬──────────────┬─────────────┘
         │              │
         ▼              ▼
┌──────────────┐  ┌────────────────────┐
│  PostgreSQL  │  │  LLM Adapters      │
│  16 +        │  │  Gemini / Groq /   │
│  pgvector    │  │  Ollama (via httpx) │
│  + FTS       │  │  Cassette replay   │
└──────────────┘  └────────────────────┘
```

## Ask Pipeline

```
POST /api/v1/ask
        │
        ▼
   pii.scrub(question)
        │
        ▼
   understand.py  ← LLM: extract intent, route, facts
        │
        ▼
   retrieval/hybrid.py  ← BM25 + pgvector + RRF fusion
        │
        ▼
   verify.py  ← LLM: claim-vs-passage stance per chunk
        │
        ▼
   quote_guard.validate()  ← deterministic, pure function
        │
        ▼
   rules/engine.py  ← three-valued Kleene logic, NO LLM
        │
        ▼
   aggregate.py  ← verdict (VERIFIED_FACT | MYTH_FALSE | ...)
        │
        ▼
   explain.py  ← LLM: plain-language explanation of validated facts
        │
        ▼
   Response (RFC 9457 errors, Pydantic-validated)
```

## Module Structure

| Module | Purpose |
|--------|---------|
| `api/v1/` | FastAPI routers (auth, ask, pathway, evidence, reports, feedback, meta, admin_*) |
| `core/` | Config (pydantic-settings), logging (structlog), errors (RFC 9457), security, rate limiting |
| `db/` | SQLAlchemy 2.0 async models, session factory, Alembic migrations |
| `pipeline/` | orchestrator, understand, verify, quote_guard, aggregate, explain, pii |
| `rules/` | DSL (Pydantic), three-valued engine (Kleene), next_question, mappings, facts, extractor, lifecycle |
| `llm/` | Base adapter, Gemini/Groq/Ollama adapters, cassette replay, response cache |
| `ingestion/` | PDF extract (PyMuPDF), chunker, table extractor, embedder, pipeline |
| `retrieval/` | Hybrid BM25 + pgvector, RRF fusion, filters |
| `eval/` | Metrics (recall@5, MRR, precision), harness, baselines, report, gate |
| `security/` | Password hashing (argon2), JWT tokens, SHA-256 audit hash chain |

## Database Schema (key tables)

- `users` — id, email, password_hash, role (viewer/author/checker/admin), created_at
- `sources` — id, title, url, doc_type, status (pending/approved/superseded), ingested_at
- `chunks` — id, source_id, page, text, embedding (vector), fts_vector (tsvector)
- `rules` — id, rule_id (stable), version, route, conditions (jsonb), status (draft/approved/superseded), author_id, checker_id
- `qa_events` — id, question_hash, verdict, eligibility, trace (jsonb), created_at
- `eval_runs` — id, harness_set, systems, metrics (jsonb), created_at
- `audit_log` — id, actor_id, action, object_id, payload (jsonb), entry_hash, created_at

## Deployment

| Service | Platform | Free tier |
|---------|----------|-----------|
| Web frontend | Cloudflare Pages | Yes |
| API backend | Render web service | Yes (spins down after inactivity) |
| Database | Supabase | Yes (500MB) |
| CI | GitHub Actions | Yes (2000 min/mo) |
