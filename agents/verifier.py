import json
from llm.gemini_client import get_gemini_client

class VerifierAgent:
    def __init__(self):
        self.client = get_gemini_client()

    def verify_and_finalize(self, user_prompt: str, execution_results: list, history: list = []) -> str:
        """
        The "Integrity Guardian": Validates results against the user's intent.
        Uses history to understand the full context of the request.
        """
        history_str = ""
        if history:
            history_str = "\nConversation History:\n" + "\n".join([f"{m['role']}: {m['content']}" for m in history])

        system_prompt = f"""
        You are the AssistOps Verifier Agent. You talk to the user like a friendly, expert colleague, NOT a robot.
        
        {history_str}

        STRICT FORMATTING RULES:
        1. NO BULLET POINTS: Do not use '*' or '-' for lists.
        2. NUMBERED LISTS: If listing multiple items (like repositories or skills), ALWAYS use numbering (1., 2., 3.).
        3. CLEAN HIGHLIGHTING: Highlight project names or key terms using **Bold** only. No trailing colons after bolded names if a description follows on the same line.
           - Example: 1. **ClubHub** is a great management platform.
        4. NO ROBOTIC META-TALK: Never say "I have reviewed results", "Execution logs", or "Verified Answer".
        5. NATURAL FLOW: Start directly with the core answer. 
        6. SKILL IDENTIFICATION: Analyze `topics` and `descriptions` to summarize the user's skills.
        7. FORK NARRATIVE: If `is_fork` is true, explain the origin using `parent` data naturally.
        8. ACTIONABLE CONCLUSION: Always end with a helpful recommendation or insight.
        9. HANDLING ERRORS: Use friendly clarification requests instead of technical error codes.
        """
        
        context = f"Current Query: {user_prompt}\n\nExecution Results: {json.dumps(execution_results, indent=2)}"
        full_prompt = f"{system_prompt}\n\n{context}\n\nFinal Verified Answer (Direct and Actionable):"
        
        return self.client.generate_response(full_prompt)
