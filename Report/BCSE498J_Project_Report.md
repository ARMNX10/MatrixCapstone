# BCSE498J Project II Report
# Voice-Implemented AI Assistant

## Team Members
[Your Name]

## Declaration by the Candidate

I hereby declare that the project report entitled "Voice-Implemented AI Assistant" submitted by me for the BCSE498J Project II is the record of work carried out by me under the guidance of the faculty and has not formed the basis for the award of any degree or diploma or fellowship or other similar titles to any candidate in any university.

Date: April 13, 2025  
Place: [Your Location]

Signature of the Student  
[Your Name]

## Certificate

This is to certify that the project report entitled "Voice-Implemented AI Assistant" submitted by [Your Name] to VIT University, in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering is a record of bonafide work carried out by him/her under my supervision and guidance.

Date: April 13, 2025  
Place: [Your Location]

Signature of the Guide  
[Your Name]

## Executive Summary

This project implements a voice-enabled AI assistant that leverages Google's Gemini AI models and LangGraph workflow orchestration to create an intelligent, conversational interface. The system combines speech recognition, natural language processing, and web search capabilities to provide users with a versatile assistant that can respond to voice commands, answer questions, perform web searches, and execute various tasks.

The assistant, named "Matrix," features multiple interfaces including a voice-based command-line interface, a web interface with WebSocket support, and a Streamlit web application. The system's architecture employs an intent analysis system that determines whether queries require web search or AI processing, routing them appropriately through a decision-making workflow.

Key technologies utilized include Google's Gemini AI models (1.5-pro and 2.0-flash), speech recognition via Google's API, text-to-speech synthesis using pyttsx3, web search capabilities through the Serper API, and browser automation with Selenium. The system is designed with a modular architecture that separates concerns between intent analysis, decision routing, web search, and AI processing.

This project demonstrates the integration of multiple AI technologies to create a practical, voice-enabled assistant that can understand natural language, search for information, and provide helpful responses to users through both voice and text interfaces.

## Acknowledgement

I would like to express my sincere gratitude to all those who have contributed to the successful completion of this project.

First and foremost, I extend my heartfelt thanks to my project guide for their invaluable guidance, continuous support, and insightful feedback throughout the development of this voice-implemented AI assistant.

I am also grateful to the faculty members of the Computer Science and Engineering department at VIT University for providing the necessary resources and knowledge that formed the foundation of this project.

Special thanks to Google for providing access to their Gemini AI models, which serve as the core intelligence of this assistant.

Finally, I would like to acknowledge the open-source community whose libraries and frameworks have been instrumental in the development of this project.

[Your Name]

## Table of Contents

1. Introduction
2. Literature Review
3. System Architecture
4. Implementation Details
5. Features and Functionality
6. Technologies Used
7. Results and Discussion
8. Conclusion and Future Work
9. References
10. Appendices

## List of Tables

| Table No. | Title | Page No. |
|-----------|-------|----------|
| 1 | System Requirements | XX |
| 2 | API Services Used | XX |
| 3 | Performance Metrics | XX |

## List of Figures

| Figure No. | Title | Page No. |
|------------|-------|----------|
| 1 | System Architecture Diagram | XX |
| 2 | LangGraph Workflow | XX |
| 3 | User Interface Screenshots | XX |

## List of Symbols, Abbreviations and Nomenclature

| Abbreviation | Full Form |
|--------------|-----------|
| AI | Artificial Intelligence |
| NLP | Natural Language Processing |
| TTS | Text-to-Speech |
| STT | Speech-to-Text |
| API | Application Programming Interface |
| LLM | Large Language Model |

## 1. Introduction

### 1.1 Background

Voice assistants have become increasingly prevalent in our daily lives, from smartphones to smart home devices. These systems leverage advances in speech recognition, natural language processing, and artificial intelligence to provide users with a natural and intuitive way to interact with technology. The development of powerful language models like Google's Gemini has opened new possibilities for creating more intelligent and capable voice assistants.

### 1.2 Problem Statement

Traditional voice assistants often have limitations in their understanding of complex queries, ability to search for information, and flexibility in handling different types of requests. This project aims to address these limitations by creating a voice-implemented AI assistant that can:

