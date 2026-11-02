import sys
from pathlib import Path

# Add backend directory to sys.path so app modules import cleanly on Vercel
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from app.main import app as fastapi_app


class VercelPathMiddleware:
    """
    Vercel rewrites requests to /api/index.py, which makes FastAPI receive
    scope['path'] as '/api/index.py' instead of the requested endpoint.
    This ASGI middleware restores the original requested path from the
    'x-matched-path' or 'x-forwarded-uri' header sent by Vercel edge.
    """
    def __init__(self, asgi_app):
        self.asgi_app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            headers = dict(scope.get("headers", []))
            raw_path = (
                headers.get(b"x-matched-path")
                or headers.get(b"x-forwarded-uri")
                or headers.get(b"x-vercel-matched-path")
            )
            if raw_path:
                path_str = raw_path.decode("latin1").split("?")[0]
                if path_str and not path_str.endswith("index.py"):
                    scope["path"] = path_str
        await self.asgi_app(scope, receive, send)


app = VercelPathMiddleware(fastapi_app)
