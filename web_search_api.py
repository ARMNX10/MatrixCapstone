import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_API_URL = "https://google.serper.dev/search"

def call_serper_api(query: str) -> str:
    """Call the Serper API and return formatted search results as a string."""
    if not SERPER_API_KEY:
        return "[Web Search Error] SERPER_API_KEY not set."
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"q": query}
    try:
        resp = requests.post(SERPER_API_URL, headers=headers, json=data, timeout=10)
        resp.raise_for_status()
        results = resp.json()
        # Format the top results for synthesis
        formatted = []
        for i, item in enumerate(results.get("organic", [])[:3], 1):
            title = item.get("title", "")
            link = item.get("link", "")
            snippet = item.get("snippet", "")
            formatted.append(f"[Source {i}] {title}\nURL: {link}\n{snippet}")
        return "\n\n".join(formatted) if formatted else "[Web Search] No results found."
    except Exception as e:
        return f"[Web Search Error] {str(e)}"