1. Accurately recognize and interpret spoken commands
2. Intelligently determine whether a query requires web search or AI processing
3. Provide informative responses through both voice and text interfaces
4. Execute various tasks based on user commands
5. Maintain context in conversations

### 1.3 Objectives

The primary objectives of this project are:

1. Develop a voice-enabled AI assistant using Google's Gemini models
2. Implement a decision-making system to route queries appropriately
3. Integrate web search capabilities for factual queries
4. Create multiple user interfaces (voice, web, Streamlit)
5. Implement a modular architecture for extensibility
6. Provide natural and helpful responses to user queries

### 1.4 Scope

The scope of this project encompasses:

- Voice recognition and synthesis
- Natural language understanding and processing
- Web search and information retrieval
- LangGraph workflow implementation
- Multiple user interfaces
- Basic task execution (opening websites, playing music, etc.)

## 2. Literature Review

### 2.1 Evolution of Voice Assistants

Voice assistants have evolved significantly since their inception. Early systems like IBM's Shoebox (1962) could recognize just 16 spoken words. Modern assistants like Siri, Alexa, and Google Assistant leverage advanced AI to understand natural language and perform complex tasks. The field has seen rapid advancement with the introduction of large language models (LLMs) that provide more sophisticated natural language understanding and generation capabilities.

### 2.2 Speech Recognition Technologies

Speech recognition has progressed from simple pattern matching to sophisticated deep learning models. Modern systems use techniques like recurrent neural networks (RNNs), convolutional neural networks (CNNs), and transformer-based models to convert speech to text with high accuracy. This project utilizes Google's Speech Recognition API, which employs these advanced techniques to provide accurate transcription of spoken commands.

### 2.3 Large Language Models

Large language models have revolutionized natural language processing. Models like GPT, BERT, and Google's Gemini can understand context, generate coherent text, and perform various language tasks. This project leverages Google's Gemini models (1.5-pro and 2.0-flash) to provide intelligent responses to user queries. These models offer advantages in terms of understanding context, generating natural language, and providing informative responses.

### 2.4 Workflow Orchestration

Workflow orchestration in AI systems allows for the coordination of multiple components to process user inputs and generate appropriate outputs. LangGraph, used in this project, provides a framework for creating directed graphs of processing nodes, enabling complex decision-making and routing of queries. This approach offers advantages in terms of modularity, extensibility, and separation of concerns.

## 3. System Architecture

### 3.1 Overall Architecture

The system follows a modular architecture with several key components:

1. **Voice Interface**: Handles speech recognition and synthesis
2. **Intent Analyzer**: Determines the intent and requirements of user queries
3. **Decision Router**: Routes queries to appropriate processing paths
4. **Web Search Tool**: Retrieves information from the internet for factual queries
5. **AI Processing**: Generates responses using Gemini models
6. **User Interfaces**: Provides multiple ways to interact with the assistant

These components are orchestrated through a LangGraph workflow that manages the flow of information and decision-making process.

### 3.2 Component Descriptions

#### 3.2.1 Voice Interface

The voice interface is implemented in `Nodes.py` and provides:
- Speech recognition using Google's speech recognition API
- Text-to-speech synthesis using pyttsx3
- Voice command processing and execution

#### 3.2.2 Intent Analyzer

The intent analyzer (`intent_analyzer.py`) analyzes user queries to determine:
- The primary intent of the query
- Whether the query requires web search
- Whether the query is complex
- Key entities and topics mentioned

#### 3.2.3 Decision Router

The decision router (`decision_path.py`) uses the intent analysis to:
- Determine the appropriate processing path (AI or web search)
- Route the query to the correct processing node
- Provide reasoning for the routing decision

#### 3.2.4 Web Search Tool

The web search tool (`web_search_tool.py`) handles factual queries by:
- Searching the web using the Serper API
- Extracting relevant information from search results
- Synthesizing a coherent response using Gemini

#### 3.2.5 AI Processing

AI processing is handled by various components that:
- Process complex queries using Gemini models
- Generate informative and helpful responses
- Maintain context in conversations

