from groq import Groq
from dotenv import load_dotenv
from functools import lru_cache
import os

load_dotenv()


@lru_cache(maxsize=1)
def get_groq_client() -> Groq:
    return Groq(api_key=os.getenv("GROQ_API_KEY"))
