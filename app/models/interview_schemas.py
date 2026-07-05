from pydantic import BaseModel
from typing import List


class InterviewQuestionRequest(BaseModel):
    mode: str          # e.g. "Technical Round", "Behavioral Round", "HR Round"
    persona: str        # e.g. "Google", "Startup Founder", "HR Manager"
    job_role: str        # e.g. "Flutter Developer"
    previous_questions: List[str] = []


class InterviewQuestionResponse(BaseModel):
    question: str


class InterviewAnswerRequest(BaseModel):
    mode: str
    persona: str
    job_role: str
    question: str
    answer: str


class InterviewAnswerResponse(BaseModel):
    score: int
    feedback: str
    strengths: List[str]
    improvements: List[str]
    next_question: str
