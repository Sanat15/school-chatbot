from fastapi import APIRouter, Depends
from backend.core.auth import get_current_user
from backend.core.nl_to_sql import run_nl_query
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def chat_query(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    result = run_nl_query(request.question)
    return result