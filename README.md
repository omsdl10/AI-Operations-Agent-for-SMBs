# AI Operations Agent for Small Businesses

Production-ready SaaS foundation for automating customer communication, lead management, follow-ups, payment reminders, appointment scheduling, and daily summaries with AI agents.

This repository is being built in staged milestones. The current implementation covers **Stage 1: Project Setup**.

## Monorepo Structure

```text
.
├── backend/   FastAPI application
├── frontend/  React + TypeScript application
├── docker/    Docker support files
└── docs/      Project documentation
```

## Prerequisites

- Docker and Docker Compose
- Node.js 20+
- Python 3.11+

## Environment Setup

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Update values in `.env` as needed.

## Run With Docker

```bash
docker compose up --build
```

Services:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Run Locally

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Health Check

```bash
curl http://localhost:8000/api/v1/health
```

## Git Setup

If this folder is not already a Git repository, initialize it before the first commit:

```bash
git init
git branch -M main
```

