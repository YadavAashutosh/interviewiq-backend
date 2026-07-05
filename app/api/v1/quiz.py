from fastapi import APIRouter, HTTPException

from app.models.quiz_schemas import QuizGenerateRequest, QuizGenerateResponse, QuizQuestion
from app.services.quiz_service import generate_quiz

router = APIRouter(prefix="/api/v1/quiz", tags=["quiz"])


@router.post("/generate", response_model=QuizGenerateResponse)
async def generate(req: QuizGenerateRequest):
    try:
        raw_questions = generate_quiz(req.category, req.difficulty, req.num_questions)
        questions = [QuizQuestion(**q) for q in raw_questions]
        if not questions:
            raise ValueError("No questions generated")
        return QuizGenerateResponse(questions=questions)
    except Exception as e:
        raise HTTPException(500, f"Could not generate quiz: {e}")
