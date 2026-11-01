# ProofPath Runbook

## Development Setup

### Prerequisites
- Docker Desktop
- Node.js 20+
- Python 3.11+
- Make

### First-time setup
```bash
git clone <repo>
cd student-1
cp .env.example .env
# Edit .env with your API keys (optional for demo mode)
make dev
# In another terminal:
make migrate
make seed
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | `postgresql+asyncpg://...` | PostgreSQL connection string |
| `SECRET_KEY` | Yes | `change-me` | JWT signing key |
| `GEMINI_API_KEY` | No | `""` | Google Gemini API key (live mode only) |
| `GROQ_API_KEY` | No | `""` | Groq API key (live mode only) |
| `LLM_MODE` | No | `replay` | `live` / `record` / `replay` |
| `EMBEDDER` | No | `local` | `gemini` / `local` |
| `CORPUS_MODE` | No | `demo` | `demo` / `reviewed` |
| `DAILY_LLM_BUDGET` | No | `100` | Max LLM calls per day |
| `CLOUDFLARE_TURNSTILE_SECRET` | No | `""` | CAPTCHA secret (production) |

## Common Operations

### Add a new source document
1. Admin panel → Sources → Upload PDF
2. System ingests, chunks, embeds
3. Admin reviews and approves source
4. Source now available for retrieval

### Author a new eligibility rule
1. Admin panel → Rule Studio → New Rule
2. Author fills conditions from source clauses
3. Submit for review (maker cannot approve own rules)
4. Checker reviews and approves
5. Rule enters `approved` status with version stamp

### Run eval against demo benchmark
```bash
make eval-replay
# Output: precision, recall@5, MRR per system (B0, B1, S)
```

### Roll back a bad migration
```bash
docker compose run --rm api alembic downgrade -1
```

### View structured logs
```bash
docker compose logs api --follow
# Logs are JSON (structlog); pipe through jq for readability
docker compose logs api --follow | docker run --rm -i ghcr.io/nicholasgasior/jq -r '.'
```

## Production Deployment

### Render (API)
- Connect repo; set environment variables in Render dashboard
- Build command: `pip install -e ".[dev]"`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check: `/health`
- Set `skip_turnstile=False` in production

### Cloudflare Pages (Web)
- Connect repo; set build directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Set `VITE_API_URL` env var to Render API URL

### Supabase (Database)
- Create project; copy connection string to `DATABASE_URL`
- Run migrations: `DATABASE_URL=<supabase_url> alembic upgrade head`
- Enable pgvector extension in Supabase SQL editor: `CREATE EXTENSION IF NOT EXISTS vector;`

## Troubleshooting

### API not starting
1. Check `docker compose logs api`
2. Ensure DB is healthy: `docker compose ps`
3. Check `DATABASE_URL` is set correctly

### Migrations failing
1. Ensure DB is running: `docker compose up db -d`
2. Check `alembic/versions/` for conflicts
3. Manual reset (dev only): `docker compose down -v && make dev && make migrate`

### LLM calls failing
1. Check `LLM_MODE` — use `replay` in dev to avoid API calls
2. Check `GEMINI_API_KEY` / `GROQ_API_KEY` if in `live` mode
3. Check daily budget: `DAILY_LLM_BUDGET`

### Eval gate failing
1. Run `make eval-replay` and check output
2. Minimum recall@5 is 0.80 — add cassettes if coverage is low
3. Check `backend/tests/cassettes/` for recorded responses

## Monitoring

- Health endpoint: `GET /health` → `{"status": "ok", "version": "...", "corpus_mode": "..."}`
- Keepalive: GitHub Actions pings API every 14 minutes (prevents Render sleep)
- Structured logs: All requests logged with `request_id`, `duration_ms`, `status_code`
