import spacy

nlp = spacy.load("en_core_web_sm")

# Starter skill vocabulary — expand this list as you go, it's the core of
# your "Skill Extraction" NLP feature. Keep lowercase for matching.
SKILL_VOCAB = [
    "python", "java", "javascript", "typescript", "flutter", "dart", "react",
    "node.js", "fastapi", "django", "flask", "sql", "mysql", "postgresql",
    "mongodb", "firebase", "docker", "kubernetes", "git", "github", "aws",
    "gcp", "azure", "machine learning", "deep learning", "nlp", "spacy",
    "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn", "html",
    "css", "rest api", "graphql", "ci/cd", "linux", "data structures",
    "algorithms", "system design",
]


def extract_skills(text: str) -> list[str]:
    text_lower = text.lower()
    found = [skill for skill in SKILL_VOCAB if skill in text_lower]
    return sorted(set(found))


def extract_entities(text: str) -> dict:
    """Named Entity Recognition — pulls organizations, dates, and
    location-like tokens out of the resume (education/experience signals)."""
    doc = nlp(text[:100000])  # cap length for speed on huge PDFs
    entities: dict[str, list[str]] = {"ORG": [], "DATE": [], "GPE": []}
    for ent in doc.ents:
        if ent.label_ in entities and ent.text not in entities[ent.label_]:
            entities[ent.label_].append(ent.text)
    return entities
