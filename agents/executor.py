from tools.weather import get_weather
from tools.github import search_repositories, get_repo_details, list_user_repositories

class ExecutorAgent:
    def __init__(self):
        self.tool_map = {
            "get_weather": get_weather,
            "search_repositories": search_repositories,
            "get_repo_details": get_repo_details,
            "list_user_repositories": list_user_repositories
        }

    def execute(self, plan: list) -> list:
        """
        Executes the steps in the plan and collects results.
        """
        results = []
        for step in plan:
            tool_name = step.get("tool")
            args = step.get("args", {})
            reason = step.get("reason", "Executing step")
            
            print(f"[Executor] Running {tool_name} for: {reason}")
            
            if tool_name in self.tool_map:
                try:
                    tool_func = self.tool_map[tool_name]
                    output = tool_func(**args)
                    # If tool returns a status, use it; otherwise default to success
                    status = "success"
                    if isinstance(output, dict) and output.get("status") == "failed":
                        status = "failed"
                        
                    results.append({
                        "step": step,
                        "output": output,
                        "status": status
                    })
                except Exception as e:
                    results.append({
                        "step": step,
                        "error": str(e),
                        "status": "failed"
                    })
            else:
                results.append({
                    "step": step,
                    "error": f"Tool '{tool_name}' not found.",
                    "status": "failed"
                })
        
        return results
