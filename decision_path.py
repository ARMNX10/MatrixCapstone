from typing import Dict, Any, Literal, List, TypedDict
from intent_analyzer import IntentAnalysisResult
from loguru import logger
import re

class DecisionPathResult(TypedDict):
    path: Literal["ai_processing", "web_search", "calculator"]
    confidence: float
    reasoning: str

def determine_path(analysis: dict) -> dict:
    """
    Determine which processing path to take based on intent analysis.
    Robust to missing or malformed keys.
    """
    # Use .get() with defaults for all keys
    requires_web_search = analysis.get("requires_web_search", False)
    is_complex_query = analysis.get("is_complex_query", False)
    confidence = analysis.get("confidence", 0.0)
    topics = analysis.get("topics", [])
    intent = analysis.get("intent", "unknown")
    reasoning = ""

    # Defensive: if analysis is empty or missing keys, fallback to AI
    if not isinstance(requires_web_search, bool):
        requires_web_search = False
    if not isinstance(is_complex_query, bool):
        is_complex_query = False
    if not isinstance(confidence, (float, int)):
        confidence = 0.0
    if not isinstance(topics, list):
        topics = []

    if requires_web_search:
        path = "web_search"
        reasoning = f"Query requires factual information about {', '.join(topics)}. Web search is more appropriate."
    elif is_complex_query:
        path = "ai_processing"
        reasoning = f"Query is complex and requires reasoning about {', '.join(topics)}. AI processing is more appropriate."
    else:
        # Default path based on confidence
        if confidence > 0.7:
            path = "ai_processing"
            reasoning = "Query is best handled by AI based on high confidence in intent analysis."
        else:
            path = "web_search"
            confidence = 1.0 - confidence
            reasoning = "Low confidence in intent analysis. Defaulting to web search for better results."

    # Normalize any 'ai' path to 'ai_processing' for workflow compatibility
    if path == "ai":
        path = "ai_processing"
    return {
        "path": path,
        "confidence": confidence,
        "reasoning": reasoning
    }

# Function to be used in the LangGraph node
import json

def decision_path_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node for determining the processing path
    
    Args:
        state: The current state dictionary
        
    Returns:
        Updated state with decision path
    """
    logger.info("[DECISION ROUTER] Starting decision routing")
    
    # Check for calculator expression
    query = state.get("messages", [{}])[-1].get("content", "")
    if re.fullmatch(r'[\d\.\s\+\-\*\/\(\)]+', query):
        decision = {"path": "calculator", "confidence": 1.0, "reasoning": "Detected calculation expression."}
        state["decision_result"] = decision
        logger.info("[DECISION ROUTER] Detected calculator expression. Routing to calculator.")
        logger.info("[DECISION ROUTER] Completed decision routing")
        return state

    # Get intent analysis from state (parse JSON string if needed)
    analysis = state.get("intent_analysis", {})
    if isinstance(analysis, str):
        try:
            analysis = json.loads(analysis)
        except Exception:
            logger.error("[DECISION ROUTER] Could not parse intent_analysis JSON string.")
            analysis = {}
    logger.info(f"[DECISION ROUTER] Processing intent: {analysis.get('intent', 'unknown')}")
    
    # Determine path
    decision = determine_path(analysis)
    logger.info(f"[DECISION ROUTER] Decision made: Path={decision['path']}, Confidence={decision['confidence']}")
    logger.info(f"[DECISION ROUTER] Reasoning: {decision['reasoning']}")
    
    # Normalize any 'ai' path to 'ai_processing' for workflow compatibility
    if decision["path"] == "ai":
        decision["path"] = "ai_processing"
    # Update state with decision
    state["decision_result"] = decision
    
    logger.info("[DECISION ROUTER] Completed decision routing")
    return state

def route_based_on_decision(state: Dict[str, Any]) -> Literal["ai", "web_search", "calculator"]:
    """
    Router function for LangGraph to determine which node to execute next
    
    Args:
        state: The current state dictionary
        
    Returns:
        String indicating which node to execute next
    """
    logger.info("[ROUTER] Determining next node to execute")
    decision = state.get("decision_result", {})
    path = decision.get("path", "ai")  # Default to AI if no decision
    
    logger.info(f"[ROUTER] Routing to: {path}")
    return path
