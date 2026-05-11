from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.auth import get_current_user
from backend.models.models import Assignment, Student, ParentStudent

router = APIRouter(prefix="/assignments", tags=["Assignments"])


def _resolve_students(user, role: str, db: Session):
    if role == "student":
        return [user]
    links = db.query(ParentStudent).filter(ParentStudent.parent_id == user.id).all()
    students = [db.get(Student, link.student_id) for link in links]
    return [s for s in students if s is not None]


@router.get("/me")
def get_assignments(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = current_user["user"]
    role = current_user["role"]
    students = _resolve_students(user, role, db)
    if not students:
        raise HTTPException(status_code=404, detail="No student data found")

    results = []
    for student in students:
        entries = db.query(Assignment).filter(Assignment.class_id == student.class_id).all()
        results.append({
            "student": student.name,
            "assignments": [
                {"subject": a.subject, "description": a.description, "due_date": str(a.due_date)}
                for a in entries
            ],
        })
    return results[0] if role == "student" else results
