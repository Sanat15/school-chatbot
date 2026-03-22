from fastapi import FastAPI
from backend.routes import timetable, assignments, marks
from backend.routes import auth

app = FastAPI(title="School Chatbot API")

app.include_router(auth.router)
app.include_router(timetable.router)
app.include_router(assignments.router)
app.include_router(marks.router)

@app.get("/")
def root():
    return {"message": "School Chatbot API is running"}