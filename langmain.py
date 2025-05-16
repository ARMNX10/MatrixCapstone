import os
import time
import random
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from langraph_app import build_graph, AgentState  # Reuse your LangGraph workflow
import subprocess
from interrupter import listen_for_interrupt, was_interrupted
import datetime

# --- Config ---
load_dotenv()
MUSIC_DIR = os.getenv("MUSIC_DIR", r"R:\Music")

WAKE_WORDS = ["activate", "wake up", "good morning", "good afternoon", "good evening"]
# SITES = [
#     ["youtube", "youtube.com"],
#     ["wikipedia", "wikipedia.org"],
#     ["google", "google.com"],
#     ["whatsapp", "web.whatsapp.com"],
#     ["gmail", "mail.google.com"],
#     ["reddit", "reddit.com"],
#     ["twitter", "twitter.com"],
#     ["facebook", "facebook.com"],
#     ["instagram", "instagram.com"],
#     ["amazon", "amazon.com"],
#     ["flipkart", "flipkart.com"],
#     ["stackoverflow", "stackoverflow.com"],
#     ["github", "github.com"],
#     ["vtop", "vtop.vit.ac.in"],
#     ["vit website", "vtop.vit.ac.in"],
#     ["netflix", "netflix.com"],
#     ["prime video", "primevideo.com"],
#     ["linkedin", "linkedin.com"],
#     ["spotify", "spotify.com"],
#     ["quora", "quora.com"],
#     ["zoom", "zoom.us"],
#     ["discord", "discord.com"],
#     ["drive", "drive.google.com"],
#     ["maps", "maps.google.com"],
#     ["news", "news.google.com"],
# ]

# --- Voice Engine ---
import pyttsx3
engine = pyttsx3.init()
# Registry tokens for Microsoft voices
# Available voices (pyttsx3):
# - David: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0
# - Mark:  HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enUS_MarkM
# - Zira:  HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0
VOICE_DAVID = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0'
VOICE_MARK = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSTTS_V110_enUS_MarkM'
VOICE_MARK = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSTTS_V110_enUS_MarkM'
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
    recognizer.energy_threshold = 150  # Lower if needed for your mic/environment
    recognizer.pause_threshold = 1.5   
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 150  # Lower if needed for your mic/environment
    recognizer.pause_threshold = 1.5   
    recognizer.dynamic_energy_threshold = True
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        print("Listening... (speak clearly, pause briefly when done)")
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return ""
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        print("Listening... (speak clearly, pause briefly when done)")
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return ""
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
from langmem import langmem
from langmem import langmem
from prompts import chat_prompt


def update_memory(conversation_history, new_message):
    conversation_history.append(new_message)
    return conversation_history[-MEMORY_LENGTH:]

# Conversational memory threading
# Track last factual context and inject it for ambiguous follow-ups
last_factual_context = {'topic': None, 'entities': None, 'answer': None}

