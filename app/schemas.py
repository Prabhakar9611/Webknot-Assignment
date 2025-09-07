from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class CollegeCreate(BaseModel):
    name: str

class CollegeOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    college_id: int

class StudentOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    college_id: int
    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    title: str
    event_type: str = Field(description="Workshop|Fest|Seminar|Hackathon|TechTalk")
    starts_at: datetime
    ends_at: datetime
    college_id: int

class EventOut(BaseModel):
    id: int
    title: str
    event_type: str
    starts_at: datetime
    ends_at: datetime
    college_id: int
    class Config:
        from_attributes = True

class RegistrationCreate(BaseModel):
    student_id: int
    event_id: int

class RegistrationOut(BaseModel):
    id: int
    student_id: int
    event_id: int
    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    registration_id: int

class FeedbackCreate(BaseModel):
    registration_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

class EventStats(BaseModel):
    event_id: int
    registrations: int
    attendance_percent: float
    avg_feedback: Optional[float]

class StudentParticipation(BaseModel):
    student_id: int
    events_attended: int

class ActiveStudent(BaseModel):
    student_id: int
    events_attended: int
    name: str
