"""
Google OAuth 2.0 + Gmail verification flow for ProofPath.

Endpoints:
  GET  /auth/google/login           → redirect URL to Google consent screen
  POST /auth/google/callback?code=  → exchange code → JWT, verify email
  GET  /auth/me                     → return current user from JWT
  POST /auth/logout                 → client-side token discard (stateless)
"""
import urllib.parse
import httpx
from fastapi import APIRouter, HTTPException, Header, Query, Request
from app.core.config import settings
from app.security.tokens import create_access_token, decode_access_token
from app.schemas.auth import TokenResponse, UserResponse

router = APIRouter()

# ──────────────────────────────────────────────
# Google OAuth 2.0 constants
# ──────────────────────────────────────────────
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
SCOPES = "openid email profile"

# CRITICAL: This must exactly match what's in Google Cloud Console
# Authorised Redirect URIs
REDIRECT_URI = "http://localhost:5173/auth/callback"

# In-memory user store
_USERS_DB: dict[str, dict] = {}


# ──────────────────────────────────────────────
# Step 1 — Frontend calls this to get Google URL
# ──────────────────────────────────────────────
@router.get("/google/login")
def google_login():
    """Return the Google OAuth consent URL for the frontend to redirect to."""
    if not settings.google_client_id:
        raise HTTPException(
            status_code=503,
            detail="Google OAuth not configured. Set GOOGLE_CLIENT_ID in .env",
        )
    redirect_uri = settings.google_redirect_uri or REDIRECT_URI
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "select_account",
    }
    url = f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return {"url": url, "redirect_uri_used": redirect_uri}


# ──────────────────────────────────────────────
# Step 2 — Frontend posts the code received from Google
# ──────────────────────────────────────────────
@router.post("/google/callback", response_model=TokenResponse)
def google_callback(code: str = Query(...)):
    """Exchange Google auth code → ProofPath JWT."""
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=503, detail="Google OAuth not configured")

    redirect_uri = settings.google_redirect_uri or REDIRECT_URI

    # Exchange code for Google tokens
    try:
        resp = httpx.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
        if not resp.is_success:
            raise HTTPException(
                status_code=502,
                detail=f"Google token exchange failed ({resp.status_code}): {resp.text}",
            )
        token_data = resp.json()
    except HTTPException:
        raise
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Google token exchange error: {exc}")

    access_token_google = token_data.get("access_token")
    if not access_token_google:
        raise HTTPException(status_code=502, detail=f"No access_token from Google. Response: {token_data}")

    # Fetch user profile from Google
    try:
        user_resp = httpx.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token_google}"},
            timeout=10,
        )
        user_resp.raise_for_status()
        profile = user_resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Google userinfo failed: {exc}")

    # Gmail verification — Google vouches that this email is verified
    if not profile.get("email_verified"):
        raise HTTPException(
            status_code=403,
            detail="Gmail address is not verified by Google. Please use a verified Gmail account.",
        )

    email: str = profile["email"]
    name: str = profile.get("name", email.split("@")[0])
    picture: str = profile.get("picture", "")
    google_sub: str = profile.get("sub", "")

    # Upsert user in memory store
    if email not in _USERS_DB:
        _USERS_DB[email] = {
            "id": f"google-{google_sub}",
            "email": email,
            "name": name,
            "picture": picture,
            "role": "user",
            "language": "en",
            "provider": "google",
            "email_verified": True,
            "allow_storing_questions": False,
        }
    else:
        _USERS_DB[email].update({"name": name, "picture": picture})

    user = _USERS_DB[email]
    jwt = create_access_token(user["id"], role=user["role"])
    return TokenResponse(access_token=jwt, role=user["role"], language=user["language"])


# ──────────────────────────────────────────────
# /me — decode JWT → return user profile
# ──────────────────────────────────────────────
@router.get("/me", response_model=UserResponse)
def me(authorization: str = Header(default="")):
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    uid = payload.get("sub", "")
    user = next((u for u in _USERS_DB.values() if u["id"] == uid), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found — please sign in again")

    return UserResponse(
        id=user["id"],
        email=user["email"],
        role=user["role"],
        language=user["language"],
        allow_storing_questions=user.get("allow_storing_questions", False),
    )


@router.post("/logout")
def logout():
    return {"status": "logged_out"}


# ──────────────────────────────────────────────
# Admin fallback — email/password login
# ──────────────────────────────────────────────
from app.schemas.auth import LoginRequest
from app.security.passwords import hash_password, verify_password

_ADMIN_USERS: dict[str, dict] = {
    "admin@proofpath.example": {
        "id": "00000000-0000-0000-0000-000000000001",
        "email": "admin@proofpath.example",
        "hashed_password": hash_password("AdminPass1234!"),
        "role": "admin",
        "language": "en",
        "allow_storing_questions": False,
    }
}


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    user = _ADMIN_USERS.get(req.email)
    if not user or not verify_password(req.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(user["id"], role=user["role"])
    return TokenResponse(access_token=token, role=user["role"], language=user["language"])
