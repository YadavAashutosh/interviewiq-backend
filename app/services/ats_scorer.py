from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _text_similarity(resume_text: str, job_description: str) -> float:
    """Raw TF-IDF + cosine similarity (0-100) — captures overall wording
    overlap, not just skills. Used as a secondary signal."""
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(similarity) * 100


def skill_gap(resume_skills: list[str], job_skills: list[str]) -> dict:
    resume_set, job_set = set(resume_skills), set(job_skills)
    return {
        "matched_skills": sorted(resume_set & job_set),
        "missing_skills": sorted(job_set - resume_set),
    }


def compute_ats_score(
    resume_text: str,
    job_description: str,
    resume_skills: list[str],
    job_skills: list[str],
) -> float:
    """Weighted ATS score:
    - 70% keyword match ratio (matched required skills / total required skills)
      — this is what real ATS tools weigh most heavily.
    - 30% TF-IDF text similarity — catches broader wording/context overlap
      beyond just the skill vocabulary.

    If the job description has no recognizable skills at all, falls back
    to pure text similarity so the score isn't artificially zero.
    """
    gap = skill_gap(resume_skills, job_skills)
    text_score = _text_similarity(resume_text, job_description)

    if job_skills:
        keyword_score = (len(gap["matched_skills"]) / len(job_skills)) * 100
        final_score = (0.7 * keyword_score) + (0.3 * text_score)
    else:
        final_score = text_score

    return round(final_score, 2)