import os
import json
import requests
import datetime
import subprocess
import speech_recognition as sr
import pyttsx3
import keyboard
import wikipedia
from langdetect import detect               # <-- For language detection!
from deep_translator import GoogleTranslator
from requests.exceptions import RequestException

# === Configuration ===
LM_URL = "http://127.0.0.1:1234/v1/chat/completions"  # LM Studio API endpoint
MODEL_NAME = "phi-2"
TIMEOUT = 30
MEMORY_FILE = "memory.json"

# === Initialize Engines ===
engine = pyttsx3.init()
engine.setProperty('rate', 180)

# === Utility Functions ===
def speak_english(text):
    print(f"🤖 JARVIS (EN): {text}")
    try:
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"⚠️ TTS Error (EN): {e}")

def speak_telugu(text):
    print(f"🤖 JARVIS (TE): {text}")
    try:
        found_telugu = False
        for voice in engine.getProperty('voices'):
            if 'te' in str(voice.languages).lower() or 'telugu' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                found_telugu = True
                break
        if not found_telugu:
            print("⚠️ Telugu TTS not found. Using English.")
            speak_english(text)
            return
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"⚠️ Telugu TTS Error: {e}")
        speak_english("[Telugu unavailable] " + text)

def speak(text, lang="en"):
    if lang == "te":
        speak_telugu(text)
    else:
        speak_english(text)

def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening... (say 'cancel' to stop)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
        text = recognizer.recognize_google(audio)
        print(f"👤 YOU: {text}")
        return text
    except sr.WaitTimeoutError:
        speak("I didn't hear anything. Please try again.")
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        speak(f"Speech service error: {e}")
    except Exception as e:
        speak(f"Microphone error: {e}")
    return ""

# === Bilingual Helpers ===
def detect_language(text):
    try:
        return detect(text)
    except Exception:
        return "en"

def translate_text(text, dest='en'):
    try:
        return GoogleTranslator(source='auto', target=dest).translate(text)
    except Exception as e:
        print(f"⚠️ Translation Error: {e}")
        return text

# === AI Query ===
def query_ai(prompt):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are Jarvis, a concise, helpful assistant. Respond only with necessary details."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 300
    }
    try:
        response = requests.post(LM_URL, json=payload, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except RequestException as e:
        return f"⚠️ API Error: {e}"
    except Exception as e:
        return f"⚠️ Unexpected Error: {e}"

# === Utility Features ===
def process_calculator(prompt):
    try:
        # Safe evaluation only for limited inputs!
        result = eval(prompt, {"__builtins__": {}})
        return f"The result is {result}."
    except Exception:
        return "Sorry, I couldn't calculate that."

def process_wikipedia(prompt):
    try:
        summary = wikipedia.summary(prompt, sentences=2)
        return summary
    except Exception as e:
        return f"Error fetching Wikipedia info: {e}"

def process_weather(prompt):
    API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')  # Set key as env var!
    if not API_KEY:
        return "Weather API key not set!"
    try:
        if 'in' in prompt:
            city = prompt.split('in')[-1].strip()
        else:
            city = prompt.strip()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()
        if data.get("main"):
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The current temperature in {city} is {temp}°C with {description}."
        else:
            return "I could not fetch weather data."
    except Exception as e:
        return f"Weather error: {e}"

def process_open_app(prompt):
    if "notepad" in prompt.lower():
        subprocess.Popen("notepad.exe")
        return "Opening Notepad."
    else:
        return "App not recognized."

def process_play_music(prompt):
    music_folder = os.path.expanduser("~/Music")
    try:
        files = os.listdir(music_folder)
        for file in files:
            if file.endswith(".mp3"):
                os.startfile(os.path.join(music_folder, file))
                return f"Playing {file}."
        return "No music file found."
    except Exception as e:
        return f"Music error: {e}"

def process_file_search(prompt):
    search_term = prompt.split("find file")[-1].strip()
    found_files = []
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for file in files:
            if search_term.lower() in file.lower():
                found_files.append(os.path.join(root, file))
        if len(found_files) >= 5:
            break
    if found_files:
        return "\n".join(found_files)
    else:
        return "No matching files found."

def process_custom_memory(prompt, save=True):
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w') as f:
            json.dump({}, f)
    with open(MEMORY_FILE, 'r') as f:
        memory = json.load(f)
    if save:
        key = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memory[key] = prompt
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory, f, indent=4)
        return "I've stored that information."
    else:
        notes = "\n".join([f"{k}: {v}" for k, v in memory.items()])
        return f"Stored notes:\n{notes}" if notes else "No memories stored yet."

def dispatch_command(prompt, lang):
    lower_prompt = prompt.lower()
    if "calculate" in lower_prompt or any(char.isdigit() for char in lower_prompt):
        return process_calculator(prompt)
    elif "wikipedia" in lower_prompt or "tell me about" in lower_prompt:
        search_query = lower_prompt.replace("wikipedia", "").replace("tell me about", "").strip()
        return process_wikipedia(search_query)
    elif "weather" in lower_prompt:
        return process_weather(prompt)
    elif "open" in lower_prompt:
        return process_open_app(prompt)
    elif "play music" in lower_prompt:
        return process_play_music(prompt)
    elif "find file" in lower_prompt:
        return process_file_search(prompt)
    elif "remember that" in lower_prompt or "store note" in lower_prompt:
        return process_custom_memory(prompt, save=True)
    elif "show notes" in lower_prompt or "memory" in lower_prompt:
        return process_custom_memory(prompt, save=False)
    else:
        return query_ai(prompt)

def process_voice_command():
    spoken_text = listen()
    if not spoken_text or spoken_text.lower() == "cancel":
        return
    detected_lang = detect_language(spoken_text)
    print(f"Detected language: {detected_lang}")
    if detected_lang == "te":
        prompt_en = translate_text(spoken_text, dest="en")
        print(f"Translated to English: {prompt_en}")
    else:
        prompt_en = spoken_text
    response = dispatch_command(prompt_en, detected_lang)
    if detected_lang == "te":
        response = translate_text(response, dest="te")
    speak(response, lang=detected_lang)

def main():
    print("=== JARVIS AI Assistant ===")
    print("Voice Hotkey: Ctrl + Alt + J")
    print("Type 'exit' to quit\n")

    try:
        requests.get("http://127.0.0.1:1234/health", timeout=5)
    except Exception:
        speak("LM Studio is not reachable. Please make sure it is running.")
        return

    speak("Jarvis is online. How can I help you?", lang="en")
    keyboard.add_hotkey('ctrl+alt+j', process_voice_command)

    while True:
        try:
            text_input = input("Type command or press hotkey: ").strip()
            if text_input.lower() == "exit":
                break
            if text_input:
                detected_lang = detect_language(text_input)
                if detected_lang == "te":
                    prompt_en = translate_text(text_input, dest="en")
                else:
                    prompt_en = text_input
                response = dispatch_command(prompt_en, detected_lang)
                if detected_lang == "te":
                    response = translate_text(response, dest="te")
                speak(response, lang=detected_lang)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠️ System Error: {e}")

    speak("Shutting down. Goodbye!", lang="en")
    print("\nJARVIS session ended.")

if __name__ == "__main__":
    main()
