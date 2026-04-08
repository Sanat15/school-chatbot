from fastapi import APIRouter, Depends
from backend.core.auth import get_current_user
from backend.core.nl_to_sql import run_nl_query
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def chat_query(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    user = current_user["user"]
    role = current_user["role"]
    username = user.name

    # Inject context into the question so LLM only fetches relevant data
    if role == "student":
        enriched_question = f"{request.question} (Only return data for student named '{user.name}' in class_id {user.class_id})"
    else:
        enriched_question = f"{request.question} (Only return data for parent named '{user.name}')"

    result = run_nl_query(enriched_question, username)
    return result