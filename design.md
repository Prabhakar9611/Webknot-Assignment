Campus Event Reporting System 
Author: Prabhakar S
Date: 7 Sep 2025


Problem:

Colleges conduct many events like seminars, workshops, hackathons, and fests. We need a simple system that can:
Allow colleges to create events
Allow students to register and attend events
Collect student feedback
Generate reports to know which events are popular and which students are most active


Scope:
The project should do these things:
Keep record of colleges, students, and events
Students can register for events
Mark attendance when they come
Collect feedback (rating 1–5)
Show reports like event popularity, event statistics, and top students
Should work for multiple colleges and different event types


Assumptions:
One email is unique only inside the same college (same email can exist in two colleges)
Event IDs are unique in the database
A student can register for an event only once
A student can give only one feedback per event
For now, no login/authentication is added (kept simple for prototype)


Database Design:
Main tables:
College – stores college details
Student – belongs to a college
Event – belongs to a college
Registration – connects student and event
Attendance – linked to registration (to avoid double marking)
Feedback – linked to registration (rating and comments)


API Endpoints:
POST /colleges → create college
POST /students → create student
POST /events → create event
POST /registrations → register student to event
POST /attendance → mark attendance
POST /feedback → submit feedback


Reports:
GET /reports/event-popularity → list events with registration counts
GET /reports/event-stats/{event_id} → show registrations, attendance %, average rating
GET /reports/student-participation/{student_id} → number of events attended by one student
GET /reports/top-active-students → most active students


Process Flow:
Student registers for an event
Attendance is marked on the day of event
After event, student submits feedback
Reports can be generated to see popularity, stats, and top students


Edge Cases:
Prevent same student registering twice for one event
Prevent attendance being marked twice
Prevent feedback being submitted twice
If no registrations, event shows 0% attendance and no feedback


Technology Used:
FastAPI (Python) → to create APIs
SQLite → lightweight database
SQLAlchemy → ORM for database handling
Pydantic → input validation (example: email format, rating range)


Limitations:
No authentication or login system in this version
Not designed for very large scale (but fine for prototype)
Features like event cancellation or editing are not included