from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI(title="Students Database CRUD API")

from pathlib import Path
DATABASE = str(Path(__file__).resolve().parent / "database.db")


# 1. Create the database and students table
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                course TEXT,
                address TEXT,
                enrollment_date TEXT
            )
        """)


init_db()


# 2. Define the data expected when creating a student
class StudentCreate(BaseModel):
    name: str
    date_of_birth: str
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None


# 3. Define the fields that can be updated
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None


def get_student(student_id: int):
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()

        return dict(row) if row else None


# Home endpoint
@app.get("/")
def home():
    return {"message": "Student Database API is running!"}


# 4. CREATE: Add a student
@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            """
            INSERT INTO students
            (name, date_of_birth, email, phone, course, address,
             enrollment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                student.name,
                student.date_of_birth,
                student.email,
                student.phone,
                student.course,
                student.address,
                student.enrollment_date,
            ),
        )

        student_id = cursor.lastrowid

    return get_student(student_id)


# 5. READ: List and filter students
@app.get("/students")
def list_students(name: Optional[str] = None, course: Optional[str] = None):
    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")

    if course:
        query += " AND course LIKE ?"
        params.append(f"%{course}%")

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, params).fetchall()

        return [dict(row) for row in rows]


# 6. READ: Get one student by ID
@app.get("/students/{student_id}")
def read_student(student_id: int):
    student = get_student(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# 7. UPDATE: Modify an existing student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    existing = get_student(student_id)

    if existing is None:
        raise HTTPException(status_code=404, detail="Student not found")

    changes = student.model_dump(exclude_unset=True)

    if not changes:
        return existing

    allowed_fields = {
        "name",
        "date_of_birth",
        "email",
        "phone",
        "course",
        "address",
        "enrollment_date",
    }

    for field, value in changes.items():
        if field in allowed_fields:
            existing[field] = value

    # Required fields cannot be empty or null
    if not existing["name"] or not existing["date_of_birth"]:
        raise HTTPException(
            status_code=400, detail="Name and date of birth are required"
        )

    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """
            UPDATE students
            SET name = ?, date_of_birth = ?, email = ?,
                phone = ?, course = ?, address = ?,
                enrollment_date = ?
            WHERE student_id = ?
        """,
            (
                existing["name"],
                existing["date_of_birth"],
                existing["email"],
                existing["phone"],
                existing["course"],
                existing["address"],
                existing["enrollment_date"],
                student_id,
            ),
        )

    return get_student(student_id)


# 8. DELETE: Remove a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    existing = get_student(student_id)

    if existing is None:
        raise HTTPException(status_code=404, detail="Student not found")

    with sqlite3.connect(DATABASE) as conn:
        conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))

    return {"message": "Student deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading

    threading.Timer(
        2,
        lambda: webbrowser.open("http://127.0.0.1:8000/docs")
    ).start()

    uvicorn.run(app, host="127.0.0.1", port=8000)
