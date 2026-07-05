import json
from groq import Groq

from app.core.config import settings

_client = Groq(api_key=settings.groq_api_key)
_MODEL = "llama-3.3-70b-versatile"


def generate_quiz(category: str, difficulty: str, num_questions: int) -> list[dict]:
    prompt = f"""Generate exactly {num_questions} multiple-choice {category} questions at
{difficulty} difficulty level, suitable for a campus placement aptitude test.

Respond with ONLY valid JSON in exactly this shape, no markdown fences, no extra text:
{{
  "questions": [
    {{
      "question": "<question text>",
      "options": ["<option A>", "<option B>", "<option C>", "<option D>"],
      "correct_index": <integer 0-3, index of the correct option>,
      "explanation": "<1-2 sentence explanation of the correct answer>"
    }}
  ]
}}

Make sure each question has EXACTLY 4 options, and correct_index correctly points to the
right one. Vary the questions — do not repeat similar questions."""

    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    return data.get("questions", [])
