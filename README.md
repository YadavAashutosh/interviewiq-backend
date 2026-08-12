# InterviewIQ AI

**Your AI Career Coach** — a full-stack, AI-powered mobile platform for campus placement preparation: resume analysis, mock interviews, and aptitude practice, all in one app.

📱 **Try the app (APK):** [Download from Google Drive](https://drive.google.com/drive/folders/126UYR0hsLgdvccnHpV46g_vpOmwms9as?usp=sharing)

> The folder above contains multiple APK versions — **install the latest
> one** for the full feature set and the most bug fixes. Older versions
> are kept there only for reference if you want to see how the app
> evolved; they're not the recommended build to use.

> **First-time note:** the backend runs on a free-tier server that sleeps
> after inactivity. The very first AI action you try (resume scan,
> interview question, quiz) may take 20-30 seconds to respond while it
> wakes up — this is normal, not a bug. Every action after that is fast.

> This repo contains the backend (API) source. The Flutter mobile app's
> source isn't published here — this README documents what the full app
> does end-to-end so the backend's purpose makes sense in context.

---

## What the app does

InterviewIQ AI is a mobile app (Flutter, Android) with a Python backend, built to help students prepare for campus placements end-to-end.

### 🏠 Home Dashboard
Real-time overview of your prep progress: current Resume Score, Interview Readiness, Communication Score, daily streak, today's practice goal, and a merged recent-activity feed — all computed live from your actual usage, not placeholder data.

> **Example:** open the app after doing a mock interview and a resume
> scan earlier in the day — Home shows your updated Resume Score,
> today's streak count, and a feed like "Technical Round — Scored 78%"
> and "Resume re-scanned — ATS score: 82%", both time-stamped.

### 📄 Resume Analyzer / ATS Checker
Upload a PDF resume and paste a target job description. The backend:
- Extracts text from the PDF
- Identifies skills present in both the resume and job description (spaCy-based matching against a skill vocabulary)
- Computes an ATS match score — a weighted blend of keyword-match ratio and TF-IDF/cosine text similarity
- Runs Named Entity Recognition to pull out organizations, dates, and locations from the resume
- Calls an LLM (Groq/Llama 3.3) to generate specific, actionable improvement suggestions

> **Example:** upload your resume and paste a "Flutter Developer" job
> posting. You get back something like: **ATS Score: 74%**, matched
> skills `Flutter, Firebase, Git`, missing skills `REST API, CI/CD`, and
> a suggestion like *"Add a project bullet demonstrating REST API
> integration."* Results are saved to your profile automatically.

### 🎤 AI Mock Interviews
Pick an interviewer **persona** (Google, Microsoft, Amazon, Startup Founder, HR Manager), a **round type** (Technical, Behavioral, HR, Resume-based, Project-based, or general Chat), and a **difficulty** (Easy/Medium/Hard). The app runs a real interview loop:

1. Backend generates a question tailored to the mode/persona/role/difficulty
2. You answer (typed or spoken) and tap **Check Score** — get an honest score, what you got right, what you missed
3. Tap **Check Answer** any time to reveal the ideal/model answer as short bullet points
4. Tap a suggested doubt chip, or type your own follow-up doubt, for a quick clarifying explanation
5. Tap **Retry** to redo the same question, or **Next Question** to move on — your call

> **Example:** choose *Google* persona, *Technical Round*, *Medium*
> difficulty for a "Backend Developer" role. You get asked "Explain the
> difference between SQL and NoSQL databases." You answer, tap **Check
> Score** → 65%, feedback on what was missed. You tap **Check Answer** →
> see the ideal 4-bullet-point answer. You tap the doubt chip *"What does
> ACID mean?"* → get a 2-line explanation, then hit **Next Question**.

**Voice Interview mode** additionally speaks the question aloud (text-to-speech) and transcribes your spoken answer live (speech-to-text) using the phone's microphone — a fully hands-free mock interview.

### 🧮 Aptitude & Coding Quiz
AI-generated multiple-choice quizzes across four categories — Quantitative Aptitude, Logical Reasoning, Verbal Ability, and Coding/Technical — at a chosen difficulty and question count.

> **Example:** pick *Logical Reasoning*, *Hard*, *10 questions*. Each
> question shows 4 options; pick one and get instant right/wrong
> highlighting plus a short explanation before moving to the next. At the
> end you get a score like **7/10** saved to your history.

### 📈 Progress
A weekly score-trend chart (Mon–Sun, averaged across interview + quiz sessions that week), gamified XP/Level/Coins computed from real session history, and weekly/monthly activity summaries.

> **Example:** after a week of practicing, Progress shows a line chart
> dipping on days you skipped and rising on days you did 2-3 sessions,
> along with something like **Level 3 · 640 XP · 64 Coins** and "5
> sessions this week."

### 👤 Profile
Editable college, branch, graduation year, skills, and social links (GitHub/LinkedIn/Portfolio), saved per account. Shows your latest resume ATS score at a glance.

> **Example:** tap the edit icon, add skills like `Python`, `Flutter`,
> `SQL` as chips, paste your GitHub/LinkedIn URLs, hit Save — it's there
> next time you log in, on any device.

### 🔐 Authentication
Email/Password, Google Sign-In, or Guest mode (full functionality without an account — progress just isn't saved permanently). Backed by Firebase Authentication + Firestore for persistence.

> **Example:** open the app for the first time and it drops you straight
> into Home as a guest — try everything immediately. A small banner
> ("browsing as guest") lets you log in with Google anytime to start
> saving your progress permanently.

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

FastAPI service combining classic NLP with an LLM to power the AI-driven modules above.

### Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI + Uvicorn (ASGI) |
| NLP | spaCy (`en_core_web_sm`) — skill extraction, named entity recognition |
| ATS scoring | scikit-learn — TF-IDF + cosine similarity, blended with keyword-match ratio |
| PDF parsing | pdfplumber |
| LLM | Groq API — Llama 3.3 70B (question generation, answer evaluation, model answers, doubts, resume suggestions, quiz generation) |
| Config | pydantic-settings (`.env`-based) |
| Hosting | Render (free tier, auto-deploy from `main`) |

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Health check |
| POST | `/api/v1/resume/analyze` | Upload PDF + job description → ATS score, skill match, AI suggestions |
| POST | `/api/v1/interview/question` | Generate an interview question (mode, persona, role, difficulty) |
| POST | `/api/v1/interview/answer` | Check the candidate's score → score, feedback, strengths, improvements, suggested doubts |
| POST | `/api/v1/interview/model-answer` | Reveal the ideal/correct answer to a question |
| POST | `/api/v1/interview/doubt` | Answer a candidate's own follow-up doubt |
| POST | `/api/v1/interview/refine-answer` | Clean up typos/Hinglish into proper English before submitting |
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
│   ├── interview_service.py   # Groq LLM — questions, scoring, model answers, doubts
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
