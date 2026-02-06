from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TrulyMadly High-Trust Assistant API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    query: str
    plan: List[Dict[str, Any]]
    results: List[Dict[str, Any]]
    verified_output: str
    status: str
    history: Optional[List[Dict[str, str]]] = []

@app.get("/")
async def root():
    return {"message": "AssistOps: AI Operations Assistant API is running"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        query = request.query
        history = request.history or []
        
        # 1. Planning Phase
        planner = PlannerAgent()
        plan = planner.create_plan(query, history)
        
        if not plan:
            results = []
            verifier = VerifierAgent()
            verified_output = verifier.verify_and_finalize(query, results)
            return ChatResponse(
                query=query,
                plan=[],
                results=[],
                verified_output=verified_output,
                status="no_plan",
                history=history
            )

        # 2. Execution Phase
        executor = ExecutorAgent()
        results = executor.execute(plan)

        # 3. Verification Phase
        verifier = VerifierAgent()
        verified_output = verifier.verify_and_finalize(query, results, history)

        return ChatResponse(
            query=query,
            plan=plan,
            results=results,
            verified_output=verified_output,
            status="success",
            history=history
        )
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
