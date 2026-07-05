from groq import Groq
from app.core.config import settings

_client = Groq(api_key=settings.groq_api_key)
_MODEL = "llama-3.3-70b-versatile"


def generate_resume_suggestions(resume_text: str, job_description: str, missing_skills: list[str]) -> list[str]:
    prompt = f"""You are an expert ATS resume reviewer. Given this resume and job description,
give exactly 4 short, specific, actionable bullet-point suggestions to improve the resume's
match for this job. Focus especially on these missing skills if relevant: {', '.join(missing_skills) or 'none'}.
Keep each suggestion under 20 words. Return ONLY the 4 bullets, no preamble, no numbering.

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{job_description[:2000]}
"""
    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.choices[0].message.content
    lines = [l.strip("-• ").strip() for l in text.strip().split("\n") if l.strip()]
    return lines[:4]