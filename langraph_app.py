import os
import json
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from typing import Dict, List, TypedDict
from model_config import get_model_config, get_groq_client
from decision_path import decision_path_node
from fetch_web_search_results_node import fetch_web_search_results_node
from calculator_tool import calculate_expression

# Load environment variables
load_dotenv()
config = get_model_config()
client = get_groq_client()

# Define state types
class AgentState(TypedDict):
    messages: List[Dict]
    config: Dict
    response: str
    intent_analysis: str

# Import prompt templates
try:
    from prompts import intent_analysis_prompt, ai_processing_prompt
except ImportError:
    def intent_analysis_prompt(user_query):
        return (
            "You are an intent analysis system. Analyze the user's query and provide a structured JSON with the following fields: "
            "'ai_inference': A brief, clear summary of what the user is asking or wants to achieve. "
            "'ai_reasoning': A concise explanation of your reasoning about the user's intent and how you arrived at your inference. "
            "Also include any other fields you would normally output (intent, confidence, requires_web_search, is_complex_query, entities, topics). "
            "\n\nFormat your response as a JSON object.\n\n"
            f"User Query: {user_query}"
        )
    def ai_processing_prompt(last_message, intent_analysis):
        return f"User Query:\n{last_message}\nIntent Analysis:\n{intent_analysis}\nPlease answer as a helpful AI assistant."

# Define nodes for the graph
import re, json

def intent_analysis_node(state: AgentState) -> AgentState:
    """Analyze user intent using prompt template (GROQ Llama4)"""
    last_message = state["messages"][-1]
    prompt = intent_analysis_prompt(last_message['content'])
    completion = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=config["temperature"],
        top_p=config["top_p"],
        stream=True
    )
    # Streaming: concatenate the streamed chunks
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""
    # Extract JSON block from response_text
    json_block = None
    pretty_json = None
    try:
        # Try to find a JSON code block
        match = re.search(r'```(?:json)?\s*([\s\S]+?)\s*```', response_text)
        if match:
            json_block = match.group(1)
        else:
            # Try to find the first curly-brace block
            match = re.search(r'(\{[\s\S]+\})', response_text)
            if match:
                json_block = match.group(1)
        if json_block:
            parsed = json.loads(json_block)
            pretty_json = json.dumps(parsed, indent=2, ensure_ascii=False)
            state["intent_analysis"] = parsed
            state["intent_analysis_raw"] = pretty_json
        else:
            # Fallback: try to parse the whole response
            parsed = json.loads(response_text)
            pretty_json = json.dumps(parsed, indent=2, ensure_ascii=False)
            state["intent_analysis"] = parsed
            state["intent_analysis_raw"] = pretty_json
    except Exception:
        # If all parsing fails, store the raw string for debugging
        state["intent_analysis"] = {}
        state["intent_analysis_raw"] = response_text
    return state

def web_search_node(state: AgentState) -> AgentState:
    """Synthesize web search results using prompt template (GROQ Llama4)"""
    last_message = state["messages"][-1]
    search_results = state.get("web_search_results", "")
    prompt = web_search_synthesis_prompt(last_message, search_results)
    completion = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=config["temperature"],
        top_p=config["top_p"],
        max_completion_tokens=config["max_completion_tokens"],
        stream=True,
        stop=config["stop"]
    )
    # Streaming: concatenate the streamed chunks
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""
    state["response"] = response_text
    return state

def ai_processing_node(state: AgentState) -> AgentState:
    """Process user query using AI processing prompt template, merging web search synthesis if available (GROQ Llama4)"""
    from model_config import get_groq_client, get_model_config
    from prompts import ai_processing_prompt
    config = get_model_config()
    client = get_groq_client()
    last_message = state["messages"][-1]
    intent_analysis = state.get("intent_analysis", "")
    web_search_synthesis = state.get("web_search_synthesis", None)
    if web_search_synthesis:
        prompt = f"You are Matrix AI, a conversational assistant with web search capabilities.\n\nHere are synthesized web search results for the user's query:\n{web_search_synthesis}\n\nUser Query:\n{last_message}\n\nPlease provide a concise, helpful, and final answer based on both the web search and your own knowledge."
    else:
        prompt = ai_processing_prompt(last_message, intent_analysis)
    completion = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=config["temperature"],
        top_p=config["top_p"],
        max_completion_tokens=config["max_completion_tokens"],
        stream=True,
        stop=config["stop"]
    )
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""
    state["response"] = response_text
    return state

def calculator_node(state: AgentState) -> AgentState:
    """Handle calculator expressions using the calculator tool."""
    last_message = state["messages"][-1]
    expr = last_message.get("content", "")
    result = calculate_expression(expr)
    state["response"] = result
    return state

def post_process(state: AgentState) -> AgentState:
    # Format and expose node-level results
    output = ""
    # Intent summary
    if "intent_analysis_raw" in state:
        output += "\n[Intent Analysis]\n" + str(state["intent_analysis_raw"]) + "\n"
    elif "intent_analysis" in state:
        output += "\n[Intent Analysis]\n" + str(state["intent_analysis"]) + "\n"
    # Web search synthesis (if present)
    if "web_search_synthesis" in state and state["web_search_synthesis"]:
        output += "\n[Web Search Synthesis]\n" + str(state["web_search_synthesis"]) + "\n"
    # AI response (if present)
    if "response" in state:
        output += "\n[Matrix AI Answer]\n" + str(state["response"]) + "\n"
    state["response"] = output.strip()
    # Ensure decision_result is present in the final state for downstream use
    if "decision_result" in state:
        state["decision_result"] = state["decision_result"]
    return state

def route_node(state: AgentState) -> AgentState:
    # This node just passes the state forward
    return state

def build_graph() -> StateGraph:
    """Build the LangGraph workflow with intent analysis, routing, web search, and AI processing nodes"""
    workflow = StateGraph(AgentState)
    workflow.add_node("intent_analysis_node", intent_analysis_node)
    workflow.add_node("decision_path", decision_path_node)
    workflow.add_node("route", route_node)
    workflow.add_node("fetch_web_search_results", fetch_web_search_results_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("calculator", calculator_node)
    workflow.add_node("ai_processing", ai_processing_node)
    workflow.add_node("post_process", post_process)
    # Edges: intent_analysis → decision_path → route → (fetch_web_search_results → web_search → ai_processing) or (ai_processing) or (calculator) → post_process → END
    workflow.add_edge("intent_analysis_node", "decision_path")
    workflow.add_edge("decision_path", "route")
    workflow.add_conditional_edges(
        "route",
        lambda state: (
            "ai_processing" if state.get("decision_result", {}).get("path") == "ai"
            else state.get("decision_result", {}).get("path", "ai_processing")
        ),
        {"fetch_web_search_results": "fetch_web_search_results", "ai_processing": "ai_processing", "calculator": "calculator"}
    )
    # Tool paths
    workflow.add_edge("fetch_web_search_results", "web_search")
    workflow.add_edge("web_search", "ai_processing")
    workflow.add_edge("calculator", "post_process")
    workflow.add_edge("ai_processing", "post_process")
    workflow.add_edge("post_process", END)
    workflow.set_entry_point("intent_analysis_node")
    return workflow

def safe_requires_web_search(intent_analysis):
    try:
        if not intent_analysis:
            return False
        data = json.loads(intent_analysis)
        return data.get("requires_web_search", False)
    except Exception:
        return False

# Create the compiled graph
graph = build_graph().compile()

# Create a streaming version of the graph
def create_streaming_graph():
    """Create a streaming version of the graph"""
    return build_graph().compile(streaming=True)

