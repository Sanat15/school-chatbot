from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from backend.core.llm import get_llm
from backend.core.language import detect_language
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import Any, Optional
import logging
import re
import os

load_dotenv()
logger = logging.getLogger(__name__)

# Singletons — created once at first request, reused for all subsequent ones.
_sql_db: Optional[SQLDatabase] = None
_chain: Any = None


def _get_chain():
    global _sql_db, _chain
    if _sql_db is None:
        _sql_db = SQLDatabase.from_uri(os.getenv("DATABASE_URL", ""))
        _chain = create_sql_query_chain(get_llm(), _sql_db)
    return _chain, _sql_db


def clean_sql(raw: str) -> str:
    if "SQLQuery:" in raw:
        raw = raw.split("SQLQuery:")[-1]
    raw = re.sub(r"```sql|```", "", raw)
    stop_prefixes = ("question:", "let's", "note:", "this query", "the above")
    lines = []
    for line in raw.strip().splitlines():
        if line.strip().lower().startswith(stop_prefixes):
            break
        lines.append(line)
    result = "\n".join(lines).strip()
    if ";" in result:
        result = result[: result.rfind(";") + 1]
    return result


def generate_response(question: str, result: str, username: str) -> str:
    lang = detect_language(question)
    prompt = (
        f"You are a helpful school assistant chatbot.\n"
        f"A user named {username} asked: \"{question}\"\n"
        f"The database returned this result: {result}\n"
        f"Write a friendly, conversational response in 1-2 sentences using this data.\n"
        f"IMPORTANT: Respond in {lang} language only.\n"
        f"Do not mention SQL or databases. Just answer naturally."
    )
    return str(get_llm().invoke(prompt).content)  # type: ignore[union-attr]


def run_nl_query(question: str, username: str = "Student") -> dict:
    try:
        chain, db = _get_chain()
        raw = chain.invoke({"question": question})
        sql_query = clean_sql(raw)
        if not sql_query:
            raise ValueError("Generated SQL is empty")
        result = db.run(sql_query)
        response = generate_response(question, str(result), username)
        return {"query": sql_query, "raw_result": result, "response": response}
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("nl_query failed for user=%s: %s", username, exc)
        raise HTTPException(
            status_code=500,
            detail="Could not process your question. Please try rephrasing.",
        )