#### 3.2.6 User Interfaces

The system provides multiple user interfaces:
- Command-line interface with voice input/output
- Web interface with WebSocket support
- Streamlit web application

### 3.3 Data Flow

The data flow through the system follows these steps:

1. User speaks a command or query
2. Speech is converted to text
3. Intent analyzer determines the nature of the query
4. Decision router selects the appropriate processing path
5. Query is processed by either AI or web search
6. Response is generated and returned to the user
7. Text response is converted to speech (if using voice interface)

## 4. Implementation Details

### 4.1 Voice Recognition and Synthesis

Voice recognition is implemented using Google's Speech Recognition API through the `speech_recognition` library. The `takecommand()` function in `Nodes.py` handles the recording and recognition of user speech:

```python
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"\n==> User: {query}")
        asyncio.run(send_message(query, "User"))
        return query.lower()
    except:
        return ""
```

Text-to-speech synthesis is implemented using the `pyttsx3` library, which provides a simple interface to the system's speech synthesis capabilities:

```python
def say(text):
    engine = pyttsx3.init()
    Id = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enUS_MarkM'
    engine.setProperty('voice', Id)
    filtered_text = remove_special_chars(text)
    print(f"\n==> Matrix AI: {filtered_text}")
    asyncio.run(send_message(filtered_text, "matrix"))
    engine.say(text=filtered_text)
    engine.runAndWait()
    return filtered_text
```

### 4.2 Intent Analysis

Intent analysis is implemented in `intent_analyzer.py` using Google's Gemini model to analyze user queries:

```python
def analyze_intent(query: str) -> IntentAnalysisResult:
    # Configure the model
    generation_config = {
        "temperature": 0.2,
        "top_p": 0.95,
        "max_output_tokens": 2048,
    }
    
    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config
    )
    
    # Create the system prompt for intent analysis
    system_prompt = """You are an intent analysis system..."""
    
    # Generate the analysis
    prompt = f"{system_prompt}\n\nAnalyze this query: {query}"
    response = model.generate_content(prompt)
    
    # Extract the JSON from the response
    # ...
    
    return IntentAnalysisResult(...)
```

### 4.3 Decision Routing

Decision routing is implemented in `decision_path.py` and determines which processing path to take based on the intent analysis:

```python
def determine_path(analysis: IntentAnalysisResult) -> DecisionPathResult:
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
```

### 4.4 Web Search

Web search is implemented in `web_search_tool.py` using the Serper API to search the web and Gemini to synthesize the results:

```python
def search_web(query: str, num_results: int = 5) -> List[SearchResult]:
    # Check if SERPER_API_KEY is available
    if SERPER_API_KEY:
        logger.info(f"[SEARCH] Using Serper API to search for: '{query}'")
        try:
            # Use Serper API for web search
            url = "https://google.serper.dev/search"
            payload = json.dumps({
                "q": query,
                "num": num_results
            })
            headers = {
                'X-API-KEY': SERPER_API_KEY,
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            
            # Process response
            # ...
            
            return results
        except Exception as e:
            logger.error(f"[SEARCH] Error using Serper API: {e}")
            # Fall back to mock implementation
    
    # Mock implementation for testing
    # ...
```

### 4.5 LangGraph Workflow

The LangGraph workflow is implemented in `langraph_app.py` and orchestrates the processing of user queries:

```python
def build_graph() -> StateGraph:
    """Build the LangGraph workflow"""
    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("generate", generate_response)
    workflow.add_node("post_process", post_process)
    
    # Add edges
    workflow.add_edge("generate", "post_process")
    workflow.add_edge("post_process", END)
    
    # Set entry point
    workflow.set_entry_point("generate")
    
    return workflow
```

### 4.6 User Interfaces

The system provides multiple user interfaces:

1. Command-line interface with voice input/output (`main_app.py`)
2. Web interface with WebSocket support (`Nodes.py`)
3. Streamlit web application (`streamlit_app.py`)

The Streamlit interface is implemented as follows:

