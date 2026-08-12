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
    points: List[str]   # short bullet-point answer, not a paragraph


class InterviewAnswerResponse(BaseModel):
    # "Check Score" result — unchanged core evaluation: score, feedback
    # (right/wrong), strengths, improvements — plus 3 suggested doubts.
    # Does NOT include the ideal answer — that's a separate action now.
    score: int
    feedback: str
    strengths: List[str]
    improvements: List[str]
    suggested_doubts: List[FollowUpDoubt]


class ModelAnswerRequest(BaseModel):
    mode: str
    persona: str
    job_role: str
    difficulty: str = "Medium"
    question: str


class ModelAnswerResponse(BaseModel):
    points: List[str]   # the ideal/correct answer, as short bullet points


class DoubtRequest(BaseModel):
    mode: str
    job_role: str
    question: str
    answer: str
    doubt: str


class DoubtResponse(BaseModel):
    points: List[str]   # short bullet-point answer, not a paragraph


class RefineAnswerRequest(BaseModel):
    raw_text: str


class RefineAnswerResponse(BaseModel):
    refined_text: str
