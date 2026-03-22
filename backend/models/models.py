from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from backend.core.database import Base

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"))
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Parent(Base):
    __tablename__ = "parents"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class ParentStudent(Base):
    __tablename__ = "parent_student"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parents.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

class Timetable(Base):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    day = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    time_slot = Column(String, nullable=False)

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(Date, nullable=False)

class Marks(Base):
    __tablename__ = "marks"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String, nullable=False)
    marks_obtained = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    exam_type = Column(String, nullable=False)