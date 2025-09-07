"""
Seed script to populate demo data.
Run: python scripts/seed.py
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app import models

Base.metadata.create_all(bind=engine)

def main():
    db: Session = SessionLocal()
    # Colleges
    c1 = models.College(name="REVA University")
    c2 = models.College(name="IISc Bangalore")
    db.add_all([c1, c2])
    db.commit()
    db.refresh(c1); db.refresh(c2)

    # Students
    students = [
        models.Student(name="Alice", email="alice@reva.edu", college_id=c1.id),
        models.Student(name="Bob", email="bob@reva.edu", college_id=c1.id),
        models.Student(name="Chandra", email="chandra@iisc.ac.in", college_id=c2.id),
    ]
    db.add_all(students)
    db.commit()
    for s in students: db.refresh(s)

    now = datetime.utcnow()
    # Events
    events = [
        models.Event(title="Intro to LLMs", event_type="Seminar", starts_at=now, ends_at=now+timedelta(hours=2), college_id=c1.id),
        models.Event(title="HackNight 2025", event_type="Hackathon", starts_at=now+timedelta(days=1), ends_at=now+timedelta(days=1, hours=8), college_id=c1.id),
        models.Event(title="Quantum Talk", event_type="TechTalk", starts_at=now+timedelta(days=2), ends_at=now+timedelta(days=2, hours=2), college_id=c2.id),
    ]
    db.add_all(events)
    db.commit()
    for e in events: db.refresh(e)

    # Registrations
    regs = [
        models.Registration(student_id=students[0].id, event_id=events[0].id),
        models.Registration(student_id=students[1].id, event_id=events[0].id),
        models.Registration(student_id=students[1].id, event_id=events[1].id),
        models.Registration(student_id=students[2].id, event_id=events[2].id),
    ]
    db.add_all(regs)
    db.commit()
    for r in regs: db.refresh(r)

    # Attendance
    db.add_all([models.Attendance(registration_id=regs[0].id), models.Attendance(registration_id=regs[2].id)])

    # Feedback
    db.add_all([
        models.Feedback(registration_id=regs[0].id, rating=5, comment="Great!"),
        models.Feedback(registration_id=regs[1].id, rating=4, comment="Nice"),
    ])
    db.commit()
    db.close()
    print("Seeded demo data.")

if __name__ == "__main__":
    main()
