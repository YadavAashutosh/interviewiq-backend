from pydantic import BaseModel
from typing import List


class SkillMatch(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]


class ResumeAnalysisResponse(BaseModel):
    ats_score: float
    resume_skills: List[str]
    job_skills: List[str]
    skill_match: SkillMatch
    entities: dict
    ai_suggestions: List[str]
