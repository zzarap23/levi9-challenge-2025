from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class StudentsCreate(BaseModel):
    name: str
    email: EmailStr
    isAdmin: bool = False

class Students(StudentsCreate):
    id: str

class WorkingHours(BaseModel):
    meal: str
    from_: str = Field(alias="from")
    to: str

class CanteensCreate(BaseModel):
    name: str
    location: str
    capacity: int
    workingHours: List[WorkingHours]

class Canteens(CanteensCreate):
    id: str

class CanteensUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    workingHours: Optional[List[WorkingHours]] = None

class ReservationsCreate(BaseModel):
    studentId: str
    canteenId: str
    date: str
    time: str
    duration: int

class Reservations(BaseModel):
    id: str
    status: str
    studentId: str
    canteenId: str
    date: str
    time: str
    duration: int
    
