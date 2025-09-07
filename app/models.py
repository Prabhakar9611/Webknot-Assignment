from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class EventType(str, enum.Enum):
    workshop = "Workshop"
    fest = "Fest"
    seminar = "Seminar"
    hackathon = "Hackathon"
    talk = "TechTalk"

class College(Base):
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    students = relationship("Student", back_populates="college")
    events = relationship("Event", back_populates="college")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)

    college = relationship("College", back_populates="students")
    registrations = relationship("Registration", back_populates="student")

    __table_args__ = (UniqueConstraint("email", "college_id", name="uq_student_email_per_college"),)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    event_type = Column(String, nullable=False)  # store EventType.value
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)

    college = relationship("College", back_populates="events")
    registrations = relationship("Registration", back_populates="event")

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    registered_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
    attendance = relationship("Attendance", uselist=False, back_populates="registration")
    feedback = relationship("Feedback", uselist=False, back_populates="registration")

    __table_args__ = (UniqueConstraint("student_id", "event_id", name="uq_registration"),)

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"), unique=True, nullable=False)
    marked_at = Column(DateTime, server_default=func.now())

    registration = relationship("Registration", back_populates="attendance")

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"), unique=True, nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(String, nullable=True)
    submitted_at = Column(DateTime, server_default=func.now())

    registration = relationship("Registration", back_populates="feedback")
