from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import cv2
import threading
import time
from datetime import datetime

from database import (
    register_student, get_all_students, delete_student,
    create_session, end_session, get_active_session,
    get_all_sessions, mark_attendance, get_attendance_for_session,
    get_analytics,
)
from face_utils import encode_face_from_b64, recognize_face, draw_faces_on_frame, frame_to_b64
from analytics import get_session_report, get_student_attendance_summary, get_trend_data

app = Flask(__name__)
CORS(app)

camera_lock = threading.Lock()
camera_instance = None
session_timer_thread = None
session_end_time = None


def get_camera():
    global camera_instance
    if camera_instance is None or not camera_instance.isOpened():
        camera_instance = cv2.VideoCapture(0)
        camera_instance.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera_instance.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return camera_instance


def release_camera():
    global camera_instance
    if camera_instance:
        camera_instance.release()
        camera_instance = None


def session_timer_worker(session_id: str, duration_seconds: int):
    global session_end_time
    session_end_time = time.time() + duration_seconds
    time.sleep(duration_seconds)
    active = get_active_session()
    if active and active["_id"] == session_id:
        end_session(session_id)
        session_end_time = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/attendance")
def attendance_page():
    return render_template("attendance.html")


@app.route("/analytics")
def analytics_page():
    return render_template("analytics.html")


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


@app.route("/api/students", methods=["GET"])
def api_get_students():
    students = get_all_students()
    for s in students:
        s.pop("embedding", None)
    return jsonify(students)


@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.json
    student_id = data.get("student_id", "").strip()
    name = data.get("name", "").strip()
    images = data.get("images", [])

    if not student_id or not name:
        return jsonify({"success": False, "message": "Student ID and name are required"}), 400
    if not images:
        return jsonify({"success": False, "message": "At least one face image is required"}), 400

    embeddings = []
    for b64 in images:
        enc = encode_face_from_b64(b64)
        if enc:
            embeddings.append(enc)

    if not embeddings:
        return jsonify({"success": False, "message": "No face detected in the provided images"}), 400

    import numpy as np
    avg_embedding = np.mean(embeddings, axis=0).tolist()
    result = register_student(student_id, name, avg_embedding)
    return jsonify(result)


@app.route("/api/students/<student_id>", methods=["DELETE"])
def api_delete_student(student_id):
    result = delete_student(student_id)
    return jsonify(result)


@app.route("/api/session/start", methods=["POST"])
def api_start_session():
    global session_timer_thread, session_end_time
    data = request.json
    subject = data.get("subject", "General").strip()
    duration = int(data.get("duration_minutes", 60))

    if get_active_session():
        return jsonify({"success": False, "message": "A session is already active"}), 400

    session_id = create_session(subject, duration)
    session_timer_thread = threading.Thread(
        target=session_timer_worker,
        args=(session_id, duration * 60),
        daemon=True,
    )
    session_timer_thread.start()
    return jsonify({"success": True, "session_id": session_id, "message": f"Session '{subject}' started"})


@app.route("/api/session/stop", methods=["POST"])
def api_stop_session():
    global session_end_time
    active = get_active_session()
    if not active:
        return jsonify({"success": False, "message": "No active session"}), 400
    end_session(active["_id"])
    session_end_time = None
    return jsonify({"success": True, "message": "Session ended"})


@app.route("/api/session/status", methods=["GET"])
def api_session_status():
    active = get_active_session()
    if not active:
        return jsonify({"active": False})
    remaining = None
    if session_end_time:
        remaining = max(0, int(session_end_time - time.time()))
    active["remaining_seconds"] = remaining
    return jsonify({"active": True, "session": active})


@app.route("/api/recognize", methods=["POST"])
def api_recognize():
    active = get_active_session()
    if not active:
        return jsonify({"success": False, "message": "No active session. Start a session first."}), 400

    data = request.json
    b64_image = data.get("image", "")
    if not b64_image:
        return jsonify({"success": False, "message": "No image provided"}), 400

    result = recognize_face(b64_image)
    if result is None:
        return jsonify({"success": False, "message": "Face not recognized"})

    marked = mark_attendance(active["_id"], result["student_id"], result["name"])
    result["already_marked"] = not marked
    result["session_id"] = active["_id"]
    result["success"] = True
    return jsonify(result)


@app.route("/api/attendance/<session_id>", methods=["GET"])
def api_get_attendance(session_id):
    records = get_attendance_for_session(session_id)
    return jsonify(records)


@app.route("/api/analytics/session/<session_id>", methods=["GET"])
def api_session_analytics(session_id):
    report = get_session_report(session_id)
    return jsonify(report)


@app.route("/api/analytics/students", methods=["GET"])
def api_student_analytics():
    summary = get_student_attendance_summary()
    return jsonify(summary)


@app.route("/api/analytics/trends", methods=["GET"])
def api_trends():
    trends = get_trend_data()
    return jsonify(trends)


@app.route("/api/analytics/overview", methods=["GET"])
def api_analytics_overview():
    data = get_analytics()
    return jsonify(data)


@app.route("/api/sessions", methods=["GET"])
def api_get_sessions():
    sessions = get_all_sessions()
    return jsonify(sessions)


def generate_preview_frames():
    students = get_all_students()
    while True:
        with camera_lock:
            cam = get_camera()
            ret, frame = cam.read()
        if not ret:
            time.sleep(0.1)
            continue
        annotated = draw_faces_on_frame(frame, students)
        _, buf = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 60])
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n")
        time.sleep(0.08)


@app.route("/api/video_feed")
def video_feed():
    return Response(generate_preview_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
