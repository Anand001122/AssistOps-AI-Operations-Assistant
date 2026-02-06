import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self, model_name="google/gemini-2.0-flash-001"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model_name = model_name

    def generate_response(self, prompt: str, json_mode: bool = False) -> str:
        """
        Generates a response from Gemini via OpenRouter.
        If json_mode is True, it attempts to return valid JSON.
        """
        try:
            response_format = None
            if json_mode:
                response_format = {"type": "json_object"}
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                response_format=response_format
            )
            
            if not response or not response.choices:
                return "[]" if json_mode else "I'm sorry, I couldn't generate a safe response for that request."
                
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenRouter API Error: {e}")
            return "[]" if json_mode else f"Error generating response: {str(e)}"

# Singleton-like access
client = None

def get_gemini_client():
    global client
    if client is None:
        client = GeminiClient()
    return client
