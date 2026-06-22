from database import get_analytics, get_all_students, get_attendance_for_session, get_all_sessions
from datetime import datetime


def get_session_report(session_id: str) -> dict:
    data = get_analytics(session_id)
    all_students = get_all_students()
    present_ids = {r["student_id"] for r in data["records"]}
    absentees = [s for s in all_students if s["student_id"] not in present_ids]
    data["absentees"] = [{"student_id": s["student_id"], "name": s["name"]} for s in absentees]
    return data


def get_student_attendance_summary() -> list:
    all_students = get_all_students()
    all_sessions = [s for s in get_all_sessions() if not s.get("active")]
    total_sessions = len(all_sessions)
    summary = []
    for student in all_students:
        sid = student["student_id"]
        attended = sum(
            1 for sess in all_sessions
            if any(r["student_id"] == sid for r in get_attendance_for_session(sess["_id"]))
        )
        summary.append({
            "student_id": sid,
            "name": student["name"],
            "attended": attended,
            "total": total_sessions,
            "percentage": round((attended / total_sessions * 100) if total_sessions else 0, 1),
        })
    return summary


def get_trend_data() -> list:
    all_sessions = [s for s in get_all_sessions() if not s.get("active")]
    trend = []
    for sess in all_sessions:
        data = get_analytics(sess["_id"])
        trend.append({
            "session_id": sess["_id"],
            "subject": sess.get("subject", ""),
            "date": sess.get("started_at", datetime.utcnow()).strftime("%d %b") if isinstance(sess.get("started_at"), datetime) else "",
            "percentage": data["percentage"],
            "present": data["present"],
            "total": data["total"],
        })
    return trend
