import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str) -> dict:
    """
    Fetches current weather for a given city using OpenWeatherMap.
    Returns a dictionary with weather details or an error message.
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return {"error": "OPENWEATHERMAP_API_KEY not set."}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        return {
            "city": data.get("name"),
            "temperature": data["main"].get("temp"),
            "description": data["weather"][0].get("description"),
            "humidity": data["main"].get("humidity"),
            "wind_speed": data["wind"].get("speed"),
            "status": "success"
        }
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "City not found", "status": "failed"}
        return {"error": f"Weather service error: {str(e)}", "status": "failed"}
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}", "status": "failed"}
