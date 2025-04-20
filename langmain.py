import os
import sys
import time
import random
import webbrowser
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from langraph_app import build_graph, AgentState  # Reuse your LangGraph workflow
import subprocess
import shutil

# --- Config ---
load_dotenv()
MUSIC_DIR = os.getenv("MUSIC_DIR", "music")  # Set your music folder path here
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
engine = pyttsx3.init()
def speak(text):
    print(f"\n==> Matrix AI: {text}")
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
                    speak("Matrix activated. How can I help you?")
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

def fake_stream_and_speak(text, delay=0.12):
    words = re.findall(r'\S+|\s+', text)  # Preserve spaces for natural printing
    buffer = ""
    for word in words:
        print(word, end="", flush=True)
        buffer += word
        if word.strip():  # Only speak actual words
            engine.say(word)
            engine.runAndWait()
        time.sleep(delay)
    print("\n" + "="*50 + "\n")

from prompts import chat_prompt


def process_query_with_langgraph(query):
    graph = build_graph().compile()
    # System prompt for conversational AI
    system_prompt = (
        "You are Matrix, a friendly, helpful conversational AI assistant. "
        "Be concise, clear, and avoid unnecessary technical jargon. "
        "Keep your responses short, easy to read, and conversational.\n"
    )
    # Use prompts.py's chat_prompt for the user query
    user_prompt = chat_prompt(query)
    full_prompt = f"{system_prompt}\n{user_prompt}"
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
        # Extract short summary (first paragraph or 2 sentences)
        import re
        paras = re.split(r'\n\s*\n|(?<=[.!?])\s+', response_text.strip())
        short_answer = paras[0].strip() if paras else response_text.strip()
        fake_stream_and_speak(short_answer)
        # Offer to provide full context
        speak("Do you want me to tell you the whole context?")
        print("\n[Matrix AI] Do you want the full context? Say 'yes' to hear more.")
        # If user says yes, provide the rest
        # This requires main loop logic to listen for 'yes' and then speak the rest of the response
        # (Implementation stub: actual listening for 'yes' would be in main loop)
        # To be implemented: if user says yes, speak '\n'.join(paras[1:])

def main():
    opened_sites = []  # Track opened sites and their processes
    #wait_for_wake_word()
    while True:
        query = listen()
        if not query:
            continue
        if "play music" in query:
            play_random_music()
        elif "exit" in query or "quit" in query:
            speak("Goodbye!")
            break
        
        # Website opening logic only
        if query.lower().startswith("open "):
            site_name = query.lower().replace("open ", "").strip()
            match = next((site for site in SITES if site[0] == site_name), None)
            if match:
                speak(f"Opening, {site_name} sir")
                proc = subprocess.Popen(["start", "", f"https://{match[1]}"], shell=True)
                opened_sites.append({"name": site_name, "process": proc})
            else:
                speak(f"Sorry, I can only open supported websites.")
            continue

        elif "the time" in query or "what is the time" in query:
            import datetime
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute
            meridian = "AM" if hour < 12 else "PM"
            hour = hour if hour <= 12 else hour - 12
            formatted_time = f"{hour:02d}:{minute:02d} {meridian}"
            speak(f"The time is {formatted_time}")
            print(f"\n==> Matrix AI: The time is {formatted_time}\n")
        else:
            process_query_with_langgraph(query)

if __name__ == "__main__":
    main()
