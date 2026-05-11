from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import timetable, assignments, marks, auth, chat
import logging

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(timetable.router)
app.include_router(assignments.router)
app.include_router(marks.router)
app.include_router(chat.router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/", tags=["Health"])
def root():
    return {"message": "School Chatbot API is running"}
