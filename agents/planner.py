import json
from llm.gemini_client import get_gemini_client

class PlannerAgent:
    def __init__(self):
        self.client = get_gemini_client()

    def create_plan(self, user_prompt: str, history: list = []) -> list:
        """
        Converts a natural language request into a sequence of tool calls.
        Uses chat history to resolve context (e.g. follow-up answers).
        """
        history_str = ""
        if history:
            history_str = "\nConversation History:\n" + "\n".join([f"{m['role']}: {m['content']}" for m in history])

        system_prompt = f"""
        You are the AssistOps Planner Agent. Your goal is to map user queries to precise tool calls.

        STRICT NO-PLACEHOLDER POLICY:
        - NEVER use placeholders like "{{repo_name}}", "user_repo_owner", or any string in curly braces as a tool argument.
        - NEVER assume a repo name unless it is explicitly typed by the user in the query.
        - If the user asks about "their repos", "my projects", or "the skills of [User]", you MUST use `list_user_repositories(username="[User]")` first.
        - FORBIDDEN: `get_repo_details(owner="user_repo_owner", repo="user_repo_name")` is an immediate failure.

        CONTEXT AWARENESS:
        Use the conversation history to resolve pronouns or missing details.
        {history_str}

        Available Tools:
        1. get_weather(city: str): Returns weather advice.
        2. search_repositories(query: str): Keyword-based search.
        3. get_repo_details(owner: str, repo: str): Detailed metrics (stars, forks, parent repo).
        4. list_user_repositories(username: str): Best for listing a specific profile's work and identifying their skills/tech-stack.

        Output Format (STRICT JSON ARRAY):
        [
            {{"tool": "tool_name", "args": {{"arg1": "value1"}}, "reason": "Reason"}}
        ]
        """
        
        full_prompt = f"{system_prompt}\n\nCurrent User Request: {user_prompt}\n\nPlan (JSON Array):"
        
        response_text = self.client.generate_response(full_prompt, json_mode=True)
        
        # Clean response if markdown blocks are present
        if "```" in response_text:
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:].strip()
            response_text = response_text.strip()

        try:
            plan = json.loads(response_text)
            if not isinstance(plan, list):
                print(f"Warning: Planner returned {type(plan)}, expected list. Wrapping in list.")
                plan = [plan]
            return plan
        except Exception as e:
            print(f"Planner failed to parse JSON: {e}")
            print(f"Raw Response: {response_text}")
            return []
