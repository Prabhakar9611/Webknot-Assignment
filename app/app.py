from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Optional

from .database import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Event Reporting System")

@app.post("/colleges", response_model=schemas.CollegeOut)
def create_college(payload: schemas.CollegeCreate, db: Session = Depends(get_db)):
    obj = models.College(name=payload.name)
    db.add(obj)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    db.refresh(obj)
    return obj

@app.post("/students", response_model=schemas.StudentOut)
def create_student(payload: schemas.StudentCreate, db: Session = Depends(get_db)):
    obj = models.Student(name=payload.name, email=payload.email, college_id=payload.college_id)
    db.add(obj)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    db.refresh(obj)
    return obj

@app.post("/events", response_model=schemas.EventOut)
def create_event(payload: schemas.EventCreate, db: Session = Depends(get_db)):
    obj = models.Event(
        title=payload.title,
        event_type=payload.event_type,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        college_id=payload.college_id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.post("/registrations", response_model=schemas.RegistrationOut)
def register_student(payload: schemas.RegistrationCreate, db: Session = Depends(get_db)):
    obj = models.Registration(student_id=payload.student_id, event_id=payload.event_id)
    db.add(obj)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate registration or invalid ids")
    db.refresh(obj)
    return obj

@app.post("/attendance")
def mark_attendance(payload: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    reg = db.get(models.Registration, payload.registration_id)
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")
    if reg.attendance:
        return {"message": "Already marked"}
    obj = models.Attendance(registration_id=payload.registration_id)
    db.add(obj)
    db.commit()
    return {"message": "Attendance marked"}

@app.post("/feedback")
def submit_feedback(payload: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    reg = db.get(models.Registration, payload.registration_id)
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")
    if reg.feedback:
        raise HTTPException(status_code=400, detail="Feedback already submitted")
    obj = models.Feedback(registration_id=payload.registration_id, rating=payload.rating, comment=payload.comment)
    db.add(obj)
    db.commit()
    return {"message": "Feedback submitted"}

# Reports
@app.get("/reports/event-popularity")
def event_popularity(college_id: Optional[int] = None, event_type: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(models.Event.id, models.Event.title, func.count(models.Registration.id).label("registrations"))        .outerjoin(models.Registration, models.Event.id == models.Registration.event_id)

    if college_id:
        q = q.filter(models.Event.college_id == college_id)
    if event_type:
        q = q.filter(models.Event.event_type == event_type)

    q = q.group_by(models.Event.id).order_by(func.count(models.Registration.id).desc())
    return [dict(event_id=eid, title=title, registrations=regs) for eid, title, regs in q.all()]

@app.get("/reports/event-stats/{event_id}", response_model=schemas.EventStats)
def event_stats(event_id: int, db: Session = Depends(get_db)):
    total_regs = db.query(func.count(models.Registration.id)).filter(models.Registration.event_id == event_id).scalar()
    attended = db.query(func.count(models.Attendance.id)).join(models.Registration).filter(models.Registration.event_id == event_id).scalar()
    avg_feedback = db.query(func.avg(models.Feedback.rating)).join(models.Registration).filter(models.Registration.event_id == event_id).scalar()
    attendance_percent = (attended / total_regs * 100.0) if total_regs else 0.0
    return schemas.EventStats(event_id=event_id, registrations=total_regs, attendance_percent=round(attendance_percent, 2), avg_feedback=(round(float(avg_feedback),2) if avg_feedback is not None else None))

@app.get("/reports/student-participation/{student_id}", response_model=schemas.StudentParticipation)
def student_participation(student_id: int, db: Session = Depends(get_db)):
    attended = db.query(func.count(models.Attendance.id)).join(models.Registration).filter(models.Registration.student_id == student_id).scalar()
    return schemas.StudentParticipation(student_id=student_id, events_attended=attended)

@app.get("/reports/top-active-students")
def top_active_students(limit: int = 3, college_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(models.Student.id, models.Student.name, func.count(models.Attendance.id).label("attended"))        .join(models.Registration, models.Student.id == models.Registration.student_id)        .join(models.Attendance, models.Registration.id == models.Attendance.registration_id, isouter=True)        .group_by(models.Student.id)        .order_by(func.count(models.Attendance.id).desc())
    if college_id:
        q = q.filter(models.Student.college_id == college_id)
    rows = q.limit(limit).all()
    return [dict(student_id=sid, name=name, events_attended=attended) for sid, name, attended in rows]
