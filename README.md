# 🚀 GitHub PR Review System (Microservices-Based)

An AI-powered microservices-based system to automate code review for GitHub Pull Requests. It integrates with GitHub’s API to fetch PR files, processes the analysis in the background using Celery, and utilizes LLM (via Groq) to identify potential issues and suggest improvements.

---

## API Documentation: https://documenter.getpostman.com/view/32119544/2sB2cUB3Vs

---

## 🧩 Tech Stack

- **Backend Frameworks**: Django, Django REST Framework, Django Ninja
- **Background Processing**: Celery with Redis
- **LLM Integration**: Groq API for code analysis
- **Authentication**: GitHub OAuth token (PAT)
- **Containerization**: Docker, Docker Compose
- **Architecture**: Microservices (Request Handler + Code Reviewer)

---

## 🏗️ System Architecture

```
                +---------------------+
                |   Client / Frontend |
                +----------+----------+
                           |
                           ▼
            +-------------------------------+
            | Request Handler (Django-Ninja)|
            | - Accepts PR Analysis Requests|
            | - Validates Input             |
            | - Returns analysis_id         |
            +-------------------------------+
                           |
                           ▼
     +---------------------------------------------+
     |    Code Reviewer (DRF + Celery with Redis)  |
     | - Pulls PR files from GitHub using API      |
     | - Processes code using Groq LLM             |
     | - Stores result linked to analysis_id       |
     +---------------------------------------------+
                           |
                           ▼
            Result accessible via analysis_id

```

---

## 📦 Features

- ✅ Submit PR for analysis via GitHub URL, branch, and PR number
- ✅ Background task for code review using Celery
- ✅ LLM-based suggestions and issue identification
- ✅ Retrieve analysis result using `analysis_id`
- ✅ Dockerized setup for easy deployment

---

## 🔐 Authentication

Users must provide a **GitHub Personal Access Token (PAT)** with appropriate permissions to access private repositories and PR data.

---

## 📬 Example Request Payload

```json
{
  "repo_url": "https://github.com/username/repo",
  "pr_branch": "feature-branch",
  "pr_number": 42,
  "github_token": "ghp_yourtokenhere"
}
```

---

## 📥 API Workflow

1. **Submit a PR analysis request** → returns `analysis_id`
2. **Background task** starts analyzing PR
3. **Use the analysis_id** on another endpoint to fetch results

---

## 🐳 Run Locally with Docker

### 🔧 Prerequisites
- Docker & Docker Compose installed

### 🛠️ Steps

```bash
# Clone the repository
git clone https://github.com/your-username/github-pr-review-api.git
cd github-pr-review-api

# Build and start the containers
docker-compose up --build (docker compose up --build)

```

### 🌐 Access the services
- **Request Handler API**: `http://127.0.0.1:8000/api/analyze-pr/`
- **Result Display API**: `http://127.0.0.1:8000/api/view-status/<analysis_id>/`
- **Celery Worker**: Runs in the background, no direct UI

---

## ❌ Error Handling

The system returns meaningful error messages for:

- Missing fields in request body
- Invalid branch or PR number
- Inaccessible private repo due to invalid token
- Files not found in the given branch

Check the [API Docs](https://documenter.getpostman.com/view/32119544/2sB2cUB3Vs) or error response section in this README for detailed examples.

---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---
