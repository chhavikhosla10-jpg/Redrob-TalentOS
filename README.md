# 🚀 Redrob TalentOS

AI-powered candidate ranking system for the Redrob Intelligent Candidate Discovery & Ranking Challenge.

## 🌐 Live Demo
https://redrob-talentos.onrender.com

## 📘 API Documentation
https://redrob-talentos.onrender.com/docs

## 📌 What this repo contains

- `rank.py` — CPU-only heuristic ranker for the official candidates dataset
- `outputs/Neura_Nova.csv` — final top-100 ranked candidate submission file
- `main.py` — FastAPI demo endpoint for Render deployment
- `requirements.txt` — minimal dependencies for demo deployment
- `submission_metadata.yaml` — metadata template for the submission portal

## 🧠 Methodology

The ranker scores candidates using the official JD requirements:

- Applied ML / AI production experience
- Search, ranking, retrieval, embeddings, vector databases, and recommendation systems
- Python and production engineering background
- Ranking evaluation exposure such as NDCG, MAP, MRR, and A/B testing
- Location and relocation fit for Noida/Pune/India-based hiring
- Redrob behavioral signals such as recruiter response rate, recent activity, notice period, profile completeness, and GitHub activity

The system also down-weights weak-fit or risky profiles such as keyword-stuffed profiles, non-technical roles, long inactive candidates, consulting-only backgrounds, and profiles with suspicious/impossible skill signals.

## ▶️ How to reproduce the CSV

Place the official `candidates.jsonl` file in the repo root, then run:

```bash
python rank.py --candidates candidates.jsonl --out outputs/Neura_Nova.csv
```

Validate using the official validator:

```bash
python validate_submission.py outputs/Neura_Nova.csv
```

## 📄 Submission File Format

The generated CSV follows the required columns:

```csv
candidate_id,rank,score,reasoning
```

It contains exactly 100 ranked candidates.

## 👥 Team

**Team Name:** Neura_Nova  
**Team Leader:** Chhavi Khosla
