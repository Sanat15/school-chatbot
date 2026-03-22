from backend.core.database import SessionLocal
from backend.models.models import Class, Student, Parent, ParentStudent, Timetable, Assignment, Marks
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

# Classes
c1 = Class(name="Class 6A")
c2 = Class(name="Class 7B")
db.add_all([c1, c2])
db.commit()

# Students
s1 = Student(name="Ravi Sharma", class_id=c1.id, username="ravi", hashed_password=pwd_context.hash("ravi123"))
s2 = Student(name="Priya Singh", class_id=c1.id, username="priya", hashed_password=pwd_context.hash("priya123"))
s3 = Student(name="Arjun Mehta", class_id=c2.id, username="arjun", hashed_password=pwd_context.hash("arjun123"))
db.add_all([s1, s2, s3])
db.commit()

# Parents
p1 = Parent(name="Suresh Sharma", username="suresh", hashed_password=pwd_context.hash("suresh123"))
p2 = Parent(name="Meena Singh", username="meena", hashed_password=pwd_context.hash("meena123"))
db.add_all([p1, p2])
db.commit()

# Parent-Student links
db.add_all([ParentStudent(parent_id=p1.id, student_id=s1.id), ParentStudent(parent_id=p2.id, student_id=s2.id)])
db.commit()

# Timetable
db.add_all([
    Timetable(class_id=c1.id, day="Monday", subject="Math", time_slot="9:00-10:00"),
    Timetable(class_id=c1.id, day="Monday", subject="Science", time_slot="10:00-11:00"),
    Timetable(class_id=c2.id, day="Monday", subject="English", time_slot="9:00-10:00"),
])
db.commit()

# Assignments
db.add_all([
    Assignment(class_id=c1.id, subject="Math", description="Complete exercise 5.1", due_date="2026-03-25"),
    Assignment(class_id=c2.id, subject="English", description="Write an essay on nature", due_date="2026-03-26"),
])
db.commit()

# Marks
db.add_all([
    Marks(student_id=s1.id, subject="Math", marks_obtained=85, total_marks=100, exam_type="Unit Test"),
    Marks(student_id=s1.id, subject="Science", marks_obtained=90, total_marks=100, exam_type="Unit Test"),
    Marks(student_id=s2.id, subject="Math", marks_obtained=78, total_marks=100, exam_type="Unit Test"),
    Marks(student_id=s3.id, subject="English", marks_obtained=88, total_marks=100, exam_type="Unit Test"),
])
db.commit()

db.close()
print("Dummy data seeded successfully!")