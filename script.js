const candidateContainer = document.getElementById("candidateContainer");
const resultsSection = document.getElementById("resultsSection");
const resultsContainer = document.getElementById("results");
const loadingBox = document.getElementById("loading");

let candidateCount = 0;

function addCandidate() {
  candidateCount++;

  const candidateCard = document.createElement("div");
  candidateCard.className = "candidate-card";

  candidateCard.innerHTML = `
    <div class="candidate-card-header">
      <h3>Candidate ${candidateCount}</h3>

      ${
        candidateCount > 1
          ? `
            <button
              type="button"
              class="remove-button"
              onclick="removeCandidate(this)"
            >
              Remove
            </button>
          `
          : ""
      }
    </div>

    <div class="form-grid">
      <div class="form-group">
        <label>Candidate Name</label>
        <input
          type="text"
          class="candidate-name"
          placeholder="Example: Alice Johnson"
        />
      </div>

      <div class="form-group">
        <label>Skills</label>
        <input
          type="text"
          class="candidate-skills"
          placeholder="Python, FastAPI, SQL, Docker"
        />
      </div>

      <div class="form-group">
        <label>Experience in years</label>
        <input
          type="number"
          class="candidate-experience"
          placeholder="3"
          min="0"
        />
      </div>

      <div class="form-group">
        <label>Education</label>
        <input
          type="text"
          class="candidate-education"
          placeholder="B.Tech Computer Science"
        />
      </div>

      <div class="form-group">
        <label>Number of Projects</label>
        <input
          type="number"
          class="candidate-projects"
          placeholder="4"
          min="0"
        />
      </div>

      <div class="form-group full-width">
        <label>Resume Summary</label>
        <textarea
          class="candidate-summary"
          placeholder="Write the candidate's experience, projects and achievements..."
        ></textarea>
      </div>
    </div>
  `;

  candidateContainer.appendChild(candidateCard);
}

function removeCandidate(button) {
  const candidateCard = button.closest(".candidate-card");
  candidateCard.remove();

  updateCandidateTitles();
}

function updateCandidateTitles() {
  const candidateCards = document.querySelectorAll(".candidate-card");

  candidateCards.forEach((card, index) => {
    const heading = card.querySelector("h3");

    if (heading) {
      heading.textContent = `Candidate ${index + 1}`;
    }
  });

  candidateCount = candidateCards.length;
}

function collectCandidates() {
  const candidateCards = document.querySelectorAll(".candidate-card");

  return Array.from(candidateCards).map((card) => {
    const skillsText = card
      .querySelector(".candidate-skills")
      .value.trim();

    return {
      name: card.querySelector(".candidate-name").value.trim(),

      skills: skillsText
        .split(",")
        .map((skill) => skill.trim())
        .filter((skill) => skill.length > 0),

      experience:
        Number(card.querySelector(".candidate-experience").value) || 0,

      education:
        card.querySelector(".candidate-education").value.trim(),

      projects:
        Number(card.querySelector(".candidate-projects").value) || 0,

      resume_summary:
        card.querySelector(".candidate-summary").value.trim()
    };
  });
}

function validateForm(jobDescription, candidates) {
  if (!jobDescription) {
    alert("Please enter the job description.");
    return false;
  }

  if (candidates.length === 0) {
    alert("Please add at least one candidate.");
    return false;
  }

  for (let index = 0; index < candidates.length; index++) {
    const candidate = candidates[index];

    if (!candidate.name) {
      alert(`Please enter the name of Candidate ${index + 1}.`);
      return false;
    }

    if (candidate.skills.length === 0) {
      alert(`Please enter the skills of Candidate ${index + 1}.`);
      return false;
    }

    if (!candidate.education) {
      alert(`Please enter the education of Candidate ${index + 1}.`);
      return false;
    }

    if (!candidate.resume_summary) {
      alert(
        `Please enter the resume summary of Candidate ${index + 1}.`
      );
      return false;
    }
  }

  return true;
}

