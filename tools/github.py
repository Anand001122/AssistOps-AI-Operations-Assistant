import os
import requests
from dotenv import load_dotenv

load_dotenv()

def search_repositories(query: str, limit: int = 5) -> dict:
    """
    Searches for GitHub repositories based on a query.
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.mercy-preview+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"https://api.github.com/search/repositories?q={query}&per_page={limit}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        items = response.json().get("items", [])
        
        repos = []
        for item in items:
            repos.append({
                "name": item.get("full_name"),
                "description": item.get("description"),
                "stars": item.get("stargazers_count"),
                "url": item.get("html_url"),
                "is_fork": item.get("fork"),
                "topics": item.get("topics", [])
            })
        
        return {"repositories": repos, "status": "success"}
    except Exception as e:
        return {"error": f"GitHub search failed: {str(e)}", "status": "failed"}

def get_repo_details(owner: str, repo: str) -> dict:
    """
    Fetches details for a specific GitHub repository, including fork parent info.
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        result = {
            "name": data.get("full_name"),
            "description": data.get("description"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "is_fork": data.get("fork"),
            "topics": data.get("topics", []),
            "status": "success"
        }
        
        if data.get("fork") and "parent" in data:
            result["parent"] = {
                "full_name": data["parent"].get("full_name"),
                "owner": data["parent"].get("owner", {}).get("login"),
                "url": data["parent"].get("html_url")
            }
            
        return result
    except Exception as e:
        return {"error": f"Failed to fetch repo details: {str(e)}", "status": "failed"}

def list_user_repositories(username: str, limit: int = 10) -> dict:
    """
    Lists repositories for a specific GitHub user with skill topics.
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.mercy-preview+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"https://api.github.com/users/{username}/repos?per_page={limit}&sort=updated"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        items = response.json()
        
        repos = []
        for item in items:
            repos.append({
                "name": item.get("full_name"),
                "description": item.get("description"),
                "stars": item.get("stargazers_count"),
                "url": item.get("html_url"),
                "is_fork": item.get("fork"),
                "topics": item.get("topics", [])
            })
        
        return {"repositories": repos, "status": "success"}
    except Exception as e:
        return {"error": f"Failed to list user repositories: {str(e)}", "status": "failed"}
