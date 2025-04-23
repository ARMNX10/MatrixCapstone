# MatrixCapstone: Voice-Enabled AI Assistant

MatrixCapstone is a voice-activated AI assistant powered by Google's Gemini AI and a LangGraph workflow. It supports natural language queries, web search, music playback, and both terminal and web-based interfaces.

---

## Features

- **Voice Interaction:**
  - Speech recognition using Google's API
  - Text-to-speech with pyttsx3
  - Interruptible speech output
- **AI Processing:**
  - Uses Google's Gemini AI models (1.5-pro, 2.0-flash)
  - Intent analysis and reasoning with structured output
  - Decision routing between AI and web search
- **Web Search:**
  - Uses Serper API for factual and current event queries
  - Synthesizes and cites sources in responses
- **Multi-Interface:**
  - Command-line interface
  - WebSocket/web interface (Nodes.py)
  - Streamlit web app
- **Other Utilities:**
  - Music playback
  - Open websites by voice command
  - Time queries
  - Conversation history

---

## Project Structure

- `main.py`           — Command-line entry point
- `Nodes.py`          — WebSocket/web interface, voice core
- `langraph_app.py`   — LangGraph workflow definition
- `intent_analyzer.py`— Intent analysis logic
- `decision_path.py`  — Decision routing logic
- `web_search_api.py` — Serper API integration
- `prompts.py`        — Prompt templates
- `requirement.py`    — Dependency management
- `fetch_web_search_results_node.py` — Web search node
- `calculator_tool.py` — Calculator node/tool

---

## Setup & Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/ARMNX10/MatrixCapstone.git
   cd MatrixCapstone
   ```

2. **Install Requirements:**
   ```sh
   pip install -r requirement.py
   ```
   Or manually install:
   - google-generativeai==0.8.4
   - google-ai-generativelanguage==0.6.15
   - langgraph
   - streamlit
   - pyttsx3
   - pynput
   - speechrecognition
   - requests
   - python-dotenv
   - loguru

3. **Environment Variables:**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   TTS_ENGINE=coqui
   ```

---

## Usage

- **Command Line:**
  ```sh
  python langmain.py
  ```
  - Say "activate" or "wake up" to start.
  - Speak your query when prompted.
  - Say "exit" or "quit" to stop.

- **Web Interface:**
  - Run the web server (see Nodes.py or Streamlit app).

---

## Key Environment Variables
- `GEMINI_API_KEY` — Google Gemini AI key
- `SERPER_API_KEY` — Serper API key for web search
- `TTS_ENGINE`     — (Optional) TTS engine (e.g., coqui)

---

## Credits
- Built by ARMNX10
- Powered by Google Gemini, Serper API, LangGraph, and open source Python libraries

---

## License
MIT License

---

## Troubleshooting
- Ensure your API keys are valid and set in `.env`.
- For voice issues, check your microphone and TTS engine.
- For web search, ensure you have not exceeded Serper API quota.

---

## Contributing
Pull requests and issues are welcome!
