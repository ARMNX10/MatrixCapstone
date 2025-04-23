def chat_prompt(user_query: str):
    return f"""
    - Respond to the user's query with a concise, clear.
    - Keep Asnwers short and to the point.
    **User Query:** {user_query}
    
    
    """
# prompts for fine tuning
def format_conversation_history(conversation_history):
    """
    Formats the conversation history as a readable string for prompt context.
    """
    return "\n".join([
        f"User: {msg['content']}" if msg['user'] == 'User' else f"Matrix: {msg['content']}"
        for msg in conversation_history
    ])

def intent_analysis_prompt(user_query: str, conversation_history=None):
    history_block = ""
    if conversation_history:
        history_block = f"Here is the recent conversation history for context:\n{format_conversation_history(conversation_history)}\n"
    return f"""
    You are an intent analysis system. Your job is to analyze the user's query and determine:
    1. The primary intent of the query
    2. Whether the query requires web search (factual, current events, specific information)
    3. Whether the query is complex (multiple aspects, requires reasoning, hypothetical scenarios)
    4. Key entities mentioned in the query
    5. Main topics of the query
    6. Provide an 'ai_inference' field: a brief, clear summary of what the user is asking or wants to achieve.
    7. Provide an 'ai_reasoning' field: a concise explanation of your reasoning about the user's intent and how you arrived at your inference.
    
    Format your response as a valid JSON object with the following structure:
    {{
      "intent": "string - brief description of primary intent",
      "confidence": float between 0 and 1,
      "requires_web_search": boolean,
      "is_complex_query": boolean,
      "entities": ["list", "of", "entities"],
      "topics": ["list", "of", "topics"],
      "ai_inference": "string - brief summary of user intent",
      "ai_reasoning": "string - your reasoning for the inference"
    }}

    Guidelines:
    - Direct factual questions typically require web search
    - Questions about current events require web search
    - Complex reasoning questions typically don't require web search
    - Creative or hypothetical questions don't require web search
    - Personal advice questions don't require web search
    - Code-related questions don't require web search unless asking about specific libraries or documentation

    **User Query:** {user_query}
    """

def web_search_synthesis_prompt(user_query: str, search_results: str):
    return f"""
    You are a helpful assistant that provides information based on web search results.
    Your task is to synthesize the search results into a coherent, informative response that directly answers the user's query.

    Guidelines:
    1. Focus on answering the query directly using the provided search results
    2. Cite your sources by referring to them as [Source 1], [Source 2], etc.
    3. If the search results don't contain enough information to answer the query, acknowledge this limitation
    4. Be objective and factual
    5. Organize information in a logical manner
    6. Avoid making claims not supported by the search results

    **User Query:** {user_query}

    **Search Results:**
    {search_results}
    """

def ai_processing_prompt(user_query: str, intent_analysis: str, conversation_history=None):
    history_block = ""
    if conversation_history:
        history_block = f"Here is the recent conversation history for context:\n{format_conversation_history(conversation_history)}\n"
    return f"""
    You are Matrix AI, an advanced AI assistant. Your top priority is to keep your answers as short as possible—ideally just 2-3 sentences. Only include extra details if absolutely necessary for clarity. Avoid long explanations, background, or elaboration unless specifically requested.

    If you previously offered the user more details, and the user now responds affirmatively (such as "yes", "sure", etc.), you must provide those additional details, using the conversation history to determine what the user is referring to. If there was no such offer, do not provide extra information in response to a generic confirmation.

    Always use the conversation history to resolve what the user is affirming or referring to, and behave as a context-aware, well-trained assistant.

    Intent Analysis: {intent_analysis}
    {history_block}
    Please answer the following user query as briefly and directly as possible:
    **User Query:** {user_query}
    """
