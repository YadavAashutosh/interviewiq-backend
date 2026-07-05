# InterviewIQ AI — Backend (Stage 2)

Resume Analyzer + ATS Checker: PDF upload → spaCy skill extraction →
TF-IDF/cosine ATS score → Gemini-based improvement suggestions.

## 1. Setup

Open this folder in PyCharm/VS Code (separate from your Flutter project).
In a terminal, inside this folder:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## 2. Add your Gemini key

Rename `.env.example` to `.env`, then open it and paste your real key:

```
GEMINI_API_KEY=your_real_key_here
```

Get a free key at https://aistudio.google.com/apikey (sign in with any
Google account → Create API key). Never put this key in the Flutter app.

## 3. Run the server

```
uvicorn app.main:app --reload --port 8000
```

## 4. Test it

Open http://127.0.0.1:8000/docs in your browser. Expand
**POST /api/v1/resume/analyze** → "Try it out" → upload a real PDF resume,
paste any job description text → Execute.

You should get back JSON with: `ats_score`, `resume_skills`, `job_skills`,
`skill_match` (matched/missing), `entities` (orgs/dates/locations pulled
from the resume), and `ai_suggestions` (4 Gemini-generated bullets).

If `ai_suggestions` comes back with the fallback message instead of real
suggestions, your `.env` key isn't loading — double check the file is
named exactly `.env` (not `.env.txt`) and sits in this folder's root.

## Next (Stage 3)
Wire this endpoint into the Flutter app: a real upload screen replacing
the mock Home scores with a live `ats_score` from this API.