async function rankCandidates() {
  const jobDescriptionElement =
    document.getElementById("jobDescription");

  const jobDescription = jobDescriptionElement.value.trim();
  const candidates = collectCandidates();

  if (!validateForm(jobDescription, candidates)) {
    return;
  }

  loadingBox.classList.remove("hidden");
  resultsSection.classList.add("hidden");
  resultsContainer.innerHTML = "";

  const requestBody = {
    job_description: jobDescription,
    candidates: candidates
  };

  console.log("Sending data to backend:", requestBody);
try {
  const response = await fetch(
    "https://redrob-ai-ranking-w00r.onrender.com/rank",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(requestBody)
    }
  );

 
}


    const responseText = await response.text();

    let data;

    try {
      data = JSON.parse(responseText);
    } catch {
      data = responseText;
    }

    if (!response.ok) {
      console.error("Backend error:", data);

      throw new Error(
        typeof data === "string"
          ? data
          : JSON.stringify(data, null, 2)
      );
    }

    console.log("Backend response:", data);

    const rankings = Array.isArray(data)
      ? data
      : data.rankings ||
        data.results ||
        data.ranked_candidates ||
        [];

    displayResults(rankings);
  } catch (error) {
    console.error("Ranking error:", error);

    resultsContainer.innerHTML = `
      <div class="result-card error-card">
        <h3>Unable to analyze candidates</h3>

        <p>
          The backend returned an error.
        </p>

        <pre>${escapeHtml(error.message)}</pre>
      </div>
    `;

    resultsSection.classList.remove("hidden");
  } finally {
    loadingBox.classList.add("hidden");
  }
}

function displayResults(rankings) {
  if (!rankings || rankings.length === 0) {
    resultsContainer.innerHTML = `
      <div class="result-card">
        <h3>No ranking results received</h3>
        <p>
          The backend responded successfully but did not return any candidates.
        </p>
      </div>
    `;

    resultsSection.classList.remove("hidden");
    return;
  }

  resultsContainer.innerHTML = rankings
    .map((candidate, index) => {
      const candidateName =
        candidate.name ||
        candidate.candidate_name ||
        candidate.candidate ||
        `Candidate ${index + 1}`;

      const scoreValue =
        candidate.score ??
        candidate.total_score ??
        candidate.overall_score ??
        candidate.match_score ??
        0;

      const score = Math.round(Number(scoreValue));

      const semanticScoreValue =
        candidate.semantic_score ??
        candidate.semantic_match ??
        candidate.similarity_score ??
        score;

      const semanticScore = Math.round(
        Number(semanticScoreValue)
      );

      const recommendation =
        score >= 85
          ? "Highly Recommended"
          : score >= 70
          ? "Recommended"
          : score >= 55
          ? "Potential Match"
          : "Low Match";

      return `
        <article class="result-card">
          <div class="result-top">
            <div>
              <div class="result-rank">
                ${getRankIcon(index)} Rank ${index + 1}
              </div>

              <div class="result-name">
                ${escapeHtml(candidateName)}
              </div>
            </div>

            <div class="result-score">
              ${score}%
            </div>
          </div>

          <div class="score-bar">
            <div
              class="score-progress"
              style="width: ${Math.min(
                Math.max(score, 0),
                100
              )}%"
            ></div>
          </div>

          <div class="result-details">
            <span>AI Match: ${semanticScore}%</span>
            <span>${recommendation}</span>
          </div>
        </article>
      `;
    })
    .join("");

  resultsSection.classList.remove("hidden");

  resultsSection.scrollIntoView({
    behavior: "smooth",
    block: "start"
  });
}

function getRankIcon(index) {
  if (index === 0) {
    return "🥇";
  }

  if (index === 1) {
    return "🥈";
  }

  if (index === 2) {
    return "🥉";
  }

  return "🏅";
}

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = String(value);
  return div.innerHTML;
}

window.addCandidate = addCandidate;
window.removeCandidate = removeCandidate;
window.rankCandidates = rankCandidates;

document.addEventListener("DOMContentLoaded", () => {
  addCandidate();
});