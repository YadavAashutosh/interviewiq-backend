from pydantic import BaseModel
from typing import List


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_index: int
    explanation: str


class QuizGenerateRequest(BaseModel):
    category: str          # "Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Coding/Technical"
    difficulty: str = "Medium"
    num_questions: int = 5


class QuizGenerateResponse(BaseModel):
    questions: List[QuizQuestion]
