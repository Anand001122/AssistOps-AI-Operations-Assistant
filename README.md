# AssistOps: AI Operations Assistant

AssistOps is a high-trust, multi-agent AI system designed for advanced operations tasks. It leverages LLM reasoning to plan, execute, and verify tasks involving real-time weather and GitHub data.

## 🚀 Vision
AssistOps prioritizes **Integrity** and **Human-Centric Interaction**:
- **Planner Agent**: A rigorous logic engine that converts natural language into precise tool sequences without guessing.
- **Verifier Agent**: An integrity guardian that validates raw data and translates it into empathetic, actionable advice.

## ✨ Core Capabilities
- **Intelligent Planning**: Multi-turn conversation awareness to resolve pronouns and follow-up intents.
- **GitHub Intelligence**: 
  - **Skill Identification**: Extracts technical expertise (React, Python, etc.) from user repositories.
  - **Fork Tracking**: Identifies original repository parents for forked projects.
  - **Profile Listing**: Directly lists repositories for any GitHub username.
- **Weather-Based Advice**: Provides genuine, weather-driven activity recommendations (e.g., suggesting indoor activities during rain).
- **Premium UI**: A glassmorphism dashboard with real-time progress tracking and picturized weather cards.

## 🛠️ Mandatory Architecture
- **Planner**: `agents/planner.py` (JSON-constrained reasoning).
- **Executor**: `agents/executor.py` (Secure API tool-calling).
- **Verifier**: `agents/verifier.py` (High-trust output verification).
- **LLM Layer**: `llm/gemini_client.py` (Powered by Gemini 2.0 Flash).

## 📂 Project Structure
```text
ai_ops_assistant/
├── agents/          # Multi-Agent Logic (Planner, Executor, Verifier)
├── tools/           # API Integrations (Weather, GitHub)
├── llm/             # LLM Client (Gemini 2.0 via OpenRouter)
├── frontend/        # React/Vite Glassmorphism Dashboard
├── main.py          # CLI Interface
├── server.py        # FastAPI Backend
├── requirements.txt # Python Dependencies
├── .env.example     # Environment template
└── README.md        # This document
```

## 🚀 Setup & Execution
1. **Keys**: Populate `.env` with `GITHUB_TOKEN`, `OPENWEATHERMAP_API_KEY`, and `GEMINI_API_KEY`.
2. **Single-Command Start**: Run the following in your terminal to start both backend and frontend:
   ```bash
   python run.py
   ```
   *Note: If port 5173 is already in use, the frontend will automatically start on 5174, 5175, etc. Check the terminal output for the exact URL.*

3. **Manual Start (Alternative)**:
   - **Backend**: `python server.py` (Port 8000)
   - **Frontend**: `cd frontend && npm run dev` (Port 5173+)
4. **CLI**: Run `python main.py "Your Task Here"` for a direct terminal response.

---
*Elevating operations through high-trust AI logic.*
