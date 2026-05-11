from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.auth import get_current_user
from backend.models.models import Marks, Student, ParentStudent

router = APIRouter(prefix="/marks", tags=["Marks"])


def _resolve_students(user, role: str, db: Session):
    if role == "student":
        return [user]
    links = db.query(ParentStudent).filter(ParentStudent.parent_id == user.id).all()
    students = [db.get(Student, link.student_id) for link in links]
    return [s for s in students if s is not None]


@router.get("/me")
def get_marks(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = current_user["user"]
    role = current_user["role"]
    students = _resolve_students(user, role, db)
    if not students:
        raise HTTPException(status_code=404, detail="No student data found")

    results = []
    for student in students:
        entries = db.query(Marks).filter(Marks.student_id == student.id).all()
        results.append({
            "student": student.name,
            "marks": [
                {
                    "subject": m.subject,
                    "marks_obtained": m.marks_obtained,
                    "total_marks": m.total_marks,
                    "exam_type": m.exam_type,
                }
                for m in entries
            ],
        })
    return results[0] if role == "student" else results
