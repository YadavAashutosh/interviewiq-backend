# InterviewIQ AI

**Your AI Career Coach** — a full-stack, AI-powered mobile platform for campus placement preparation: resume analysis, mock interviews, and aptitude practice, all in one app.

📱 **Try the app (APK):** [Download from Google Drive](https://drive.google.com/file/d/1t69Sajt2D8PPKNFDbae_L9jADEnU9YNH/view?usp=sharing)

> This repo contains the backend (API) source. The Flutter mobile app's
> source isn't published here — this README documents what the full app
> does end-to-end so the backend's purpose makes sense in context.

---

## What the app does

InterviewIQ AI is a mobile app (Flutter, Android) with a Python backend, built to help students prepare for campus placements end-to-end.

### 🏠 Home Dashboard
Real-time overview of your prep progress: current Resume Score, Interview Readiness, Communication Score, daily streak, today's practice goal, and a merged recent-activity feed (interviews, quizzes, resume scans) — all computed live from your actual usage, not placeholder data.

### 📄 Resume Analyzer / ATS Checker
Upload a PDF resume and paste a target job description. The backend:
- Extracts text from the PDF
- Identifies skills present in both the resume and job description (spaCy-based matching against a skill vocabulary)
- Computes an ATS match score — a weighted blend of keyword-match ratio and TF-IDF/cosine text similarity
- Runs Named Entity Recognition to pull out organizations, dates, and locations from the resume
- Calls an LLM (Groq/Llama 3.3) to generate specific, actionable improvement suggestions
Results (score + skill gaps + suggestions) are shown in the app and saved to the user's profile.

### 🎤 AI Mock Interviews
Pick an interviewer **persona** (Google, Microsoft, Amazon, Startup Founder, HR Manager) and a **round type** (Technical, Behavioral, HR, Resume-based, Project-based, or a general Chat interview). The app then runs a real back-and-forth interview:
1. Backend generates a question tailored to the mode/persona/role
2. You answer (typed or spoken)
3. Backend evaluates the answer — returns a score, feedback, strengths, improvements, and a natural follow-up question
4. Repeats for as long as you want to practice

**Voice Interview mode** additionally speaks the question aloud (text-to-speech) and transcribes your spoken answer live (speech-to-text) using the phone's microphone — a fully hands-free mock interview.

### 🧮 Aptitude & Coding Quiz
AI-generated multiple-choice quizzes across four categories — Quantitative Aptitude, Logical Reasoning, Verbal Ability, and Coding/Technical — at a chosen difficulty and question count. Each question includes an explanation shown immediately after you answer, and a final score summary.

### 📈 Progress
A weekly score-trend chart (Mon–Sun, averaged across interview + quiz sessions that week), gamified XP/Level/Coins computed from real session history, and weekly/monthly activity summaries.

### 👤 Profile
Editable college, branch, graduation year, skills, and social links (GitHub/LinkedIn/Portfolio), saved per account. Shows your latest resume ATS score at a glance.

### 🔐 Authentication
Email/Password, Google Sign-In, or Guest mode (full functionality without an account — progress just isn't saved permanently). Backed by Firebase Authentication + Firestore for persistence.

---

## Architecture

```
┌───────────────────────┐        HTTPS / JSON        ┌───────────────────────┐
│   Flutter Mobile App    │ ──────────────────────────▶ │   FastAPI Backend       │
│   (Android, not          │ ◀────────────────────────── │   (this repo)            │
│    published here)       │                              │                          │
│                          │                              │  spaCy (NLP)             │
│  Riverpod (state)         │                              │  scikit-learn (ATS)      │
│  GoRouter (navigation)     │                              │  pdfplumber (PDF parse)  │
│  Firebase Auth              │                              │  Groq LLM (Llama 3.3)   │
│  Firestore (persistence)     │                              │                          │
└───────────────────────┘                              └───────────────────────┘
```

The app never calls the LLM directly — every AI operation is proxied through this backend, which is the only place holding the LLM API key. Firebase (Auth + Firestore) is used independently by the app for login and saving user data (scores, history, profile), with no backend involvement.

---

## This repo: Backend

FastAPI service combining classic NLP with an LLM to power the three AI-driven modules above.

### Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI + Uvicorn (ASGI) |
| NLP | spaCy (`en_core_web_sm`) — skill extraction, named entity recognition |
| ATS scoring | scikit-learn — TF-IDF + cosine similarity, blended with keyword-match ratio |
| PDF parsing | pdfplumber |
| LLM | Groq API — Llama 3.3 70B (question generation, answer evaluation, resume suggestions, quiz generation) |
| Config | pydantic-settings (`.env`-based) |
| Hosting | Render (free tier, auto-deploy from `main`) |

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Health check |
| POST | `/api/v1/resume/analyze` | Upload PDF + job description → ATS score, skill match, AI suggestions |
| POST | `/api/v1/interview/question` | Generate an interview question (mode, persona, job role) |
| POST | `/api/v1/interview/answer` | Evaluate an answer → score, feedback, next question |
| POST | `/api/v1/quiz/generate` | Generate MCQ quiz questions (category, difficulty, count) |

### Project Structure

```
app/
├── main.py                    # FastAPI app entrypoint, CORS, router registration
├── core/
│   └── config.py              # Environment-based settings (Groq API key)
├── models/                    # Pydantic request/response schemas
│   ├── quiz_schemas.py
│   └── interview_schemas.py
├── services/                  # Business logic
│   ├── pdf_extractor.py       # PDF text extraction
│   ├── resume_parser.py       # spaCy skill extraction + NER
│   ├── ats_scorer.py          # TF-IDF/cosine + keyword-match ATS scoring
│   ├── gemini_service.py      # Groq LLM — resume suggestions
│   ├── interview_service.py   # Groq LLM — question generation + answer evaluation
│   └── quiz_service.py        # Groq LLM — quiz generation
└── api/v1/                    # Route handlers
    ├── resume.py
    ├── interview.py
    └── quiz.py
```

### Running Locally (extra — only needed if you want to run/modify the backend yourself)

```bash
git clone https://github.com/YadavAashutosh/interviewiq-backend.git
cd interviewiq-backend

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Create a `.env` file in the project root (never commit this file):
```
GROQ_API_KEY=your_own_key_here
```
Get a free key at [console.groq.com](https://console.groq.com) — no credit card required.

Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```
Visit `http://127.0.0.1:8000/docs` for interactive Swagger API docs.

### Deployment

Deployed on [Render](https://render.com) (free tier, no credit card required):
- **Build command:** `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment variable:** `GROQ_API_KEY` (set in Render's dashboard, never in code)
- Auto-deploys on every push to `main`.

> The live deployment URL isn't published here — it's a free-tier
> deployment with a shared LLM quota, so it's kept private to the app
> itself rather than open for anyone to call directly. Use the APK above
> to try the full app.

---

## Author

**Ashu Yadav** — B.Tech CSE (AI & ML), Uka Tarsadia University
An end-to-end portfolio project spanning mobile development, backend engineering, applied NLP, and LLM integration.