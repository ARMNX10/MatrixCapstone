from typing import Dict, Any, Literal, List, TypedDict
from intent_analyzer import IntentAnalysisResult
from loguru import logger

class DecisionPathResult(TypedDict):
    path: Literal["ai", "web_search"]
    confidence: float
    reasoning: str

def determine_path(analysis: IntentAnalysisResult) -> DecisionPathResult:
    """
    Determine which processing path to take based on intent analysis
    
    Args:
        analysis: The intent analysis result
        
    Returns:
        DecisionPathResult: The decision on which path to take
    """
    # Initialize confidence and reasoning
    confidence = 0.0
    reasoning = ""
    
    # Decision logic
    if analysis["requires_web_search"]:
        path = "web_search"
        confidence = analysis["confidence"]
        reasoning = f"Query requires factual information about {', '.join(analysis['topics'])}. Web search is more appropriate."
    elif analysis["is_complex_query"]:
        path = "ai"
        confidence = analysis["confidence"]
        reasoning = f"Query is complex and requires reasoning about {', '.join(analysis['topics'])}. AI processing is more appropriate."
    else:
        # Default path based on confidence
        if analysis["confidence"] > 0.7:
            path = "ai"
            confidence = analysis["confidence"]
            reasoning = "Query is best handled by AI based on high confidence in intent analysis."
        else:
            path = "web_search"
            confidence = 1.0 - analysis["confidence"]
            reasoning = "Low confidence in intent analysis. Defaulting to web search for better results."
    
    return DecisionPathResult(
        path=path,
        confidence=confidence,
        reasoning=reasoning
    )

# Function to be used in the LangGraph node
def decision_path_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node for determining the processing path
    
    Args:
        state: The current state dictionary
        
    Returns:
        Updated state with decision path
    """
    logger.info("[DECISION ROUTER] Starting decision routing")
    
    # Get intent analysis from state
    analysis = state.get("intent_analysis", {})
    logger.info(f"[DECISION ROUTER] Processing intent: {analysis.get('intent', 'unknown')}")
    
    # Determine path
    decision = determine_path(analysis)
    logger.info(f"[DECISION ROUTER] Decision made: Path={decision['path']}, Confidence={decision['confidence']}")
    logger.info(f"[DECISION ROUTER] Reasoning: {decision['reasoning']}")
    
    # Update state with decision
    state["decision_result"] = decision
    
    logger.info("[DECISION ROUTER] Completed decision routing")
    return state

def route_based_on_decision(state: Dict[str, Any]) -> Literal["ai", "web_search"]:
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
