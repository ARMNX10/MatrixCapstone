import os
import time
import random
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from langraph_app import build_graph, AgentState  # Reuse your LangGraph workflow
import subprocess

# --- Config ---
load_dotenv()
MUSIC_DIR = os.getenv("R:\Music", "music")  
WAKE_WORDS = ["activate", "wake up"]
SITES = [
    ["youtube", "youtube.com"],
    ["wikipedia", "wikipedia.org"],
    ["google", "google.com"],
    ["whatsapp", "web.whatsapp.com"],
    ["gmail", "mail.google.com"],
    ["reddit", "reddit.com"],
    ["twitter", "twitter.com"],
    ["facebook", "facebook.com"],
    ["instagram", "instagram.com"],
    ["amazon", "amazon.com"],
    ["flipkart", "flipkart.com"],
    ["stackoverflow", "stackoverflow.com"],
    ["github", "github.com"],
    ["vtop", "vtop.vit.ac.in"],
    ["vit website", "vtop.vit.ac.in"],
    ["netflix", "netflix.com"],
    ["prime video", "primevideo.com"],
    ["linkedin", "linkedin.com"],
    ["spotify", "spotify.com"],
    ["quora", "quora.com"],
    ["zoom", "zoom.us"],
    ["discord", "discord.com"],
    ["drive", "drive.google.com"],
    ["maps", "maps.google.com"],
    ["news", "news.google.com"],
]

# --- Voice Engine ---
import pyttsx3
engine = pyttsx3.init()
# Registry tokens for Microsoft voices
VOICE_DAVID = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0'
VOICE_MARK = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_MARK_11.0'
engine.setProperty('voice', VOICE_DAVID)

def speak(text, use_mark=False):
    print(f"\n==> Matrix AI: {text}")
    if use_mark:
        engine.setProperty('voice', VOICE_MARK)
    else:
        engine.setProperty('voice', VOICE_DAVID)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"==> User: {query}")
        return query.lower()
    except Exception as e:
        print("Sorry, could not understand. Please repeat.")
        return ""

def wait_for_wake_word():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("Say 'activate' or 'wake up' to start the assistant...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print("[Launcher] Listening for wake word...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"[Launcher] Heard: {text}")
                if any(word in text for word in WAKE_WORDS):
                    print("[Launcher] Wake word detected! Launching assistant...")
                    speak("Matrix activated. How can I help you?", use_mark=True)
                    return
            except sr.UnknownValueError:
                print("[Launcher] Could not understand audio.")
            except sr.RequestError as e:
                print(f"[Launcher] Could not request results; {e}")
            time.sleep(0.5)

def play_random_music():
    if not os.path.isdir(MUSIC_DIR):
        speak("Music directory not found.")
        return
    songs = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav'))]
    if not songs:
        speak("No music files found.")
        return
    song = random.choice(songs)
    song_path = os.path.join(MUSIC_DIR, song)
    speak(f"Playing {song}")
    os.startfile(song_path)

import warnings
warnings.filterwarnings("ignore", message="Convert_system_message_to_human will be deprecated!*")

import re

# def fake_stream(text, delay=0.006):
#     words = re.findall(r'\S+|\s+', text)  # Preserve spaces for natural printing
#     buffer = ""
#     for word in words:
#         print(word, end="", flush=True)
#         buffer += word
#         time.sleep(delay)
#     print("\n" + "="*50 + "\n")

from prompts import chat_prompt


MEMORY_LENGTH = 20  # Number of messages to keep in memory

def update_memory(conversation_history, new_message):
    conversation_history.append(new_message)
    return conversation_history[-MEMORY_LENGTH:]

