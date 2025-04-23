from typing import Dict
from web_search_api import call_serper_api

def fetch_web_search_results_node(state: Dict) -> Dict:
    """
    LangGraph node to fetch web search results using Serper API.
    Populates state['web_search_results'] with formatted results.
    """
    last_message = state["messages"][-1]
    query = last_message.get("content", "")
    results = call_serper_api(query)
    state["web_search_results"] = results
    state["web_search_done"] = True
    return state
