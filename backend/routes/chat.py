from fastapi import APIRouter, Depends
from backend.core.auth import get_current_user
from backend.core.nl_to_sql import run_nl_query
from pydantic import BaseModel, field_validator

router = APIRouter(prefix="/chat", tags=["Chat"])


class QueryRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def question_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Question cannot be empty")
        return v


@router.post("/query")
def chat_query(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    user = current_user["user"]
    role = current_user["role"]

    if role == "student":
        enriched = (
            f"{request.question} "
            f"(Only return data for student named '{user.name}' in class_id {user.class_id})"
        )
    else:
        enriched = f"{request.question} (Only return data for parent named '{user.name}')"

    return run_nl_query(enriched, user.name)
