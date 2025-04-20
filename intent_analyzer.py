import os
from typing import Dict, List, Any, TypedDict
import google.generativeai as genai
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

class IntentAnalysisResult(TypedDict):
    intent: str
    confidence: float
    requires_web_search: bool
    is_complex_query: bool
    entities: List[str]
    topics: List[str]

def analyze_intent(query: str) -> IntentAnalysisResult:
    """
    Analyze the intent of a user query to determine if it requires web search or AI processing.
    
    Args:
        query: The user's query string
        
    Returns:
        IntentAnalysisResult: Analysis of the query intent
    """
    # Configure the model
    generation_config = {
        "temperature": 0.2,  # Lower temperature for more deterministic output
        "top_p": 0.95,
        "max_output_tokens": 2048,
    }
    
    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config
    )
    
    # Create the system prompt for intent analysis
    system_prompt = """You are an intent analysis system. Your job is to analyze the user's query and determine:
1. The primary intent of the query
2. Whether the query requires web search (factual, current events, specific information)
3. Whether the query is complex (multiple aspects, requires reasoning, hypothetical scenarios)
4. Key entities mentioned in the query
5. Main topics of the query

Format your response as a valid JSON object with the following structure:
{
  "intent": "string - brief description of primary intent",
  "confidence": float between 0 and 1,
  "requires_web_search": boolean,
  "is_complex_query": boolean,
  "entities": ["list", "of", "entities"],
  "topics": ["list", "of", "topics"]
}

Guidelines:
- Direct factual questions typically require web search
- Questions about current events require web search
- Complex reasoning questions typically don't require web search
- Creative or hypothetical questions don't require web search
- Personal advice questions don't require web search
- Code-related questions don't require web search unless asking about specific libraries or documentation
"""
    
    # Generate the analysis
    prompt = f"{system_prompt}\n\nAnalyze this query: {query}"
    response = model.generate_content(prompt)
    
    # Extract the JSON from the response
    import json
    import re
    
    # Find JSON pattern in the response
    json_match = re.search(r'({.*})', response.text, re.DOTALL)
    if json_match:
        try:
            analysis = json.loads(json_match.group(1))
            return IntentAnalysisResult(
                intent=analysis.get("intent", ""),
                confidence=analysis.get("confidence", 0.0),
                requires_web_search=analysis.get("requires_web_search", False),
                is_complex_query=analysis.get("is_complex_query", False),
                entities=analysis.get("entities", []),
                topics=analysis.get("topics", [])
            )
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            pass
    
    # Default fallback response
    return IntentAnalysisResult(
        intent="unknown",
        confidence=0.0,
        requires_web_search=False,
        is_complex_query=False,
        entities=[],
        topics=[]
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
