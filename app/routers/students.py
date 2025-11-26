from fastapi import APIRouter, HTTPException
from app.models import StudentsCreate, Students
from app.database import students, generate_student_id

router = APIRouter (
    prefix = "/students",
    tags = ["students"]
)

@router.post("", response_model=Students, status_code=201)
def create_student(student_in: StudentsCreate):
    for s in students.values():
        if s.email == student_in.email:
            raise HTTPException(status_code=400, detail="Email already in use")
        
    student_id = generate_student_id()

    student = Students(
        id = student_id,
        name = student_in.name,
        email = student_in.email,
        isAdmin = student_in.isAdmin
    )
    students[student_id] = student

    return student

@router.get("/{student_id}", response_model=Students)
def get_student(student_id):
    student = students.get(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student

