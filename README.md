<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=AttendAI&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=AI-Powered%20Face%20Recognition%20Attendance%20System&descAlignY=55&descAlign=50" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> **🤖 No more proxy attendance. No more manual registers. Just faces.**

<br/>

![AttendAI Demo](https://raw.githubusercontent.com/SAILESHKUMARSAINI/AttendAI/main/static/demo.gif)

</div>

---

## 🎯 What is AttendAI?

AttendAI is a **production-grade, AI-powered attendance management system** that uses real-time facial recognition to automatically mark student attendance — eliminating proxy attendance, manual errors, and paperwork forever.

Built with **Flask + MongoDB + OpenCV + face_recognition (dlib)** — it runs entirely on-premise with zero cloud dependency and zero subscription cost.

> Built by **Sailesh Kumar Saini** — MCA'27, D.Y. Patil Institute, Pune | Patent Holder | IEEE Member

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎭 **Face Registration** | Register students with 3–5 face captures — averaged embedding for max accuracy |
| ⚡ **Auto Attendance** | Live camera scans every 2 seconds — marks attendance automatically |
| 🛡️ **Anti-Proxy** | Face embedding comparison with 0.5 tolerance — fakes don't pass |
| 👁️ **Liveness Detection** | EAR-based blink detection — photos won't fool the system |
| ⏱️ **Session Timer** | Auto-ends attendance session after set duration via background thread |
| 📊 **Analytics Dashboard** | Per-session reports, student-wise % attendance, trend charts |
| 🎥 **Live Video Feed** | Real-time MJPEG stream with face bounding boxes and name labels |
| 🗄️ **Admin Panel** | Manage students and sessions — add, view, delete with ease |
| 📈 **Trend Analysis** | Track attendance patterns across subjects and dates |
| 🔌 **REST API** | Complete API for integration with any frontend or mobile app |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   BROWSER CLIENT                     │
│  Dashboard │ Register │ Attendance │ Analytics │ Admin│
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / MJPEG Stream
┌──────────────────────▼──────────────────────────────┐
│                  FLASK BACKEND                       │
│                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   app.py    │  │ face_utils  │  │ analytics   │  │
│  │ REST Routes │  │ encode/recog│  │ reports/    │  │
│  │ Video Feed  │  │ draw/liveness│ │ trends/summary│ │
│  │ Session Mgr │  └──────┬──────┘  └─────────────┘  │
│  └──────┬──────┘         │                           │
│         │         ┌──────▼──────┐                    │
│  ┌──────▼──────┐  │  OpenCV +   │                    │
│  │ database.py │  │    dlib     │                    │
│  │ MongoDB CRUD│  │ face_recog  │                    │
│  └──────┬──────┘  └─────────────┘                    │
└─────────│───────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────┐
│                    MONGODB                           │
│   students │ sessions │ attendance                   │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
AttendAI/
│
├── 🐍 app.py                  # Flask app — all REST routes + video feed
├── 🗄️ database.py             # MongoDB CRUD — students, sessions, attendance
├── 🤖 face_utils.py           # Face encode, recognize, draw, liveness (EAR)
├── 📊 analytics.py            # Session reports, student summaries, trend data
├── 📋 requirements.txt        # Python dependencies
├── 🔒 .env                    # Environment variables (MONGO_URI)
│
├── 📂 templates/
│   ├── base.html              # Base layout
│   ├── index.html             # 📊 Dashboard
│   ├── register.html          # 📸 Face registration
│   ├── attendance.html        # 🎥 Live attendance capture
│   ├── analytics.html         # 📈 Reports & charts
│   └── admin.html             # ⚙️ Admin panel
│
└── 📂 static/
    ├── css/style.css
    └── js/main.js
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+ · Flask · Flask-CORS |
| **AI/ML** | face_recognition · dlib · OpenCV · NumPy |
| **Database** | MongoDB · PyMongo |
| **Frontend** | HTML5 · CSS3 · Vanilla JavaScript |
| **Video** | MJPEG Streaming · OpenCV VideoCapture |
| **Threading** | Python threading — session timer worker |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MongoDB running on port 27017
- Webcam connected
- CMake installed (for dlib)

```bash
# Install CMake
# Ubuntu/Debian
sudo apt-get install cmake build-essential

# macOS
brew install cmake
```

### 1. Clone the Repository
```bash
git clone https://github.com/SAILESHKUMARSAINI/AttendAI.git
cd AttendAI
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
> ⏳ `dlib` compilation takes 5–10 minutes. Windows users → use prebuilt wheel from [here](https://github.com/sachadee/Dlib)

### 4. Configure Environment
```bash
# Create .env file
echo "MONGO_URI=mongodb://localhost:27017/" > .env
```

### 5. Start MongoDB
```bash
# As service
sudo systemctl start mongod

# Or directly
mongod --dbpath /data/db
```

### 6. Run AttendAI
```bash
python app.py
```

🌐 Open **http://localhost:5000** in your browser!

---

## 📖 Usage Workflow

```
Step 1: Register Students
   → /register
   → Enter Student ID + Name
   → Capture 3–5 face images
   → System averages embeddings for accuracy
   → ✅ Student registered in MongoDB

Step 2: Start Attendance Session
   → /attendance
   → Enter subject name + duration (minutes)
   → Click "Start Session"
   → Background timer auto-ends session

Step 3: Auto Mark Attendance
   → Click "Start Auto-Scan"
   → Camera scans every 2 seconds
   → Face matched → attendance marked instantly
   → Already marked → skipped (anti-duplicate)

Step 4: View Analytics
   → /analytics
   → Per-session attendance %
   → Student-wise summary
   → Trend charts across subjects

Step 5: Admin Management
   → /admin
   → View all students + sessions
   → Delete students or clear sessions
```

---

## 🔌 API Reference

### Students
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/students` | Get all registered students |
| `POST` | `/api/register` | Register student with face images |
| `DELETE` | `/api/students/<id>` | Delete a student |

### Sessions
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/session/start` | Start attendance session |
| `POST` | `/api/session/stop` | End active session |
| `GET` | `/api/session/status` | Get active session + remaining time |
| `GET` | `/api/sessions` | Get all sessions |

### Attendance
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/recognize` | Recognize face + mark attendance |
| `GET` | `/api/attendance/<session_id>` | Get attendance records |
| `GET` | `/api/video_feed` | Live MJPEG camera stream |

### Analytics
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/analytics/overview` | Overall system analytics |
| `GET` | `/api/analytics/session/<id>` | Detailed session report |
| `GET` | `/api/analytics/students` | Per-student attendance % |
| `GET` | `/api/analytics/trends` | Trend data across sessions |

---

## 🧠 How Face Recognition Works

```python
# 1. Registration — encode face from image
embedding = face_recognition.face_encodings(rgb_frame)[0]

# 2. Multiple captures → averaged embedding for robustness
avg_embedding = np.mean(embeddings, axis=0)

# 3. Recognition — compare unknown face to all stored embeddings
distances = face_recognition.face_distance(known_encodings, unknown)
best_match = students[np.argmin(distances)]

# 4. Tolerance check — 0.5 is strict enough to prevent fakes
if distances[best_match] <= 0.5:
    mark_attendance(student)
```

**Accuracy improves with more registration images.**
**Tolerance 0.5 = strict. Lower = stricter. Configurable in `face_utils.py`.**

---

## 🗺️ Roadmap

- [x] Face registration with multi-image averaging
- [x] Real-time auto attendance marking
- [x] Session timer with background thread
- [x] Analytics dashboard with trend data
- [x] Admin panel for data management
- [x] REST API for all operations
- [ ] Docker containerization
- [ ] AWS EC2 deployment with CI/CD
- [ ] Power BI analytics integration
- [ ] Mobile app (React Native)
- [ ] GeoFencing anti-spoofing layer
- [ ] Multi-camera support

---

## 👨‍💻 Author

<div align="center">

**Sailesh Kumar Saini**

MCA'27 — Data Science | D.Y. Patil Institute of MCA and Management, Pune

🏛️ Patent Holder — Govt. of India | 🔬 Research Paper — ICBAAISEM 2026 | 🛡️ IEEE Member

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/saileshsaini-663b42257)
[![Portfolio](https://img.shields.io/badge/Portfolio-7c5cfc?style=for-the-badge&logo=vercel&logoColor=white)](https://portfolio-livid-eta-21b0w1vzq7.vercel.app)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SAILESHKUMARSAINI)

</div>

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

⭐ **Star this repo if AttendAI helped you!** ⭐

</div>
