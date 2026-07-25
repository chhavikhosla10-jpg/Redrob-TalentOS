import re
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def calculate_candidate_score(
    job_description: str,
    candidate: dict[str, Any],
) -> dict[str, Any]:

    skills = candidate.get("skills", [])

    candidate_text = " ".join(
        [
            " ".join(skills),
            str(candidate.get("education", "")),
            str(candidate.get("resume_summary", "")),
        ]
    )

    documents = [
        normalize_text(job_description),
        normalize_text(candidate_text),
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )

    vectors = vectorizer.fit_transform(documents)

    similarity_score = float(
        cosine_similarity(
            vectors[0:1],
            vectors[1:2],
        )[0][0]
    )

    job_text = normalize_text(job_description)

    matched_skills = [
        skill
        for skill in skills
        if normalize_text(skill) in job_text
    ]

    skill_score = (
        len(matched_skills) / len(skills)
        if skills
        else 0
    )

    experience = float(candidate.get("experience", 0))
    project_count = float(candidate.get("projects", 0))

    experience_score = min(experience / 5, 1)
    project_score = min(project_count / 6, 1)

    final_score = (
        similarity_score * 45
        + skill_score * 35
        + experience_score * 12
        + project_score * 8
    )

    return {
        **candidate,
        "score": round(final_score, 2),
        "matched_skills": matched_skills,
    }


def rank_candidates(
    job_description: str,
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:

    ranked_candidates = [
        calculate_candidate_score(
            job_description,
            candidate,
        )
        for candidate in candidates
    ]

    ranked_candidates.sort(
        key=lambda candidate: candidate["score"],
        reverse=True,
    )

    for index, candidate in enumerate(
        ranked_candidates,
        start=1,
    ):
        candidate["rank"] = index

    return ranked_candidates