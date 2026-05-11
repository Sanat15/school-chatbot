from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.auth import get_current_user
from backend.models.models import Timetable, Student, ParentStudent

router = APIRouter(prefix="/timetable", tags=["Timetable"])


def _resolve_students(user, role: str, db: Session):
    if role == "student":
        return [user]
    links = db.query(ParentStudent).filter(ParentStudent.parent_id == user.id).all()
    students = [db.get(Student, link.student_id) for link in links]
    return [s for s in students if s is not None]


@router.get("/me")
def get_timetable(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = current_user["user"]
    role = current_user["role"]
    students = _resolve_students(user, role, db)
    if not students:
        raise HTTPException(status_code=404, detail="No student data found")

    results = []
    for student in students:
        entries = db.query(Timetable).filter(Timetable.class_id == student.class_id).all()
        results.append({
            "student": student.name,
            "timetable": [{"day": t.day, "subject": t.subject, "time_slot": t.time_slot} for t in entries],
        })
    return results[0] if role == "student" else results
