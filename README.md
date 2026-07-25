# 🚀 Redrob TalentOS – AI Candidate Ranking System

An AI-powered Candidate Ranking System built for the **Redrob Intelligent Candidate Discovery & Ranking Challenge**. The application analyzes candidate profiles against a job description and intelligently ranks candidates based on their relevance using an AI-powered scoring engine.

---

## 🌐 Live Demo

**Frontend:** https://redrob-talent-os.vercel.app

**Backend API:** https://redrob-ai-ranking-w00r.onrender.com

**API Documentation:** https://redrob-ai-ranking-w00r.onrender.com/docs

---

## 📌 Features

- 🤖 AI-powered candidate ranking
- 📄 Job description analysis
- 👨‍💻 Multiple candidate profile comparison
- 📊 Match score calculation
- 🏆 Automatic candidate ranking
- 📈 Visual score bars
- 💡 Recommendation labels (Highly Recommended, Recommended, Potential Match, Low Match)
- 🌐 REST API using FastAPI
- 📱 Responsive and clean user interface

---

## 🛠 Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- FastAPI
- Uvicorn

### Deployment
- Vercel (Frontend)
- Render (Backend)

---

## 📂 Project Structure

```text
.
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── main.py
│   ├── ranking_engine.py
│   ├── requirements.txt
│   └── models.py
│
└── README.md
```

---

## 🚀 How It Works

1. Enter the Job Description.
2. Add one or more candidate profiles.
3. Click **Analyze Candidates**.
4. The AI evaluates each candidate.
5. Candidates are ranked according to their relevance.
6. Match scores and recommendations are displayed instantly.

---

## 🎯 Ranking Parameters

The ranking engine evaluates candidates using multiple factors:

- Skills Match
- Years of Experience
- Educational Qualification
- Number of Projects
- Resume Summary Relevance
- Overall Job Description Similarity

---

## 📸 Sample Output

The application displays:

- 🥇 Candidate Ranking
- 📊 Match Percentage
- 📈 Score Progress Bar
- 💼 Recommendation Status

Example:

```
Rank 1 — Priya Sharma — 67%
AI Match: 67%
Recommendation: Potential Match

Rank 2 — Rahul Verma — 37%
AI Match: 37%
Recommendation: Low Match
```

---

## ⚙️ Run Locally

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

### Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

### Frontend

Simply open:

```
index.html
```

or run using VS Code Live Server.

---

## 📚 API Endpoint

### Rank Candidates

```
POST /rank
```

Example Request

```json
{
  "job_description": "AI Engineer",
  "candidates": [
    {
      "name": "Priya Sharma",
      "skills": ["Python", "FastAPI", "Machine Learning"],
      "experience": 4,
      "education": "B.Tech Computer Science",
      "projects": 5,
      "resume_summary": "Experienced AI Engineer..."
    }
  ]
}
```

---

## 🔮 Future Enhancements

- Resume PDF Upload
- NLP-based Resume Parsing
- Semantic Embeddings
- LLM-powered Candidate Insights
- Authentication & Recruiter Dashboard
- Candidate Database Integration

---

## 👥 Team

**Team Name:** Neura_Nova

**Team Leader:** Chhavi Khosla

---

## 📄 License

This project was developed for the **Redrob Intelligent Candidate Discovery & Ranking Challenge** and is intended for educational and demonstration purposes.
