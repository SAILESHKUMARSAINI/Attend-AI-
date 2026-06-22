# AttendAI — AI-Powered Smart Attendance System

## Stack
- **Backend**: Python 3.10+ · Flask · face_recognition (dlib) · OpenCV
- **Database**: MongoDB (local)
- **Frontend**: HTML · CSS · Vanilla JavaScript
- **Deployment**: Local / on-premise

## Project structure
```
attendai/
├── app.py              # Flask routes (main entry point)
├── database.py         # MongoDB operations
├── face_utils.py       # Face detection, encoding, recognition
├── analytics.py        # Attendance analytics helpers
├── requirements.txt
├── .env
├── templates/
│   ├── base.html
│   ├── index.html      # Dashboard
│   ├── register.html   # Face registration
│   ├── attendance.html # Live attendance capture
│   ├── analytics.html  # Reports & charts
│   └── admin.html      # Admin panel
└── static/
    ├── css/style.css
    └── js/main.js
```

## Setup

### 1. Prerequisites
- Python 3.10 or higher
- MongoDB running locally on port 27017
- A webcam connected to your machine
- CMake installed (needed for dlib)

#### Install CMake (if not present)
```bash
# Ubuntu/Debian
sudo apt-get install cmake build-essential

# macOS
brew install cmake
```

### 2. Create virtual environment
```bash
cd attendai
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate.bat    # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> Note: `dlib` and `face_recognition` can take several minutes to compile.
> On Windows, install dlib via wheel: https://github.com/sachadee/Dlib

### 4. Start MongoDB
```bash
# If MongoDB is installed as a service
sudo systemctl start mongod

# Or run directly
mongod --dbpath /data/db
```

### 5. Run the application
```bash
python app.py
```

Open your browser at: **http://localhost:5000**

## Usage workflow

1. **Register students** → Go to `/register`, enter student ID + name, capture 3–5 face images, click Register.
2. **Start a session** → Go to `/attendance`, enter subject name + duration, click Start session.
3. **Mark attendance** → Start your camera, click Start auto-scan. The system will scan every 2 seconds and mark students automatically.
4. **View reports** → Go to `/analytics` to see trends, per-student summaries, and session reports.
5. **Manage data** → Go to `/admin` to view/delete students and sessions.

## Modules

| Module | File | Description |
|---|---|---|
| Face registration | `face_utils.py` + `/api/register` | Captures and stores face embeddings averaged from multiple shots |
| Attendance capture | `face_utils.py` + `/api/recognize` | Compares live frame embedding against all stored embeddings |
| Timer control | `app.py` session_timer_worker | Background thread auto-ends session after duration |
| Database | `database.py` | All MongoDB CRUD operations for students, sessions, attendance |
| Analytics | `analytics.py` | Per-session reports, student-wise %, trend data |
| Security | `face_utils.py` liveness helpers | EAR-based blink detection (expandable) |

## Configuration

Edit `.env` to change:
- `MONGO_URI` — point to a remote MongoDB if needed
- Recognition tolerance is set to `0.5` in `face_utils.py` (lower = stricter)

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/students` | All registered students |
| POST | `/api/register` | Register new student with face images |
| DELETE | `/api/students/<id>` | Remove a student |
| POST | `/api/session/start` | Start attendance session |
| POST | `/api/session/stop` | End active session |
| GET | `/api/session/status` | Get active session info |
| POST | `/api/recognize` | Recognize face and mark attendance |
| GET | `/api/attendance/<session_id>` | Attendance records for session |
| GET | `/api/analytics/overview` | Overall analytics |
| GET | `/api/analytics/trends` | Per-session trend data |
| GET | `/api/analytics/students` | Per-student attendance summary |
| GET | `/api/analytics/session/<id>` | Detailed session report |
| GET | `/api/video_feed` | MJPEG live camera stream |