```python
def init_streamlit_app():
    """Initialize the Streamlit app"""
    if "app" not in st.session_state:
        st.session_state.app = MatrixAIApp()
        
    if "config" not in st.session_state:
        st.session_state.config = {
            "temperature": 1.0,
            "top_p": 0.95,
        }
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    return st.session_state.app

# Main Streamlit app
st.title("Matrix AI Assistant")
st.subheader("Powered by LangGraph and Gemini")

# Initialize app
app = init_streamlit_app()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_query = st.chat_input("Ask Matrix AI something...")

if user_query:
    # Process query and display response
    # ...
```

## 5. Features and Functionality

### 5.1 Voice Commands

The assistant can process various voice commands, including:

- General questions and queries
- Opening websites (e.g., "open youtube")
- Playing music (e.g., "play random music")
- Checking the time (e.g., "what's the time")
- Activating and deactivating the assistant

### 5.2 Web Search

The assistant can search the web for factual information and synthesize the results into coherent responses. This feature is particularly useful for:

- Answering factual questions
- Providing information about current events
- Retrieving specific information from the internet

### 5.3 AI Processing

For complex queries that don't require web search, the assistant uses Gemini models to generate informative responses. This includes:

- Answering complex questions
- Providing explanations and reasoning
- Generating creative content
- Offering advice and suggestions

### 5.4 Multiple Interfaces

The assistant can be accessed through multiple interfaces:

- Voice interface with speech recognition and synthesis
- Command-line interface for text input/output
- Web interface with WebSocket support
- Streamlit web application

### 5.5 Context Awareness

The assistant maintains context in conversations, allowing for more natural and coherent interactions. This is achieved through:

- LangGraph workflow that maintains state
- Intent analysis that understands the context of queries
- Response generation that takes context into account

## 6. Technologies Used

### 6.1 Google Gemini AI

Google's Gemini AI models (1.5-pro and 2.0-flash) are used for:

- Intent analysis
- Response generation
- Web search result synthesis

These models provide advanced natural language understanding and generation capabilities.

### 6.2 LangGraph

LangGraph is used for workflow orchestration, providing:

- A directed graph of processing nodes
- State management for conversations
- Decision-making and routing of queries

### 6.3 Speech Recognition and Synthesis

Speech technologies used include:

- Google's Speech Recognition API for converting speech to text
- pyttsx3 for text-to-speech synthesis

### 6.4 Web Search

Web search capabilities are provided by:

- Serper API for searching the web
- BeautifulSoup for extracting content from web pages
- Gemini for synthesizing search results

### 6.5 User Interface Technologies

User interface technologies include:

- Command-line interface for text input/output
- WebSockets for real-time communication with web interfaces
- Streamlit for creating web applications
- Selenium for browser automation

## 7. Results and Discussion

### 7.1 System Performance

The system demonstrates good performance in terms of:

- Speech recognition accuracy
- Intent analysis precision
- Response generation quality
- Web search result synthesis

The use of Google's Gemini models provides high-quality responses, while the LangGraph workflow ensures appropriate routing of queries.

### 7.2 Limitations

The system has some limitations, including:

- Dependency on internet connectivity for web search and some AI features
- Potential for speech recognition errors in noisy environments
- Limited ability to handle very specialized or technical queries
- Dependency on external APIs that may have rate limits or costs

### 7.3 Comparison with Existing Systems

Compared to existing voice assistants like Siri, Alexa, and Google Assistant, this system offers:

- More flexible architecture for customization
- Integration of advanced language models (Gemini)
- Workflow-based approach to query processing
- Multiple interfaces for different use cases

However, commercial assistants may offer better integration with devices and services, as well as more polished user experiences.

## 8. Conclusion and Future Work

### 8.1 Conclusion

This project has successfully implemented a voice-enabled AI assistant that leverages Google's Gemini models and LangGraph workflow orchestration. The system can process voice commands, search the web for information, and provide informative responses through both voice and text interfaces.

The modular architecture and workflow-based approach provide flexibility and extensibility, allowing for future enhancements and customizations. The integration of advanced language models and speech technologies demonstrates the potential of these technologies for creating intelligent and helpful assistants.

### 8.2 Future Work

Future work on this project could include:

