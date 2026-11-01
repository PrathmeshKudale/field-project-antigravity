from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import configure_logging, logger
from app.core.errors import (
    AppError,
    problem_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

from app.api.v1 import (
    auth,
    ask,
    pathway,
    evidence,
    reports,
    feedback,
    meta,
    admin_sources,
    admin_rules,
    admin_eval,
    admin_users,
    admin_audit,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("ProofPath Backend starting up", corpus_mode=settings.corpus_mode)
    yield
    logger.info("ProofPath Backend shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""ProofPath: Evidence-grounded vocational pathway and eligibility verification platform.
Answers questions with claim-level evidence, quote-verified citations, three-valued rule engine, and safe abstention.""",
    lifespan=lifespan,
)

# Exception handlers (RFC 9457 problem+json)
app.add_exception_handler(AppError, problem_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(ask.router, prefix="/api/v1", tags=["ask"])
app.include_router(pathway.router, prefix="/api/v1", tags=["pathway"])
app.include_router(evidence.router, prefix="/api/v1", tags=["evidence"])
app.include_router(reports.router, prefix="/api/v1", tags=["reports"])
app.include_router(feedback.router, prefix="/api/v1", tags=["feedback"])
app.include_router(meta.router, prefix="/api/v1/meta", tags=["meta"])

# Admin & Reviewer routes
app.include_router(admin_sources.router, prefix="/api/v1/admin", tags=["admin_sources"])
app.include_router(admin_rules.router, prefix="/api/v1/admin", tags=["admin_rules"])
app.include_router(admin_eval.router, prefix="/api/v1/admin", tags=["admin_eval"])
app.include_router(admin_users.router, prefix="/api/v1/admin", tags=["admin_users"])
app.include_router(admin_audit.router, prefix="/api/v1/admin", tags=["admin_audit"])


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": settings.app_version,
        "corpus_mode": settings.corpus_mode,
        "app": settings.app_name,
    }
