import sys
import os

# Make the project root importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app
from starlette.types import ASGIApp, Receive, Scope, Send


class _StripPrefix:
    """Strip /api prefix added by Vercel's rewrite rule before handing off to FastAPI."""

    def __init__(self, inner: ASGIApp, prefix: str) -> None:
        self.inner = inner
        self.prefix = prefix.encode()
        self.prefix_str = prefix

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            path: str = scope["path"]
            if path.startswith(self.prefix_str):
                stripped = path[len(self.prefix_str):] or "/"
                scope = {**scope, "path": stripped}
                raw: bytes = scope.get("raw_path", path.encode())
                if raw.startswith(self.prefix):
                    scope["raw_path"] = raw[len(self.prefix):] or b"/"
        await self.inner(scope, receive, send)


# Vercel routes /api/* → this file; strip the /api prefix so FastAPI routes match.
app = _StripPrefix(app, "/api")
