from fastapi import APIRouter, HTTPException

from app.models.interview_schemas import (
    InterviewQuestionRequest,
    InterviewQuestionResponse,
    InterviewAnswerRequest,
    InterviewAnswerResponse,
    RefineAnswerRequest,
    RefineAnswerResponse,
)
from app.services.interview_service import generate_question, evaluate_answer, refine_answer

router = APIRouter(prefix="/api/v1/interview", tags=["interview"])


@router.post("/question", response_model=InterviewQuestionResponse)
async def get_question(req: InterviewQuestionRequest):
    try:
        question = generate_question(
            req.mode, req.persona, req.job_role, req.previous_questions, req.difficulty
        )
        return InterviewQuestionResponse(question=question)
    except Exception as e:
        raise HTTPException(500, f"Could not generate question: {e}")


@router.post("/answer", response_model=InterviewAnswerResponse)
async def submit_answer(req: InterviewAnswerRequest):
    try:
        result = evaluate_answer(
            req.mode, req.persona, req.job_role, req.question, req.answer, req.difficulty
        )
        return InterviewAnswerResponse(**result)
    except Exception as e:
        raise HTTPException(500, f"Could not evaluate answer: {e}")


@router.post("/refine-answer", response_model=RefineAnswerResponse)
async def refine(req: RefineAnswerRequest):
    if not req.raw_text.strip():
        raise HTTPException(400, "Nothing to refine — the answer is empty.")
    try:
        refined = refine_answer(req.raw_text)
        return RefineAnswerResponse(refined_text=refined)
    except Exception as e:
        raise HTTPException(500, f"Could not refine answer: {e}")
