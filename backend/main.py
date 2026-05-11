from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import timetable, assignments, marks, auth, chat
import logging
import os

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Warm up the NL-to-SQL singleton at startup to eliminate first-request cold start.
    try:
        from backend.core.nl_to_sql import _get_chain
        _get_chain()
        logging.getLogger(__name__).info("NL-to-SQL chain ready")
    except Exception as exc:
        logging.getLogger(__name__).warning("Chain warmup failed (non-fatal): %s", exc)
    yield


app = FastAPI(title="School Chatbot API", version="1.0.0", lifespan=lifespan)

_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
# Allow the deployed Vercel domain if set via env var (e.g. https://school-chatbot.vercel.app)
if _frontend_url := os.getenv("FRONTEND_URL"):
    _ALLOWED_ORIGINS.append(_frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(timetable.router, prefix="/api")
app.include_router(assignments.router, prefix="/api")
app.include_router(marks.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/", tags=["Health"])
def root():
    return {"message": "School Chatbot API is running"}
