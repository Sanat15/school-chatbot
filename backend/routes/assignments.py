from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.auth import get_current_user
from backend.models.models import Assignment, Student

router = APIRouter(prefix="/assignments", tags=["Assignments"])

@router.get("/me")
def get_assignments(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = current_user["user"]
    role = current_user["role"]
    student = user if role == "student" else db.query(Student).filter(Student.id == user.id).first()
    assignments = db.query(Assignment).filter(Assignment.class_id == student.class_id).all()
    return {"student": student.name, "assignments": [
        {"subject": a.subject, "description": a.description, "due_date": str(a.due_date)} for a in assignments
    ]}