def process_query_with_langgraph(query, conversation_history):
    graph = build_graph().compile()
    # System prompt for conversational AI
    system_prompt = (
        "You are Matrix, a friendly, helpful conversational AI assistant. "
        "Be concise, clear, and avoid unnecessary technical jargon. "
        "Keep your responses short, easy to read, and conversational. DO NOT GIVE LONG ANSWER WHICH WOULD TAKE LONGER TO READ ALOUD.\n"
    )
    conversation_history = update_memory(conversation_history, {"user": "User", "content": query})
    messages_block = "\n".join([
        f"User: {msg['user']}\n{msg['content']}" if msg['user'] else msg['content']
        for msg in conversation_history
    ])
    user_prompt = chat_prompt(query)
    full_prompt = f"{system_prompt}\n{messages_block}\n{user_prompt}"
    state = {
        "messages": [{"content": full_prompt}],
        "config": {"temperature": 1.0, "top_p": 0.95},
        "response": "",
        "intent_analysis": {},
        "decision_result": {},
        "web_search_results": []
    }
    result = graph.invoke(state)
    response_text = result.get("response", "")
    if response_text:
        import re
        # Print Intent Analysis (if present)
        import json
        if 'intent_analysis' in result and result['intent_analysis']:
            print(json.dumps(result['intent_analysis'], indent=2, ensure_ascii=False))
            # Print decision_result (decision path) in one line with separator
            if 'decision_result' in result and result['decision_result']:
                print("=========================")
                print(json.dumps(result['decision_result'], indent=2, ensure_ascii=False))
        else:
            # fallback to regex extraction if needed
            intent_match = re.search(r"\[Intent Analysis\](.*?)(?:\n\[|$)", response_text, re.DOTALL)
            if intent_match:
                intent_block = intent_match.group(1).strip()
                print(intent_block)

        # Print Decision Path (if present)
        decision_match = re.search(r"\[Decision Path\](.*?)(?:\n\[|$)", response_text, re.DOTALL)
        if decision_match:
            decision_block = decision_match.group(1).strip()
            print("\n[Decision Path]\n" + decision_block + "\n")
        # Extract and speak only the final AI answer
        match = re.search(r"\[Matrix AI Answer\](.*?)(?:\n\[|$)", response_text, re.DOTALL)
        if match:
            ai_answer = match.group(1).strip()
        else:
            parts = re.split(r"\[Intent Analysis\].*?\n", response_text, flags=re.DOTALL)
            ai_answer = parts[-1].strip() if len(parts) > 1 else response_text.strip()
        print("\n" + "="*50 + "\n")
        speak(ai_answer, use_mark=False)
        # Update memory with the AI answer
        conversation_history = update_memory(conversation_history, {"user": "Matrix", "content": ai_answer})
        return conversation_history


def main():
    opened_sites = []
    conversation_history = []  
    wait_for_wake_word()
    while True:
        query = listen()
        if not query:
            continue
        if "play music" in query:
            play_random_music()
        elif "exit" in query or "quit" in query:
            speak("Goodbye!", use_mark=False)
            break
        
        # Website opening logic only
        if query.lower().startswith("open "):
            site_name = query.lower().replace("open ", "").strip()
            match = next((site for site in SITES if site[0] == site_name), None)
            if match:
                speak(f"Opening, {site_name} sir", use_mark=False)
                proc = subprocess.Popen(["start", "", f"https://{match[1]}"], shell=True)
                opened_sites.append({"name": site_name, "process": proc})
            else:
                speak(f"Sorry, I can only open supported websites.", use_mark=False)
            continue

        elif "the time" in query or "what is the time" in query:
            import datetime
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute
            meridian = "AM" if hour < 12 else "PM"
            hour = hour if hour <= 12 else hour - 12
            formatted_time = f"{hour:02d}:{minute:02d} {meridian}"
            speak(f"The time is {formatted_time}", use_mark=False)
            #print(f"\n==> Matrix AI: The time is {formatted_time}\n")
        else:
            conversation_history.append({"user": "User", "content": query})
            process_query_with_langgraph(query, conversation_history)
            conversation_history.append({"user": "Matrix", "content": "[Matrix AI Answer]"})  # Optionally update with real answer

if __name__ == "__main__":
    main()