1. **Enhanced Context Management**: Implementing more sophisticated context management to handle complex, multi-turn conversations.

2. **Expanded Capabilities**: Adding support for more tasks and integrations, such as controlling smart home devices, managing calendars, and accessing more services.

3. **Improved Voice Recognition**: Implementing custom voice recognition models for better accuracy and support for more languages and accents.

4. **Personalization**: Adding user profiles and personalization features to tailor responses and behaviors to individual users.

5. **Offline Capabilities**: Implementing offline functionality for core features to reduce dependency on internet connectivity.

6. **Mobile Applications**: Developing mobile applications for iOS and Android to make the assistant more accessible.

7. **Enhanced Security**: Implementing more robust security measures for sensitive commands and information.

8. **Performance Optimization**: Optimizing the system for better performance on resource-constrained devices.

## 9. References

1. Google Generative AI. (2023). Gemini API Documentation. Retrieved from https://ai.google.dev/docs

2. LangGraph. (2023). LangGraph Documentation. Retrieved from https://langchain-ai.github.io/langgraph/

3. Jurafsky, D., & Martin, J. H. (2023). Speech and Language Processing (3rd ed.). Retrieved from https://web.stanford.edu/~jurafsky/slp3/

4. Mozilla. (2023). Web Speech API. Retrieved from https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API

5. Streamlit. (2023). Streamlit Documentation. Retrieved from https://docs.streamlit.io/

6. Serper. (2023). Serper API Documentation. Retrieved from https://serper.dev/api-documentation

7. Selenium. (2023). Selenium Documentation. Retrieved from https://www.selenium.dev/documentation/

8. pyttsx3. (2023). pyttsx3 Documentation. Retrieved from https://pyttsx3.readthedocs.io/

9. SpeechRecognition. (2023). SpeechRecognition Documentation. Retrieved from https://pypi.org/project/SpeechRecognition/

10. BeautifulSoup. (2023). BeautifulSoup Documentation. Retrieved from https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## 10. Appendices

### Appendix A: Installation and Setup

To set up the project, follow these steps:

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the environment variables:
   - GEMINI_API_KEY: Your Google Gemini API key
   - SERPER_API_KEY: Your Serper API key (for web search)

4. Run the application:
   - For voice interface: `python main_app.py`
   - For Streamlit interface: `streamlit run streamlit_app.py`

### Appendix B: Code Structure

The project code is organized as follows:

- `main_app.py`: Main application with voice interface
- `Nodes.py`: Core functionality for voice recognition and synthesis
- `intent_analyzer.py`: Intent analysis system
- `decision_path.py`: Decision routing system
- `web_search_tool.py`: Web search functionality
- `langraph_app.py`: LangGraph workflow implementation
- `streamlit_app.py`: Streamlit web application
- `prompts.py`: Prompt templates for AI interactions
- `main.py`: Simple command-line interface
- `.env`: Environment variables (API keys)

### Appendix C: API Documentation

#### Google Gemini API

The project uses Google's Gemini API for natural language processing. Key models used:

- `gemini-1.5-pro`: Used for intent analysis and complex query processing
- `gemini-2.0-flash`: Used for simple query processing and response generation

#### Serper API

The Serper API is used for web search functionality. It provides a simple interface to Google search results in JSON format.

#### Speech Recognition API

Google's Speech Recognition API is used for converting speech to text. It provides high-quality transcription of spoken commands.

### Appendix D: User Guide

#### Voice Commands

To use the voice interface:

1. Start the application with `python main_app.py`
2. Say "Wake up" or "Activate" to activate the assistant
3. Speak your command or query
4. Listen to the assistant's response

Common commands include:

- "Open [website]" (e.g., "Open YouTube")
- "Play random music"
- "What's the time"
- "How do I [task]" (e.g., "How do I make pasta")
- "Who is [person]" (e.g., "Who is Albert Einstein")
- "Matrix deactivate" (to shut down the assistant)

#### Streamlit Interface

To use the Streamlit interface:

1. Start the application with `streamlit run streamlit_app.py`
2. Type your query in the input box
3. View the assistant's response in the chat window
