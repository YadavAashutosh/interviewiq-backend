from fastapi import APIRouter, HTTPException

from app.models.interview_schemas import (
    InterviewQuestionRequest,
    InterviewQuestionResponse,
    InterviewAnswerRequest,
    InterviewAnswerResponse,
    ModelAnswerRequest,
    ModelAnswerResponse,
    DoubtRequest,
    DoubtResponse,
    RefineAnswerRequest,
    RefineAnswerResponse,
)
from app.services.interview_service import (
    generate_question,
    check_answer,
    get_model_answer,
    ask_doubt,
    refine_answer,
)

router = APIRouter(prefix="/api/v1/interview", tags=["interview"])


@router.post("/question", response_model=InterviewQuestionResponse)
async def get_question(req: InterviewQuestionRequest):
    """Used both for the first question AND the 'Next Question' button."""
    try:
        question = generate_question(
            req.mode, req.persona, req.job_role, req.previous_questions, req.difficulty
        )
        return InterviewQuestionResponse(question=question)
    except Exception as e:
        raise HTTPException(500, f"Could not generate question: {e}")


@router.post("/answer", response_model=InterviewAnswerResponse)
async def submit_answer(req: InterviewAnswerRequest):
    """'Check Score' — evaluates the candidate's own typed answer."""
    try:
        result = check_answer(
            req.mode, req.persona, req.job_role, req.question, req.answer, req.difficulty
        )
        return InterviewAnswerResponse(**result)
    except Exception as e:
        raise HTTPException(500, f"Could not evaluate answer: {e}")


@router.post("/model-answer", response_model=ModelAnswerResponse)
async def model_answer(req: ModelAnswerRequest):
    """'Check Answer' — reveals the ideal/correct answer to the question."""
    try:
        points = get_model_answer(
            req.mode, req.persona, req.job_role, req.question, req.difficulty
        )
        return ModelAnswerResponse(points=points)
    except Exception as e:
        raise HTTPException(500, f"Could not get model answer: {e}")


@router.post("/doubt", response_model=DoubtResponse)
async def doubt(req: DoubtRequest):
    try:
        points = ask_doubt(req.mode, req.job_role, req.question, req.answer, req.doubt)
        return DoubtResponse(points=points)
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
