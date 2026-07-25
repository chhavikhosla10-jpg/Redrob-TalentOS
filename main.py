from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

from ranking_engine import rank_candidates


app = FastAPI(
    title="Redrob TalentOS API",
    description="AI-powered candidate ranking system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Candidate(BaseModel):
    name: str
    skills: List[str]
    experience: float = Field(ge=0)
    education: str
    projects: int = Field(ge=0)
    resume_summary: str


class RankingRequest(BaseModel):
    job_description: str
    candidates: List[Candidate]


@app.get("/")
def home():
    return {
        "project": "Redrob TalentOS",
        "status": "running",
        "message": "AI candidate-ranking API is live"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/rank")
def rank(request: RankingRequest):
    candidates = [
        candidate.model_dump()
        for candidate in request.candidates
    ]

    results = rank_candidates(
        candidates=candidates,
        job_description=request.job_description
    )

    return {
        "total_candidates": len(results),
        "ranked_candidates": results
    }