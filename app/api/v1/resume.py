from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.pdf_extractor import extract_text_from_pdf
from app.services.resume_parser import extract_skills, extract_entities
from app.services.ats_scorer import compute_ats_score, skill_gap
from app.services.gemini_service import generate_resume_suggestions
from app.models.schemas import ResumeAnalysisResponse, SkillMatch

router = APIRouter(prefix="/api/v1/resume", tags=["resume"])


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    job_description: str = Form(...),
    file: UploadFile = File(...),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF resumes are supported right now.")

    file_bytes = await file.read()

    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except ValueError as e:
        raise HTTPException(400, str(e))

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    entities = extract_entities(resume_text)
    gap = skill_gap(resume_skills, job_skills)
    ats_score = compute_ats_score(resume_text, job_description, resume_skills, job_skills)

    
    try:
        suggestions = generate_resume_suggestions(resume_text, job_description, gap["missing_skills"])
    except Exception as e:
        print(f"Gemini error: {e}")
        suggestions = ["AI suggestions unavailable right now — check your Gemini API key in .env"]


    return ResumeAnalysisResponse(
        ats_score=ats_score,
        resume_skills=resume_skills,
        job_skills=job_skills,
        skill_match=SkillMatch(**gap),
        entities=entities,
        ai_suggestions=suggestions,
    )
