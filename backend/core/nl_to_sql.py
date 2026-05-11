from groq import Groq
from sqlalchemy import text
from backend.core.database import engine
from backend.core.language import detect_language
from fastapi import HTTPException
from dotenv import load_dotenv
from functools import lru_cache
import logging
import re
import os

load_dotenv()
logger = logging.getLogger(__name__)

_SCHEMA = """
Tables in the PostgreSQL database:
- classes(id, name)
- students(id, name, class_id, username, hashed_password)
- parents(id, name, username, hashed_password)
- parent_student(id, parent_id, student_id)
- timetable(id, class_id, day, subject, time_slot)
- assignments(id, class_id, subject, description, due_date)
- marks(id, student_id, subject, marks_obtained, total_marks, exam_type)
"""


@lru_cache(maxsize=1)
def _client() -> Groq:
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


def _chat(messages: list) -> str:
    return (
        _client()
        .chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0,
        )
        .choices[0]
        .message.content
    )


def _generate_sql(question: str) -> str:
    raw = _chat([
        {
            "role": "system",
            "content": (
                "You are a SQL expert. Given a question, write a single PostgreSQL SELECT query.\n"
                "Output ONLY the SQL query — no explanation, no markdown, no backticks.\n\n"
                f"Schema:\n{_SCHEMA}"
            ),
        },
        {"role": "user", "content": question},
    ])
    return re.sub(r"```sql|```", "", raw).strip()


def _generate_response(question: str, result: str, username: str) -> str:
    lang = detect_language(question)
    return _chat([
        {
            "role": "system",
            "content": (
                f"You are a helpful school assistant chatbot. "
                f"Answer naturally in {lang}. Never mention SQL or databases."
            ),
        },
        {
            "role": "user",
            "content": (
                f"User {username} asked: {question}\n"
                f"Database result: {result}\n"
                f"Give a friendly 1-2 sentence answer."
            ),
        },
    ])


def run_nl_query(question: str, username: str = "Student") -> dict:
    try:
        sql = _generate_sql(question)
        if not sql.upper().lstrip().startswith("SELECT"):
            raise ValueError(f"Non-SELECT query generated: {sql[:80]}")

        with engine.connect() as conn:
            rows = conn.execute(text(sql)).fetchall()
            result = str([dict(row._mapping) for row in rows])

        response = _generate_response(question, result, username)
        return {"query": sql, "raw_result": result, "response": response}

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("nl_query failed user=%s: %s", username, exc)
        raise HTTPException(
            status_code=500,
            detail="Could not process your question. Please try rephrasing.",
        )
