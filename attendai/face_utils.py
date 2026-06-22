import face_recognition
import numpy as np
import cv2
import base64
from database import get_all_students

TOLERANCE = 0.5


def encode_face_from_frame(frame_bgr: np.ndarray) -> list | None:
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb, model="hog")
    if not locations:
        return None
    encodings = face_recognition.face_encodings(rgb, locations)
    if not encodings:
        return None
    return encodings[0].tolist()


def encode_face_from_b64(b64_image: str) -> list | None:
    img_data = base64.b64decode(b64_image.split(",")[-1])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if frame is None:
        return None
    return encode_face_from_frame(frame)


def recognize_face(b64_image: str) -> dict | None:
    students = get_all_students()
    if not students:
        return None

    unknown_enc = encode_face_from_b64(b64_image)
    if unknown_enc is None:
        return None

    unknown = np.array(unknown_enc)
    known_encs = [np.array(s["embedding"]) for s in students]
    distances = face_recognition.face_distance(known_encs, unknown)
    best_idx = int(np.argmin(distances))
    if distances[best_idx] <= TOLERANCE:
        return {
            "student_id": students[best_idx]["student_id"],
            "name": students[best_idx]["name"],
            "confidence": round((1 - float(distances[best_idx])) * 100, 1),
        }
    return None


def draw_faces_on_frame(frame_bgr: np.ndarray, students: list) -> np.ndarray:
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb, model="hog")
    if not locations:
        return frame_bgr

    encodings = face_recognition.face_encodings(rgb, locations)
    known_encs = [np.array(s["embedding"]) for s in students]

    for (top, right, bottom, left), enc in zip(locations, encodings):
        name = "Unknown"
        color = (0, 0, 200)
        if known_encs:
            distances = face_recognition.face_distance(known_encs, enc)
            best = int(np.argmin(distances))
            if distances[best] <= TOLERANCE:
                name = students[best]["name"]
                color = (0, 180, 0)
        cv2.rectangle(frame_bgr, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame_bgr, (left, bottom - 28), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame_bgr, name, (left + 4, bottom - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    return frame_bgr


def frame_to_b64(frame_bgr: np.ndarray) -> str:
    _, buf = cv2.imencode(".jpg", frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 75])
    return "data:image/jpeg;base64," + base64.b64encode(buf).decode()


def liveness_check_blink(prev_ear: float, curr_ear: float, threshold: float = 0.25) -> bool:
    return prev_ear > threshold and curr_ear < threshold


def get_eye_aspect_ratio(eye_landmarks) -> float:
    A = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
    B = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
    C = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
    return (A + B) / (2.0 * C) if C > 0 else 0
