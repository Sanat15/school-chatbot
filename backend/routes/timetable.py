from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.auth import get_current_user
from backend.models.models import Timetable, Student

router = APIRouter(prefix="/timetable", tags=["Timetable"])

@router.get("/me")
def get_timetable(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = current_user["user"]
    role = current_user["role"]
    student = user if role == "student" else db.query(Student).filter(Student.id == user.id).first()
    timetable = db.query(Timetable).filter(Timetable.class_id == student.class_id).all()
    return {"student": student.name, "timetable": [
        {"day": t.day, "subject": t.subject, "time_slot": t.time_slot} for t in timetable
    ]}