-- Event Popularity Report
SELECT e.id AS event_id, e.title, COUNT(r.id) AS registrations
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
GROUP BY e.id
ORDER BY registrations DESC;

-- Student Participation Report
SELECT s.id AS student_id, s.name, COUNT(a.id) AS events_attended
FROM students s
JOIN registrations r ON s.id = r.student_id
LEFT JOIN attendance a ON r.id = a.registration_id
GROUP BY s.id
ORDER BY events_attended DESC;

-- Event Stats (attendance %, avg rating) for a specific event_id = ?
SELECT
  (SELECT COUNT(*) FROM registrations r WHERE r.event_id = :event_id) AS registrations,
  (SELECT ROUND(100.0 * COUNT(*) / NULLIF((SELECT COUNT(*) FROM registrations r WHERE r.event_id = :event_id), 0), 2)
     FROM attendance a JOIN registrations r ON a.registration_id = r.id
     WHERE r.event_id = :event_id) AS attendance_percent,
  (SELECT ROUND(AVG(f.rating), 2) FROM feedback f JOIN registrations r ON f.registration_id = r.id WHERE r.event_id = :event_id) AS avg_feedback;
