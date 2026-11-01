from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uuid


class AppError(Exception):
    def __init__(self, status: int, code: str, detail: str) -> None:
        self.status = status
        self.code = code
        self.detail = detail


async def problem_exception_handler(request: Request, exc: AppError) -> JSONResponse:
    request_id = str(uuid.uuid4())[:8]
    return JSONResponse(
        status_code=exc.status,
        content={
            "type": f"https://proofpath.example/errors/{exc.code.lower()}",
            "title": exc.code.replace("_", " ").title(),
            "status": exc.status,
            "detail": exc.detail,
            "code": exc.code,
            "request_id": request_id,
        },
        headers={"Content-Type": "application/problem+json"},
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    request_id = str(uuid.uuid4())[:8]
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": "about:blank",
            "title": "HTTP Error",
            "status": exc.status_code,
            "detail": exc.detail,
            "code": f"HTTP_{exc.status_code}",
            "request_id": request_id,
        },
        headers={"Content-Type": "application/problem+json"},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "type": "https://proofpath.example/errors/validation_error",
            "title": "Validation Error",
            "status": 422,
            "detail": str(exc.errors()),
            "code": "VALIDATION_ERROR",
        },
        headers={"Content-Type": "application/problem+json"},
    )
