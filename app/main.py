from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.resume import router as resume_router
from app.api.v1.interview import router as interview_router
from app.api.v1.quiz import router as quiz_router

app = FastAPI(title="InterviewIQ AI Backend", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your app's domain before real deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(quiz_router)


@app.get("/")
def health_check():
    return {"status": "InterviewIQ AI backend is running"}
