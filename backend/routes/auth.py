from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.auth import verify_password, create_access_token
from backend.models.models import Student, Parent

router = APIRouter(tags=["Auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Try student first
    user = db.query(Student).filter(Student.username == form_data.username).first()
    role = "student"

    if not user:
        user = db.query(Parent).filter(Parent.username == form_data.username).first()
        role = "parent"

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": user.username, "role": role, "id": user.id})
    return {"access_token": token, "token_type": "bearer", "role": role}