def process_query_with_langgraph(query):
    from langraph_app import build_graph
    import json, re
    global last_factual_context
    graph = build_graph().compile()
    # System prompt for conversational AI
    system_prompt = (
        "You are Matrix, an AI assistant helping users with queries. "
        "Be concise, clear, and avoid unnecessary technical jargon. "
        "Keep your responses short, easy to read, and conversational. DO NOT GIVE LONG ANSWER WHICH WOULD TAKE LONGER TO READ ALOUD.\n"
        "If the user asks to change the screen brightness, respond ONLY with the exact command in the form: 'change brightness to {number}' (e.g., 'change brightness to 70'). DO NOT say anything else. DO NOT add explanations, confirmations, or questions. Your response MUST be only the command.\n"
        "If the user asks to change the system volume, respond ONLY with the exact command in the form: 'change system volume to {number}' (e.g., 'change system volume to 35'). DO NOT say anything else. DO NOT add explanations, confirmations, or questions. Your response MUST be only the command.\n"
    )
    # Add user query to LangMem
    langmem.add({"type": "user_query", "content": query})
    memory_context = langmem.get_context(query, top_k=5)

    # --- Contextual follow-up detection ---
    ambiguous_phrases = [
        "yes", "sure", "okay", "ok", "please share", "tell me more", "go on", "continue", "elaborate", "more info", "more details", "show me", "share", "what about that", "what about it", "can you explain", "explain more", "give details"
    ]
    is_ambiguous = any(phrase in query.lower() for phrase in ambiguous_phrases) and len(query.split()) <= 6
    # Only inject context if ambiguous and we have a last factual context
    context_injected = False
    if is_ambiguous and last_factual_context['answer']:
        # Prepend last factual context to query
        context_str = "[PREVIOUS CONTEXT] "
        if last_factual_context['entities']:
            context_str += f"Entities: {last_factual_context['entities']}. "
        if last_factual_context['topic']:
            context_str += f"Topic: {last_factual_context['topic']}. "
        context_str += f"Previous Answer: {last_factual_context['answer']}\n"
        query_for_prompt = context_str + query
        context_injected = True
    else:
        query_for_prompt = query

    input_state = {
        "messages": [{"role": "user", "content": f"{memory_context}\nUser: {query_for_prompt}"}],
        "config": {},
        "memory_context": memory_context
    }
    result = graph.invoke(input_state)
    result = graph.invoke(input_state)
    response_text = result.get("response", "")

    # --- Parse blocks from response_text ---
    intent_block = re.search(r"\[Intent Analysis\](.*?)(?:\n\[|$)", response_text, re.DOTALL)
    web_search_block = re.search(r"\[Web Search Synthesis\](.*?)(?:\n\[|$)", response_text, re.DOTALL)
    ai_answer_block = re.search(r"\[Matrix AI Answer\](.*?)(?:\n\[|$)", response_text, re.DOTALL)

    # 1. Print intent analysis immediately
    if intent_block:
        try:
            intent_json = json.loads(intent_block.group(1))
            print(json.dumps(intent_json, indent=2, ensure_ascii=False))
        except Exception:
            print("[Intent Analysis]", intent_block.group(1).strip())
    # 2. Print web search tool logs if web search was needed (always before answer)
    decision = result.get("decision_result") or {}
    # Only print web search logs if decision path is 'web_search'
    if decision.get("path") == "web_search":
        print("[Matrix] Calling web search tool...")
        print("[Matrix] Synthesizing results from web search tool...")
    # 3. Print/speak the final synthesized answer (always after search logs)
    if ai_answer_block:
        ai_answer = ai_answer_block.group(1).strip()
        print("\n" + "="*50 + "\n")
        speak(ai_answer, use_mark=False)
        # --- AI-driven volume control ---
        import re
        # Match more phrasings for volume
        vol_cmd = re.search(r"(?:set|change|adjust|setting|i've set|i have set|i am setting|i'm setting)[^\d]{0,20}volume[^\d]{0,10}to (\d{1,3})", ai_answer.lower())
        if not vol_cmd:
            vol_match = re.match(r"(set|change|adjust) volume to (\d{1,3})", query.lower())
        if vol_match:
            try:
                volume = int(vol_match.group(2))
                volume = max(0, min(100, volume))
                # Try using pycaw (if available)
                try:
                    from ctypes import cast, POINTER
                    from comtypes import CLSCTX_ALL
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume_obj = cast(interface, POINTER(IAudioEndpointVolume))
                    # pycaw uses scalar 0.0-1.0
                    volume_obj.SetMasterVolumeLevelScalar(volume/100.0, None)
                    speak(f"System volume set to {volume}.", use_mark=False)
                except Exception:
                    # Fallback: use PowerShell
                    import subprocess
                    try:
                        for _ in range(50):
                            subprocess.run(["powershell", "(new-object -com wscript.shell).SendKeys([char]175)"], shell=True)
                        # Above is a hack; better to use nircmd if available
                        # subprocess.run(["nircmd.exe", "setsysvolume", str(int(volume*65535/100))])
                        speak(f"System volume set to {volume} (fallback method).", use_mark=False)
                    except Exception as e:
                        speak(f"Failed to set volume: {e}", use_mark=False)
            except Exception as e:
                speak(f"Could not parse volume command: {e}", use_mark=False)
            return  # SKIP AI/LLM call
        # --- AI-driven brightness control ---
        import re
        # Match more phrasings for brightness (similar to volume)
        bright_cmd = re.search(r"(?:set|change|adjust|setting|i've set|i have set|i am setting|i'm setting)[^\d]{0,20}brightness[^\d]{0,10}to (\d{1,3})", ai_answer.lower()) if ai_answer else None
        if not bright_cmd:
            bright_cmd = re.search(r"(?:set|change|adjust|setting|i've set|i have set|i am setting|i'm setting)[^\d]{0,20}brightness[^\d]{0,10}to (\d{1,3})", query.lower())
        if not bright_cmd:
            bright_cmd = re.match(r"(set|change|adjust) brightness to (\d{1,3})", query.lower())
        # Handle incomplete brightness commands (e.g., 'set brightness to')
        incomplete_bright = re.search(r"(?:set|change|adjust|setting|i've set|i have set|i am setting|i'm setting)[^\d]{0,20}brightness[^\d]{0,10}to\s*$", ai_answer.lower()) if ai_answer else None
        if not incomplete_bright:
            incomplete_bright = re.search(r"(?:set|change|adjust|setting|i've set|i have set|i am setting|i'm setting)[^\d]{0,20}brightness[^\d]{0,10}to\s*$", query.lower())
        if not incomplete_bright:
            incomplete_bright = re.match(r"(set|change|adjust) brightness to\s*$", query.lower())
        if incomplete_bright:
            speak("To set the brightness, I need a specific level. What brightness level do you want?", use_mark=False)
            return  # SKIP AI/LLM call
        if bright_cmd:
            try:
                # Try to extract the number from the correct group
                if bright_cmd.lastindex:
                    brightness = int(bright_cmd.group(bright_cmd.lastindex))
                else:
                    brightness = int(bright_cmd.group(2))
                brightness = max(0, min(100, brightness))
                try:
                    import wmi
                    wmi_obj = wmi.WMI(namespace='wmi')
                    methods = wmi_obj.WmiMonitorBrightnessMethods()[0]
                    methods.WmiSetBrightness(brightness, 0)
                    speak(f"Screen brightness set to {brightness}.", use_mark=False)
                except Exception:
                    import subprocess
                    try:
                        subprocess.run(["powershell", f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness})"], shell=True)
                        speak(f"Screen brightness set to {brightness} (fallback method).", use_mark=False)
                    except Exception as e:
                        speak(f"Failed to set brightness: {e}", use_mark=False)
            except Exception as e:
                speak(f"Could not parse brightness command: {e}", use_mark=False)
            return  # SKIP AI/LLM call
        # End brightness control block
        
    # Save intent and answer to LangMem robustly
    if intent_block:
        try:
            intent_json = json.loads(intent_block.group(1))
            langmem.add({"type": "intent", "content": json.dumps(intent_json, ensure_ascii=False)})
        except Exception:
            langmem.add({"type": "intent", "content": intent_block.group(1).strip()})
    if 'ai_answer' in locals() and ai_answer:
        langmem.add({"type": "ai_answer", "content": ai_answer})
    # --- Update last factual context if this was a factual/web search query ---
    if intent_block:
        try:
            intent_json = json.loads(intent_block.group(1))
            if (decision.get("path") == "web_search") or (intent_json.get("requires_web_search") is True):
                last_factual_context['topic'] = ', '.join(intent_json.get('topics', [])) if intent_json.get('topics') else None
                last_factual_context['entities'] = ', '.join(intent_json.get('entities', [])) if intent_json.get('entities') else None
                if 'ai_answer' in locals() and ai_answer:
                    last_factual_context['answer'] = ai_answer
        except Exception:
            pass
    # Save/update game or task state if needed (future: add structured state here)
    if context_injected:
        print("[Matrix] (Injected previous context for ambiguous follow-up)")
    return

