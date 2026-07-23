import json
from groq import Groq

from app.core.config import settings

_client = Groq(api_key=settings.groq_api_key)
_MODEL = "llama-3.3-70b-versatile"

_DIFFICULTY_GUIDANCE = {
    "Easy": "Keep it foundational and approachable — basic concepts, definitions, and simple scenarios. Suitable for a beginner or someone early in their prep.",
    "Medium": "A realistic, moderately challenging question appropriate for an average candidate applying for this role — not trivial, not a trick question.",
    "Hard": "A genuinely challenging, in-depth question that would test a strong, experienced candidate — can involve edge cases, trade-offs, or deeper reasoning.",
}


def generate_question(
    mode: str,
    persona: str,
    job_role: str,
    previous_questions: list[str],
    difficulty: str = "Medium",
) -> str:
    avoid = "\n".join(f"- {q}" for q in previous_questions) or "(none yet)"
    difficulty_note = _DIFFICULTY_GUIDANCE.get(difficulty, _DIFFICULTY_GUIDANCE["Medium"])

    prompt = f"""You are acting as a {persona}-style interviewer conducting a {mode} for a
{job_role} candidate. Ask exactly ONE interview question appropriate for this round.

Difficulty level: {difficulty}. {difficulty_note}

Do NOT repeat or closely rephrase any of these already-asked questions:
{avoid}

Return ONLY the question text. No preamble, no numbering, no quotation marks."""

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip().strip('"')


def evaluate_answer(
    mode: str,
    persona: str,
    job_role: str,
    question: str,
    answer: str,
    difficulty: str = "Medium",
) -> dict:
    difficulty_note = _DIFFICULTY_GUIDANCE.get(difficulty, _DIFFICULTY_GUIDANCE["Medium"])

    prompt = f"""You are an expert {persona}-style interviewer evaluating a candidate's answer
in a {mode} for a {job_role} role. The candidate selected difficulty level: {difficulty}.

QUESTION: {question}
CANDIDATE ANSWER: {answer}

Evaluate the answer honestly (don't be overly generous) and respond with ONLY valid JSON in
exactly this shape, no markdown fences, no extra text:
{{
  "score": <integer 0-100>,
  "feedback": "<2-3 sentence overall feedback, direct and specific>",
  "strengths": ["<short strength>", "<short strength>"],
  "improvements": ["<short improvement>", "<short improvement>"],
  "next_question": "<the next interview question for this {mode}, different from the question above, at {difficulty} difficulty: {difficulty_note}>"
}}"""

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def refine_answer(raw_text: str) -> str:
    """Takes a raw typed/transcribed answer — possibly containing typos,
    Hindi/Hinglish, or mixed-language phrasing — and rewrites it as a
    clean, grammatically correct, professional English interview answer,
    preserving the original meaning and every point the candidate made."""
    prompt = f"""The following is a candidate's interview answer, typed or transcribed as-is.
It may contain typos, be in Hindi, Hinglish, or a mix of languages.

Rewrite it as a clean, grammatically correct, professional English answer that an interviewer
would read. Preserve the original meaning and every point made — do not add new content, do not
remove substance, just fix language, grammar, and clarity. If it's already clean English, make
only minor polish.

Return ONLY the rewritten answer text. No preamble, no quotes, no explanation.

ORIGINAL ANSWER:
{raw_text}"""

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip().strip('"')
