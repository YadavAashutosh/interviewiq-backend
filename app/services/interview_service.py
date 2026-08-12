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

# Applied everywhere the LLM writes explanation text, so nothing ever
# comes back as a wall of text or a huge code dump that would overflow a
# mobile screen. Points, not paragraphs.
_BREVITY_RULE = """Keep everything SHORT — bullet points, not paragraphs. Each point under
15 words. If code is truly necessary, at most 2 short lines, no long blocks, no comments —
prefer a plain-English point over code whenever possible."""


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

Keep the question itself concise — 1 to 3 sentences, no long setup or preamble.

Do NOT repeat or closely rephrase any of these already-asked questions:
{avoid}

Return ONLY the question text. No preamble, no numbering, no quotation marks."""

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip().strip('"')


def check_answer(
    mode: str,
    persona: str,
    job_role: str,
    question: str,
    answer: str,
    difficulty: str = "Medium",
) -> dict:
    """'Check Score' — evaluates the candidate's own answer: score, honest
    feedback on right/wrong, strengths, improvements (same core signal as
    before), plus 3 short follow-up doubts a beginner would likely still
    have. Does NOT reveal the ideal answer — that's a separate action."""
    difficulty_note = _DIFFICULTY_GUIDANCE.get(difficulty, _DIFFICULTY_GUIDANCE["Medium"])

    prompt = f"""You are an expert {persona}-style interviewer evaluating a candidate's answer
in a {mode} for a {job_role} role. Difficulty level: {difficulty}. {difficulty_note}

QUESTION ASKED: {question}
CANDIDATE'S ANSWER: {answer}

Evaluate the answer honestly (don't be overly generous) — say clearly what the candidate got
right and what they got wrong or missed.

{_BREVITY_RULE}

Also prepare exactly 3 short follow-up "doubt" clarifications — basic things a candidate at
this level would likely still be confused about after this question (e.g. "what does X mean",
"why does Y happen", "difference between A and B"). Each doubt's answer must be 2-3 short
bullet points, not a paragraph.

Respond with ONLY valid JSON in exactly this shape, no markdown fences, no extra text:
{{
  "score": <integer 0-100>,
  "feedback": "<short overall feedback, under 40 words, direct and specific about what was right/wrong>",
  "strengths": ["<short strength, under 12 words>", "<short strength, under 12 words>"],
  "improvements": ["<short improvement, under 12 words>", "<short improvement, under 12 words>"],
  "suggested_doubts": [
    {{"question": "<short common doubt question>", "points": ["<short point>", "<short point>"]}},
    {{"question": "<short common doubt question>", "points": ["<short point>", "<short point>"]}},
    {{"question": "<short common doubt question>", "points": ["<short point>", "<short point>"]}}
  ]
}}"""

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def get_model_answer(
    mode: str,
    persona: str,
    job_role: str,
    question: str,
    difficulty: str = "Medium",
) -> list[str]:
    """'Check Answer' — the ideal/correct answer to the question itself
    (not an evaluation of what the candidate said), as short bullet
    points — what a strong candidate would ideally say."""
    difficulty_note = _DIFFICULTY_GUIDANCE.get(difficulty, _DIFFICULTY_GUIDANCE["Medium"])

    prompt = f"""You are an expert {persona}-style interviewer for a {mode} at {difficulty}
difficulty for a {job_role} role. {difficulty_note}

QUESTION: {question}

Give the ideal, correct answer to this question as 3-5 short bullet points — what a strong
candidate would ideally say. {_BREVITY_RULE}

Respond with ONLY valid JSON in exactly this shape, no markdown fences, no extra text:
{{
  "points": ["<short point>", "<short point>", "<short point>"]
}}"""

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    return data.get("points", [])


def ask_doubt(mode: str, job_role: str, question: str, answer: str, doubt: str) -> list[str]:
    """Answers a candidate's own free-typed follow-up doubt — as short
    bullet points, not a paragraph."""
    prompt = f"""You are a friendly, patient technical mentor helping a candidate preparing for
a {mode} interview for a {job_role} role understand something better.

ORIGINAL INTERVIEW QUESTION: {question}
CANDIDATE'S ANSWER: {answer}
CANDIDATE'S FOLLOW-UP DOUBT: {doubt}

{_BREVITY_RULE}

Answer the doubt as 2-4 short bullet points, simple enough for a beginner.

Respond with ONLY valid JSON in exactly this shape, no markdown fences, no extra text:
{{
  "points": ["<short point>", "<short point>"]
}}"""

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    return data.get("points", [])


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
