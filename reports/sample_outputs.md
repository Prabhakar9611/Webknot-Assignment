# Sample CURL commands

# Start server (in another terminal)
# uvicorn app.app:app --reload

# Create college
curl -s -X POST http://127.0.0.1:8000/colleges -H "Content-Type: application/json" -d '{"name":"REVA University"}'

# Create student
curl -s -X POST http://127.0.0.1:8000/students -H "Content-Type: application/json" -d '{"name":"Alice","email":"alice@reva.edu","college_id":1}'

# Create event
curl -s -X POST http://127.0.0.1:8000/events -H "Content-Type: application/json" -d '{"title":"Intro to LLMs","event_type":"Seminar","starts_at":"2025-09-07T10:00:00","ends_at":"2025-09-07T12:00:00","college_id":1}'

# Register student
curl -s -X POST http://127.0.0.1:8000/registrations -H "Content-Type: application/json" -d '{"student_id":1,"event_id":1}'

# Mark attendance
curl -s -X POST http://127.0.0.1:8000/attendance -H "Content-Type: application/json" -d '{"registration_id":1}'

# Submit feedback
curl -s -X POST http://127.0.0.1:8000/feedback -H "Content-Type: application/json" -d '{"registration_id":1,"rating":5,"comment":"Great!"}'

# Reports
curl -s "http://127.0.0.1:8000/reports/event-popularity"
curl -s "http://127.0.0.1:8000/reports/event-stats/1"
curl -s "http://127.0.0.1:8000/reports/student-participation/1"
curl -s "http://127.0.0.1:8000/reports/top-active-students?limit=3"
