from langchain_groq import ChatGroq
from pydantic import SecretStr
from dotenv import load_dotenv
from functools import lru_cache
import os

load_dotenv()

@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    return ChatGroq(  # type: ignore
        model="llama-3.3-70b-versatile",
        api_key=SecretStr(os.getenv("GROQ_API_KEY") or ""),
        temperature=0,
    )