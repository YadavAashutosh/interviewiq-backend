import json
from groq import Groq

from app.core.config import settings

_client = Groq(api_key=settings.groq_api_key)
_MODEL = "llama-3.3-70b-versatile"


def generate_question(mode: str, persona: str, job_role: str, previous_questions: list[str]) -> str:
    avoid = "\n".join(f"- {q}" for q in previous_questions) or "(none yet)"
    prompt = f"""You are acting as a {persona}-style interviewer conducting a {mode} for a
{job_role} candidate. Ask exactly ONE interview question appropriate for this round.

Do NOT repeat or closely rephrase any of these already-asked questions:
{avoid}

Return ONLY the question text. No preamble, no numbering, no quotation marks."""

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip().strip('"')


def evaluate_answer(mode: str, persona: str, job_role: str, question: str, answer: str) -> dict:
    prompt = f"""You are an expert {persona}-style interviewer evaluating a candidate's answer
in a {mode} for a {job_role} role.

QUESTION: {question}
CANDIDATE ANSWER: {answer}

Evaluate the answer honestly (don't be overly generous) and respond with ONLY valid JSON in
exactly this shape, no markdown fences, no extra text:
{{
  "score": <integer 0-100>,
  "feedback": "<2-3 sentence overall feedback, direct and specific>",
  "strengths": ["<short strength>", "<short strength>"],
  "improvements": ["<short improvement>", "<short improvement>"],
  "next_question": "<the next interview question for this {mode}, different from the question above, appropriate difficulty progression>"
}}"""

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)