import os

from groq import Groq
import os

def get_model_config():
    """
    Returns the centralized configuration for the GROQ model.
    """
    return {
        "api_key": os.getenv("GROQ_API_KEY"),
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",  
        "temperature": 1.0,
        "top_p": 1.0,
        "max_completion_tokens": 1024,
        "stream": True,
        "stop": None
    }

def get_groq_client():
    """
    Returns an authenticated Groq client instance.
    """
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

