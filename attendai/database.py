from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "attendai"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

students_col = db["students"]
sessions_col = db["sessions"]
attendance_col = db["attendance"]


def register_student(student_id: str, name: str, embedding: list) -> dict:
    if students_col.find_one({"student_id": student_id}):
        return {"success": False, "message": "Student already registered"}
    doc = {
        "student_id": student_id,
        "name": name,
        "embedding": embedding,
        "registered_at": datetime.utcnow(),
    }
    students_col.insert_one(doc)
    return {"success": True, "message": f"{name} registered successfully"}


def get_all_students() -> list:
    return list(students_col.find({}, {"_id": 0}))


def delete_student(student_id: str) -> dict:
    result = students_col.delete_one({"student_id": student_id})
    if result.deleted_count:
        return {"success": True, "message": "Student deleted"}
    return {"success": False, "message": "Student not found"}


def create_session(subject: str, duration_minutes: int) -> str:
    doc = {
        "subject": subject,
        "duration_minutes": duration_minutes,
        "started_at": datetime.utcnow(),
        "ended_at": None,
        "active": True,
    }
    result = sessions_col.insert_one(doc)
    return str(result.inserted_id)


def end_session(session_id: str):
    from bson import ObjectId
    sessions_col.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"ended_at": datetime.utcnow(), "active": False}},
    )


def get_active_session() -> dict | None:
    session = sessions_col.find_one({"active": True})
    if session:
        session["_id"] = str(session["_id"])
    return session


def get_all_sessions() -> list:
    sessions = list(sessions_col.find({}, {"_id": 1, "subject": 1, "started_at": 1, "ended_at": 1, "active": 1}))
    for s in sessions:
        s["_id"] = str(s["_id"])
    return sessions


def mark_attendance(session_id: str, student_id: str, student_name: str):
    existing = attendance_col.find_one({"session_id": session_id, "student_id": student_id})
    if existing:
        return False
    attendance_col.insert_one({
        "session_id": session_id,
        "student_id": student_id,
        "student_name": student_name,
        "timestamp": datetime.utcnow(),
    })
    return True


def get_attendance_for_session(session_id: str) -> list:
    records = list(attendance_col.find({"session_id": session_id}, {"_id": 0}))
    return records


def get_analytics(session_id: str = None) -> dict:
    total_students = students_col.count_documents({})
    if session_id:
        present = attendance_col.count_documents({"session_id": session_id})
        absent = total_students - present
        records = get_attendance_for_session(session_id)
        return {
            "total": total_students,
            "present": present,
            "absent": max(absent, 0),
            "percentage": round((present / total_students * 100) if total_students else 0, 1),
            "records": records,
        }
    all_sessions = list(sessions_col.find({"active": False}, {"_id": 1, "subject": 1, "started_at": 1}))
    summary = []
    for s in all_sessions:
        sid = str(s["_id"])
        present = attendance_col.count_documents({"session_id": sid})
        summary.append({
            "session_id": sid,
            "subject": s.get("subject", ""),
            "date": s["started_at"].strftime("%Y-%m-%d %H:%M"),
            "present": present,
            "total": total_students,
            "percentage": round((present / total_students * 100) if total_students else 0, 1),
        })
    return {"sessions": summary, "total_students": total_students}
