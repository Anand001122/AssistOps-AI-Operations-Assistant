# AssistOps: AI Operations Assistant

AssistOps is a high-trust, multi-agent AI system designed for advanced operations tasks. It leverages LLM reasoning to plan, execute, and verify tasks involving real-time weather and GitHub data.

## 🏗️ Architecture Explanation

AssistOps uses a **Multi-Agent Orchestration** pattern to ensure results are accurate, verified, and human-friendly.

1.  **Planner Agent (`agents/planner.py`)**: The "Brain". It parses natural language into a structured JSON execution plan. It follows a **Strict Zero-Assumption Policy**, meaning it will never guess missing data (like locations) and instead asks for clarification.
2.  **Executor Agent (`agents/executor.py`)**: The "Worker". It carries out the plan by calling the permitted tools in sequence. It handles the raw data fetching from external APIs.
3.  **Verifier Agent (`agents/verifier.py`)**: The "Guardian". It reviews the raw data from the Executor, validates it against the user's original intent, and translates technical logs into empathetic, actionable advice.
4.  **Tools (`tools/`)**: Modular Python functions that interface with third-party APIs.

## 🔌 Integrated APIs
- **OpenWeatherMap API**: Provides real-time weather data for activity planning.
- **GitHub API**: Used for repository search, user profile listing, skill identification (topics), and fork tracking.
- **Gemini 2.0 Flash**: The core LLM powering the agents' reasoning and linguistics.

## ⚙️ Setup Instructions (Localhost)

Follow these steps to run the complete system on your local machine:

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & npm
- A **GitHub Personal Access Token** (Classic or Fine-grained)
- An **OpenWeatherMap API Key** (Free tier)
- A **Gemini API Key** (via Google AI Studio or OpenRouter)

### 2. Environment Configuration
Create a `.env` file in the root directory and populate it based on `.env.example`:
```env
# Gemini API Key
GEMINI_API_KEY=your_key_here

# OpenWeatherMap API Key
OPENWEATHERMAP_API_KEY=your_key_here

# GitHub Token
GITHUB_TOKEN=your_token_here
```

### 3. Installation
**Backend**:
```bash
pip install -r requirements.txt
```
**Frontend**:
```bash
cd frontend
npm install
cd ..
```

### 4. Running the Project
**Option A: Single-Command Startup (Recommended)**
Run both services concurrently with one command:
```bash
python assistops.py
```
*Note: The backend starts on port 8000. The frontend starts on port 5173 (or 5174+ if 5173 is occupied).*

**Option B: Manual Startup**
- Terminal 1 (Backend): `python server.py`
- Terminal 2 (Frontend): `cd frontend && npm run dev`

---

## 🧪 Example Prompts & Testing

You can test these prompts in the **Web Dashboard** (Browser) or the **CLI** (Terminal).

### 1. Web Dashboard Testing
Navigate to `http://localhost:5173` and type:
1.  **Contextual Planning**: *"I'm planning a coding meetup in Delhi. Check the weather and find a repository with 'FastAPI' examples to show the group."*
2.  **Skill Discovery**: *"List repositories for Anand001122 and tell me about his skills."*
3.  **Stateful Clarification**: *"Should I take an umbrella?"* (Wait for it to ask for the city, then reply *"Bhopal"*).

### 2. Local Terminal Testing
Run these commands from the project root:
1.  **Weather Insight**: `python main.py "Is it a good night for an outdoor walk in Mumbai?"`
2.  **Fork Intelligence**: `python main.py "Who did I fork my latest repository from?"`
3.  **Project Metrics**: `python main.py "Tell me about the stars and description of the 'facebook/react' repo."`

---

## ⚠️ Known Limitations & Tradeoffs
- **API Activation**: New OpenWeatherMap keys can take up to 2 hours to activate.
- **Rate Limits**: The Gemini Free Tier has a request-per-minute limit. If you see a 429 error, wait 60 seconds.
- **Public Data Only**: The GitHub tool intentionally fetches only public repository data unless a token with private repo scope is provided.
- **Vite Port Drift**: In some local environments, Vite may jump to port 5174 if 5173 hasn't fully closed from a previous session. Always check the terminal for the active `Local URL`.

---
*Elevating operations through high-trust AI logic.*
