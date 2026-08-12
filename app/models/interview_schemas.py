from pydantic import BaseModel
from typing import List


class InterviewQuestionRequest(BaseModel):
    mode: str
    persona: str
    job_role: str
    difficulty: str = "Medium"
    previous_questions: List[str] = []


class InterviewQuestionResponse(BaseModel):
    question: str


class InterviewAnswerRequest(BaseModel):
    mode: str
    persona: str
    job_role: str
    difficulty: str = "Medium"
    question: str
    answer: str


class FollowUpDoubt(BaseModel):
    question: str
    answer: str


class InterviewAnswerResponse(BaseModel):
    # Same core evaluation as before — score, feedback, strengths,
    # improvements are unchanged. next_question is REMOVED from this
    # response: advancing to the next question is now a separate,
    # explicit action (the "Next" button), not automatic.
    score: int
    feedback: str
    strengths: List[str]
    improvements: List[str]
    suggested_doubts: List[FollowUpDoubt]


class DoubtRequest(BaseModel):
    mode: str
    job_role: str
    question: str
    answer: str
    doubt: str


class DoubtResponse(BaseModel):
    answer: str


class RefineAnswerRequest(BaseModel):
    raw_text: str


class RefineAnswerResponse(BaseModel):
    refined_text: str
