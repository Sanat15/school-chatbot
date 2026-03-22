from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.auth import get_current_user
from backend.models.models import Marks, Student

router = APIRouter(prefix="/marks", tags=["Marks"])

@router.get("/me")
def get_marks(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = current_user["user"]
    role = current_user["role"]
    student = user if role == "student" else db.query(Student).filter(Student.id == user.id).first()
    marks = db.query(Marks).filter(Marks.student_id == student.id).all()
    return {"student": student.name, "marks": [
        {"subject": m.subject, "marks_obtained": m.marks_obtained, "total_marks": m.total_marks, "exam_type": m.exam_type} for m in marks
    ]}