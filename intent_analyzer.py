import os
from typing import Dict, List, Any, TypedDict
from model_config import get_groq_client, get_model_config
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()


class IntentAnalysisResult(TypedDict):
    intent: str
    confidence: float
    requires_web_search: bool
    is_complex_query: bool
    entities: List[str]
    topics: List[str]
    ai_inference: str
    ai_reasoning: str

def analyze_intent(query: str) -> IntentAnalysisResult:
    """
    Analyze the intent of a user query to determine if it requires web search or AI processing.
    Args:
        query: The user's query string
    Returns:
        IntentAnalysisResult: Analysis of the query intent
    """
    config = get_model_config()
    client = get_groq_client()
    system_prompt = (
        "You are an intent analysis system. Your job is to analyze the user's query and determine: "
        "1. The primary intent of the query\n"
        "2. Whether the query requires web search (factual, current events, specific information)\n"
        "3. Whether the query is complex (multiple aspects, requires reasoning, hypothetical scenarios)\n"
        "4. Key entities mentioned in the query\n"
        "5. Main topics of the query\n"
        "6. Provide an 'ai_inference' field: a brief, clear summary of what the user is asking or wants to achieve.\n"
        "7. Provide an 'ai_reasoning' field: a concise explanation of your reasoning about the user's intent and how you arrived at your inference.\n"
        "\nFormat your response as a valid JSON object with the following structure:\n"
        "{\n"
        "  \"intent\": \"string - brief description of primary intent\",\n"
        "  \"confidence\": float between 0 and 1,\n"
        "  \"requires_web_search\": boolean,\n"
        "  \"is_complex_query\": boolean,\n"
        "  \"entities\": [\"list\", \"of\", \"entities\"],\n"
        "  \"topics\": [\"list\", \"of\", \"topics\"],\n"
        "  \"ai_inference\": \"string - brief summary of user intent\",\n"
        "  \"ai_reasoning\": \"string - your reasoning for the inference\"\n"
        "}\n"
        "\nGuidelines:\n- Direct factual questions typically require web search\n"
        "- Questions about current events require web search\n"
        "- Complex reasoning questions typically don't require web search\n"
        "- Creative or hypothetical questions don't require web search\n"
        "- Personal advice questions don't require web search\n"
        "- Code-related questions don't require web search unless asking about specific libraries or documentation\n"
    )
    prompt = f"{system_prompt}\n\nAnalyze this query: {query}"
    completion = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=config["temperature"],
        top_p=config["top_p"],
        max_completion_tokens=config["max_completion_tokens"],
        stream=config["stream"],
        stop=config["stop"]
    )
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""
    import json
    try:
        analysis = json.loads(response_text)
        return IntentAnalysisResult(
            intent=analysis.get("intent", "unknown"),
            confidence=analysis.get("confidence", 0.0),
            requires_web_search=analysis.get("requires_web_search", False),
            is_complex_query=analysis.get("is_complex_query", False),
            entities=analysis.get("entities", []),
            topics=analysis.get("topics", []),
            ai_inference=analysis.get("ai_inference", analysis.get("intent", "")),
            ai_reasoning=analysis.get("ai_reasoning", "No reasoning provided.")
        )
    except json.JSONDecodeError:
        pass
    return IntentAnalysisResult(
        intent="unknown",
        confidence=0.0,
        requires_web_search=False,
        is_complex_query=False,
        entities=[],
        topics=[],
        ai_inference="",
        ai_reasoning=""
    )


# Function to be used in the LangGraph node
def intent_analyzer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node for analyzing user intent
    
    Args:
        state: The current state dictionary
        
    Returns:
        Updated state with intent analysis
    """
    logger.info("[INTENT ANALYZER] Starting intent analysis")
    query = state.get("messages", [""])[0]
    logger.info(f"[INTENT ANALYZER] Processing query: {query}")
    
    analysis = analyze_intent(query)
    
    # Log the analysis results
    logger.info(f"[INTENT ANALYZER] Analysis results: Intent={analysis['intent']}, Confidence={analysis['confidence']}, Requires Web Search={analysis['requires_web_search']}")
    logger.debug(f"[INTENT ANALYZER] Full analysis: {analysis}")
    
    # Update state with analysis
    state["intent_analysis"] = analysis
    
    logger.info("[INTENT ANALYZER] Completed intent analysis")
    return state
