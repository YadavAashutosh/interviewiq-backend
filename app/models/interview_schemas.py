from pydantic import BaseModel
from typing import List


class InterviewQuestionRequest(BaseModel):
    mode: str
    persona: str
    job_role: str
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


class RefineAnswerRequest(BaseModel):
    raw_text: str


class RefineAnswerResponse(BaseModel):
    refined_text: str
