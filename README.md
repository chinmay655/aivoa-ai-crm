# AIVOA AI-First CRM — HCP Interaction Module

A full-stack AI-first CRM application for logging and managing Healthcare Professional (HCP) interactions.

Users can log interactions through:

- A structured React form
- A conversational AI assistant

Both interfaces use the same FastAPI backend and PostgreSQL database.

## Technology Stack

### Frontend

- React
- TypeScript
- Vite
- Redux Toolkit
- Google Inter

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

### AI

- LangGraph
- Groq
- `llama-3.3-70b-versatile`

### Database

- PostgreSQL
- Psycopg

## Features

- Search HCP records
- Log HCP interactions
- Edit existing interactions
- Record product samples
- Schedule follow-ups
- View interaction history
- Structured interaction form
- Conversational AI assistant
- PostgreSQL data persistence
- Seeded HCP demonstration records

## Architecture

```text
React + Redux Toolkit
        |
        | REST API
        v
FastAPI + SQLAlchemy
        |
        +--------------------+
        |                    |
        v                    v
PostgreSQL            LangGraph Agent
                            |
                            v
                     Groq LLM

The structured form and AI assistant use the same backend services and PostgreSQL database.

## LangGraph Tools

The application implements six sales-related tools.

### `search_hcp`

Searches HCP records by name, specialty, organization, or location.

```text
Find Dr. Sarah Mitchell.
```

### `log_interaction`

Creates and stores a new HCP interaction.

```text
Log an in-person interaction with HCP ID 1.
We discussed CardioPlus benefits.
Dr. Mitchell requested additional safety data.
The sentiment was positive.

### `edit_interaction`

Updates an existing interaction.

```text
Edit interaction ID 1 and change the sentiment to neutral.

### `add_product_sample`

Records product samples associated with an interaction.

```text
Add 2 samples of CardioPlus 10 mg to interaction ID 1.

### `schedule_follow_up`

Creates a follow-up activity.

```text
Schedule a follow-up for HCP ID 1 on July 21, 2026 at 10:00 AM.
```

### `get_interaction_history`

Retrieves previous interactions for an HCP.

```text
Show the interaction history for HCP ID 1.
```

## Project Structure

```text
aivoa-ai-crm/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   └── types/
│   ├── .env.example
│   └── package.json
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── DEMO_SCRIPT.md
│
├── .gitignore
└── README.md
```

## Prerequisites

Install:

- Python 3.11 or newer
- Node.js 20 or newer
- PostgreSQL
- Git
- A Groq API key

## PostgreSQL Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE aivoa_crm;
```

Default example configuration:

```text
Database: aivoa_crm
User: postgres
Host: 127.0.0.1
Port: 5432
```

## Backend Setup

Open a terminal:

```powershell
cd backend
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_POSTGRES_PASSWORD@127.0.0.1:5432/aivoa_crm
GROQ_API_KEY=YOUR_PRIVATE_GROQ_API_KEY
GROQ_MODEL=llama-3.3-70b-versatile
CORS_ORIGINS=http://localhost:5173
```

Start the backend:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://localhost:8000/health
http://localhost:8000/docs
```

## Frontend Setup

Open a second terminal:

```powershell
cd frontend
npm install
```

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

Start the frontend:

```powershell
npm run dev
```

Open:

```text
http://localhost:5173
```

## Demo HCP Records

The backend automatically seeds demonstration records including:

- Dr. Sarah Mitchell — Cardiology
- Dr. Michael Chen — Endocrinology
- Dr. Priya Patel — Oncology
- Dr. James Wilson — Internal Medicine
- Dr. Emily Rodriguez — Neurology

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Backend health check |
| `GET` | `/api/hcps?q=` | Search HCP records |
| `GET` | `/api/interactions` | List interactions |
| `POST` | `/api/interactions` | Create an interaction |
| `PATCH` | `/api/interactions/{id}` | Edit an interaction |
| `POST` | `/api/agent/chat` | Run the LangGraph assistant |
| `GET` | `/api/agent/tools` | List available tools |

## Testing

Backend:

```powershell
cd backend
python -m pytest
```

Frontend:

```powershell
cd frontend
npm run build
```

## Model Configuration

The assignment referenced `gemma2-9b-it` and also mentioned `llama-3.3-70b-versatile`.

This implementation uses:

```env
GROQ_MODEL=llama-3.3-70b-versatile
```

The model is configurable through the environment file without changing the source code.

## Security

Do not commit:

```text
.env
backend/.env
frontend/.env
```

The application uses demonstration data and should not be used for storing real patient or sensitive healthcare information.

## Known Limitations

- Authentication is not implemented.
- Role-based access control is not implemented.
- Production audit logging is not implemented.
- A valid Groq API key and internet connection are required for AI features.
- The application is intended for demonstration and technical evaluation.

## Documentation

- `docs/ARCHITECTURE.md` — system architecture and LangGraph flow
- `docs/DEMO_SCRIPT.md` — video demonstration outline

## Author

**Chinmay Ravindra Ghogale**

Full Stack Developer — AI Applications Assignment
