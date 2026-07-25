from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_score(job_description: str, candidate_text: str) -> float:
    embeddings = model.encode(
        [job_description, candidate_text]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(float(similarity) * 100, 2)


def score_candidate(candidate: dict, job_description: str) -> dict:
    name = candidate.get("name", "Unknown Candidate")
    skills = candidate.get("skills", [])
    experience = float(candidate.get("experience", 0))
    education = candidate.get("education", "")
    projects = int(candidate.get("projects", 0))
    resume_summary = candidate.get("resume_summary", "")

    candidate_text = f"""
    Education: {education}
    Skills: {", ".join(skills)}
    Experience: {experience} years
    Projects: {projects}
    Resume summary: {resume_summary}
    """

    semantic_score = calculate_semantic_score(
        job_description,
        candidate_text
    )

    experience_score = min(experience * 5, 15)
    project_score = min(projects * 2.5, 10)

    final_score = (
        semantic_score * 0.75
        + experience_score
        + project_score
    )

    return {
        "name": name,
        "score": round(min(final_score, 100), 2),
        "semantic_match": semantic_score,
        "experience_score": round(experience_score, 2),
        "project_score": round(project_score, 2)
    }


def rank_candidates(
    candidates: list[dict],
    job_description: str
) -> list[dict]:
    ranked_candidates = []

    for candidate in candidates:
        result = score_candidate(
            candidate,
            job_description
        )
        ranked_candidates.append(result)

    ranked_candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    for index, candidate in enumerate(
        ranked_candidates,
        start=1
    ):
        candidate["rank"] = index

    return ranked_candidates
