# AI Operations Agent for Small Businesses

Production-ready SaaS foundation for automating customer communication, lead management, follow-ups, payment reminders, appointment scheduling, and daily summaries with AI agents.

This repository is being built in staged milestones. The current implementation covers **Stage 6: CRM Module**.

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
- PostgreSQL: localhost:5433
- Redis: localhost:6380

## Run Locally

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
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

## Authentication Endpoints

- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

## CRM Endpoints

- `GET /api/v1/customers`
- `POST /api/v1/customers`
- `GET /api/v1/customers/{customer_id}`
- `PUT /api/v1/customers/{customer_id}`
- `DELETE /api/v1/customers/{customer_id}`
- `GET /api/v1/leads`
- `POST /api/v1/leads`
- `GET /api/v1/leads/{lead_id}`
- `PUT /api/v1/leads/{lead_id}`
- `DELETE /api/v1/leads/{lead_id}`

## Seed Data

After migrations are applied, load sample business data:

```bash
cd backend
python scripts/seed.py
```

With Docker:

```bash
docker compose exec backend python scripts/seed.py
```

Sample login after seeding:

- Email: `owner@example.com`
- Password: `password123`

## Git Setup

If this folder is not already a Git repository, initialize it before the first commit:

```bash
git init
git branch -M main
```