def main():
    opened_sites = []
    #wait_for_wake_word()
    while True:
        query = listen()
        if not query:
            continue
        # Volume control: 'change volume to {number}'
        import re
        vol_match = re.match(r"(set|change|adjust) volume to (\d{1,3})", query.lower())
        if vol_match:
            try:
                volume = int(vol_match.group(2))
                volume = max(0, min(100, volume))
                # Try using pycaw (if available)
                try:
                    from ctypes import cast, POINTER
                    from comtypes import CLSCTX_ALL
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume_obj = cast(interface, POINTER(IAudioEndpointVolume))
                    # pycaw uses scalar 0.0-1.0
                    volume_obj.SetMasterVolumeLevelScalar(volume/100.0, None)
                    speak(f"System volume set to {volume}.", use_mark=False)
                except Exception:
                    # Fallback: use PowerShell
                    import subprocess
                    try:
                        # Fallback: try to increase volume step by step (simulate key press)
                        for _ in range(50):
                            subprocess.run(["powershell", "(new-object -com wscript.shell).SendKeys([char]175)"], shell=True)
                        # For best results, install nircmd and uncomment below:
                        # subprocess.run(["nircmd.exe", "setsysvolume", str(int(volume*65535/100))])
                        speak(f"System volume set to {volume} (fallback method).", use_mark=False)
                    except Exception as e:
                        speak(f"Failed to set volume: {e}", use_mark=False)
            except Exception as e:
                speak(f"Could not parse volume command: {e}", use_mark=False)
            continue
        if "play music" in query:
            play_random_music()
            continue
        elif "exit" in query or "quit" in query or "stop matrix" in query:
            speak("Goodbye!", use_mark=False)
            break
        if query.lower().startswith("open "):
            site_name = query.lower().replace("open ", "").strip()
            speak(f"Searching for {site_name} website...", use_mark=False)
            try:
                from web_search_api import call_serper_api
                search_query = f"official website for {site_name}"
                search_results = call_serper_api(search_query)
                import re
                url_match = re.search(r'(https?://[^\s]+)', search_results)
                if url_match:
                    url = url_match.group(1)
                    speak(f"Opening {site_name}...", use_mark=False)
                    import webbrowser
                    webbrowser.open(url)
                    opened_sites.append(url)
                else:
                    speak(f"Sorry, I couldn't find a valid website for {site_name}.", use_mark=False)
            except Exception as e:
                speak(f"An error occurred while searching for {site_name}: {e}", use_mark=False)
        elif "time" in query:
            now = datetime.datetime.now()
            hour, minute = now.hour, now.minute
            meridian = "AM" if hour < 12 else "PM"
            hour = hour if hour <= 12 else hour - 12
            formatted_time = f"{hour:02d}:{minute:02d} {meridian}"
            speak(f"The time is {formatted_time}", use_mark=False)
        else:
            process_query_with_langgraph(query)

if __name__ == "__main__":
    main()
