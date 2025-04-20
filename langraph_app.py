import os
import streamlit as st
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.messages import HumanMessage
from langgraph.graph import END, StateGraph
from typing import Dict, List, TypedDict, Annotated, Sequence
import google.generativeai as genai

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Generative AI
genai.configure(api_key=API_KEY)

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
        return f"Analyze the following user intent:\n{user_query}"
    def ai_processing_prompt(last_message, intent_analysis):
        return f"User Query:\n{last_message}\nIntent Analysis:\n{intent_analysis}\nPlease answer as a helpful AI assistant."

# Define nodes for the graph
def intent_analysis_node(state: AgentState) -> AgentState:
    """Analyze user intent using prompt template"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        convert_system_message_to_human=True,
        temperature=state["config"].get("temperature", 1.0),
        top_p=state["config"].get("top_p", 0.95),
        google_api_key=API_KEY,
    )
    last_message = state["messages"][-1]
    prompt = intent_analysis_prompt(last_message['content'])
    response = llm.invoke([HumanMessage(content=prompt)])
    state["intent_analysis"] = response.content
    return state

def web_search_node(state: AgentState) -> AgentState:
    """Synthesize web search results using prompt template"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        convert_system_message_to_human=True,
        temperature=state["config"].get("temperature", 1.0),
        top_p=state["config"].get("top_p", 0.95),
        google_api_key=API_KEY,
    )
    last_message = state["messages"][-1]
    search_results = state.get("web_search_results", "")
    prompt = web_search_synthesis_prompt(last_message, search_results)
    response = llm.invoke([HumanMessage(content=prompt)])
    state["web_search_synthesis"] = response.content
    return state

def ai_processing_node(state: AgentState) -> AgentState:
    """Process user query using AI processing prompt template, merging web search synthesis if available"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        convert_system_message_to_human=True,
        temperature=state["config"].get("temperature", 1.0),
        top_p=state["config"].get("top_p", 0.95),
        google_api_key=API_KEY,
    )
    last_message = state["messages"][-1]
    intent_analysis = state.get("intent_analysis", "")
    web_search_synthesis = state.get("web_search_synthesis", None)
    if web_search_synthesis:
        prompt = f"You are Matrix AI, a conversational assistant with web search capabilities.\n\nHere are synthesized web search results for the user's query:\n{web_search_synthesis}\n\nUser Query:\n{last_message}\n\nPlease provide a concise, helpful, and final answer based on both the web search and your own knowledge."
    else:
        prompt = ai_processing_prompt(last_message, intent_analysis)
    response = llm.invoke([HumanMessage(content=prompt)])
    state["response"] = response.content
    return state

def post_process(state: AgentState) -> AgentState:
    # Format and expose node-level results
    output = ""
    # Intent summary
    if "intent_analysis" in state:
        output += "\n[Intent Analysis]\n" + str(state["intent_analysis"]) + "\n"
    # Web search synthesis (if present)
    if "web_search_synthesis" in state and state["web_search_synthesis"]:
        output += "\n[Web Search Synthesis]\n" + str(state["web_search_synthesis"]) + "\n"
    # AI response (if present)
    if "response" in state:
        output += "\n[Matrix AI Answer]\n" + str(state["response"]) + "\n"
    state["response"] = output.strip()
    return state

def route_node(state: AgentState) -> AgentState:
    # This node just passes the state forward
    return state

def build_graph() -> StateGraph:
    """Build the LangGraph workflow with intent analysis, routing, web search, and AI processing nodes"""
    workflow = StateGraph(AgentState)
    workflow.add_node("intent_analysis_node", intent_analysis_node)
    workflow.add_node("route", route_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("ai_processing", ai_processing_node)
    workflow.add_node("post_process", post_process)
    # Edges: intent_analysis → route → (web_search or ai_processing) → ai_processing → post_process → END
    workflow.add_edge("intent_analysis_node", "route")
    workflow.add_conditional_edges(
        "route",
        lambda state: "web_search" if safe_requires_web_search(state["intent_analysis"]) else "ai_processing",
        {"web_search": "web_search", "ai_processing": "ai_processing"}
    )
    workflow.add_edge("web_search", "ai_processing")
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

# App class for streamlit integration
class MatrixAIApp:
    def __init__(self):
        self.streaming_graph = create_streaming_graph()
        
    def stream(self, input_data, config, stream_mode='messages'):
        """Stream responses from the AI model"""
        # Initialize state
        state = {
            "messages": input_data["messages"],
            "config": config,
            "response": ""
        }
        
        # Stream the response
        for chunk in self.streaming_graph.stream(state, stream_mode=stream_mode):
            yield chunk

# Initialize Streamlit app
def init_streamlit_app():
    """Initialize the Streamlit app"""
    if "app" not in st.session_state:
        st.session_state.app = MatrixAIApp()
        
    if "config" not in st.session_state:
        st.session_state.config = {
            "temperature": 1.0,
            "top_p": 0.95,
        }
    
    return st.session_state.app

# Example usage in a Streamlit app
if __name__ == "__main__":
    st.title("Matrix AI Assistant")
    
    # Initialize app
    app = init_streamlit_app()
    
    # Create a text input
    user_input = st.text_input("Ask Matrix AI:")
    
    if user_input:
        # Display user message
        st.write(f"User: {user_input}")
        
        # Display AI response with streaming
        st.write("Matrix AI: ")
        response_container = st.empty()
        full_response = ""
        
        # Stream the response
        for chunk in app.stream({"messages": [user_input]}, st.session_state.config, stream_mode='messages'):
            if "response" in chunk:
                full_response += chunk["response"]
                response_container.markdown(full_response)
