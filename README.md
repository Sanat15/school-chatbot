# School Assistant Chatbot

A full-stack AI-powered school assistant that lets students and parents query their timetable, assignments, and marks using natural language — including in Hindi.

**Live app:** [https://school-chatbot-puce.vercel.app](https://school-chatbot-puce.vercel.app)

---

## Features

- **Natural language queries** — Ask "What are my marks?" or "क्या कोई assignment है?" and get a friendly answer
- **Role-based access** — Students see their own data; parents see their linked child's data
- **JWT authentication** — Secure login with token-based sessions
- **Multilingual** — Detects Hindi vs English and responds in the same language
- **Fast** — Singleton LLM client, NullPool DB connections optimised for serverless

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Vite |
| Backend | FastAPI (Python) |
| Database | PostgreSQL (Neon) |
| AI | Groq API — Llama 3.3 70B |
| Auth | JWT (python-jose) + bcrypt |
| Hosting | Vercel (serverless) |

## Project Structure

```
school-chatbot/
├── api/
│   └── index.py          # Vercel entry point
├── backend/
│   ├── main.py           # FastAPI app, CORS, static SPA serving
│   ├── core/
│   │   ├── auth.py       # JWT token logic
│   │   ├── database.py   # SQLAlchemy engine (NullPool on Vercel)
│   │   ├── nl_to_sql.py  # NL → SQL → friendly response pipeline
│   │   ├── language.py   # Hindi/English detection
│   │   └── llm.py        # Groq client singleton
│   ├── models/
│   │   └── models.py     # SQLAlchemy ORM models
│   ├── routes/
│   │   ├── auth.py       # POST /api/login
│   │   ├── chat.py       # POST /api/chat/query
│   │   ├── timetable.py  # GET  /api/timetable
│   │   ├── assignments.py# GET  /api/assignments
│   │   └── marks.py      # GET  /api/marks
│   ├── init_db.py        # Creates all tables
│   └── seed.py           # Seeds demo data
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── pages/        # Login, Chat, Timetable, Marks, Assignments
├── requirements.txt
└── vercel.json
```

## Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Student | `ravi` | `ravi123` |
| Student | `priya` | `priya123` |
| Student | `arjun` | `arjun123` |
| Parent | `suresh` | `suresh123` |
| Parent | `meena` | `meena123` |

## Running Locally

**Prerequisites:** Python 3.11+, Node.js 18+, a PostgreSQL database (e.g. [Neon](https://neon.tech))

```bash
# 1. Clone
git clone https://github.com/Sanat15/school-chatbot.git
cd school-chatbot

# 2. Backend setup
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 3. Environment variables — create a .env file:
#    DATABASE_URL=postgresql://...
#    GROQ_API_KEY=gsk_...
#    SECRET_KEY=some-random-secret

# 4. Initialise and seed the database
python -m backend.init_db
python -m backend.seed

# 5. Start the backend
uvicorn backend.main:app --reload

# 6. Start the frontend (new terminal)
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`, backend at `http://localhost:8000`.

## Deployment (Vercel)

The app deploys as a single Vercel serverless function:

1. **Build** — copies `backend/` into `api/backend/` and `frontend/dist` into `api/static/`
2. **Runtime** — every request hits `api/index.py`, which loads the FastAPI app
3. **Routing** — API routes (`/api/*`) are handled by FastAPI; all other paths serve the React SPA

Required environment variables in Vercel:
- `DATABASE_URL`
- `GROQ_API_KEY`
- `SECRET_KEY`
- `FRONTEND_URL` (optional, e.g. `https://school-chatbot-puce.vercel.app`)

## Example Queries

- "What's my timetable on Monday?"
- "Show me my latest marks"
- "Do I have any assignments due this week?"
- "मेरे क्या marks हैं?" *(Hindi)*
- "कोई assignment है क्या?"
