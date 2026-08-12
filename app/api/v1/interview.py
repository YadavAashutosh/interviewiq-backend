from fastapi import APIRouter, HTTPException

from app.models.interview_schemas import (
    InterviewQuestionRequest,
    InterviewQuestionResponse,
    InterviewAnswerRequest,
    InterviewAnswerResponse,
    DoubtRequest,
    DoubtResponse,
    RefineAnswerRequest,
    RefineAnswerResponse,
)
from app.services.interview_service import generate_question, check_answer, ask_doubt, refine_answer

router = APIRouter(prefix="/api/v1/interview", tags=["interview"])


@router.post("/question", response_model=InterviewQuestionResponse)
async def get_question(req: InterviewQuestionRequest):
    """Used both for the very first question AND for the 'Next Question'
    button — same generation logic either way."""
    try:
        question = generate_question(
            req.mode, req.persona, req.job_role, req.previous_questions, req.difficulty
        )
        return InterviewQuestionResponse(question=question)
    except Exception as e:
        raise HTTPException(500, f"Could not generate question: {e}")


@router.post("/answer", response_model=InterviewAnswerResponse)
async def submit_answer(req: InterviewAnswerRequest):
    """Checks the candidate's answer to the CURRENT question — returns
    score/feedback/strengths/improvements (unchanged from before) plus 3
    suggested follow-up doubts. Does NOT advance to a new question."""
    try:
        result = check_answer(
            req.mode, req.persona, req.job_role, req.question, req.answer, req.difficulty
        )
        return InterviewAnswerResponse(**result)
    except Exception as e:
        raise HTTPException(500, f"Could not evaluate answer: {e}")


@router.post("/doubt", response_model=DoubtResponse)
async def doubt(req: DoubtRequest):
    try:
        answer = ask_doubt(req.mode, req.job_role, req.question, req.answer, req.doubt)
        return DoubtResponse(answer=answer)
    except Exception as e:
        raise HTTPException(500, f"Could not answer doubt: {e}")


@router.post("/refine-answer", response_model=RefineAnswerResponse)
async def refine(req: RefineAnswerRequest):
    if not req.raw_text.strip():
        raise HTTPException(400, "Nothing to refine — the answer is empty.")
    try:
        refined = refine_answer(req.raw_text)
        return RefineAnswerResponse(refined_text=refined)
    except Exception as e:
        raise HTTPException(500, f"Could not refine answer: {e}")
