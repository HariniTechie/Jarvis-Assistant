JARVIS AI Assistant
A powerful desktop voice assistant in Python, supporting both English and Telugu—with features like speech recognition, Wikipedia search, note-keeping, calculations, local app launching, weather reports, and integration with local LLMs using LM Studio.

-Table of Contents
Features
Architecture Overview
Setup & Installation
Configuration
Usage
Supported Commands & Examples
Extending the Assistant
Troubleshooting
License

-Features
Voice Control: Activate voice commands with a hotkey (Ctrl+Alt+J).
Bilingual: English and Telugu supported (auto-detected).
Text-to-Speech: Spoken and written responses; Telugu TTS when supported by OS.
Wikipedia Summaries: Get quick, concise explanations for any topic.
Calculator: Allows arithmetic and math queries.
Weather Info: Real-time weather fetching (requires API key).
Notes & Memory: Store and list custom reminders and notes.
App Launcher & Music: Launches Notepad and plays .mp3 files from your Music directory.
File Search: Finds files in your user directory.
Local AI Model Integration: Uses LM Studio for advanced question answering.

-Architecture Overview
![Architecture Diagram (Optional: insert one if you make itssing:** Language detection, translation (if needed), command dispatch, or LM Studio query.

Action: Fetches data, launches apps, stores notes, or triggers TTS for replies

Output: Immediate voice and console responses

-Setup & Installation
1. Clone the Project
bash
git clone https://github.com/HariniTechie/jarvis-ai-assistant.git
cd jarvis-ai-assistant

2. Create a Virtual Environment (Recommended)
bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

3. Install Python Dependencies
bash
pip install -r requirements.txt

# If you face issues with PyAudio on Windows:
pipwin install pyaudio
Sample requirements.txt
text
pyttsx3
keyboard
SpeechRecognition
wikipedia
requests
langdetect
deep-translator
pytz
pipwin
pyaudio
Configuration

-LM Studio:
Download and run LM Studio
Load your model (e.g. phi-2)
Set REST API: http://127.0.0.1:1234/v1/chat/completions

-Confirm the model name in your script:
text
MODEL_NAME = "phi-2"
Weather:
Get OpenWeatherMap API key
Set your API key as an environment variable:
bash
export OPENWEATHERMAP_API_KEY=your_actual_key   # Linux/macOS
set OPENWEATHERMAP_API_KEY=your_actual_key      # Windows CMD
Usage
Start LM Studio and load your LLM.

-Launch your assistant:
bash
python main.py
Interact by typing or pressing Ctrl+Alt+J to speak.
Type exit or use keyboard interrupt (Ctrl+C) to stop.

-Supported Commands & Examples :
Functionality	                        Example Command
Wikipedia	                            Tell me about Alan Turing.
Math	                                Calculate 23 times 19.
Weather	                                What is the weather in Hyderabad?
Notes (Save)	                        Remember that tomorrow is my mom's birthday.
Notes (List)	                        Show notes.
App Launch	                            Open Notepad.
File Search	                            Find file report.docx.
Music	                                Play music.
News	                                [If API integrated] Tell me the latest news.
General QA	                            Who is the current President of India?
Telugu input	                        [Speak or type in Telugu; assistant   auto-detects & replies in Telugu]
How It Works                            Input: You speak/type a command.
                                        

Language Detection: Auto-detects if Telugu or English (uses langdetect).

-Processing:
Translates to English if necessary (deep-translator).
Checks if the query is for Wikipedia, calculation, weather, notes, app-launch, or music.
If general QA, sends question to LM Studio for answer.

-Output:
Gets the answer.
If input was Telugu, translates result back.
Always speaks answer aloud and writes to terminal instantly (simultaneously).

-Extending the Assistant
Add more apps to launch:
Extend process_open_app() with more cases.

-Improve weather/news/integration:
Add your own API keys or advanced retrieval logic.

-Support more languages:
Expand language detection and add TTS voices.

-Change hotkeys or UI:
Modify the keyboard.add_hotkey() line.

-Troubleshooting
-LM Studio is not reachable:
Ensure LM Studio app is started and the API endpoint matches in your config
Model must be running in LM Studio

-Microphone or TTS issues:
Install PyAudio via pipwin if needed
Ensure your mic and speakers are working

-Telugu TTS doesn't work:
Your OS may not have Telugu voice installed.
Defaults to English voice as a fallback.

-Weather/news not working:
Make sure you’ve set the correct API key as an environment variable.

-License
MIT License

-Credits
LM Studio
SpeechRecognition
pyttsx3
wikipedia
deep-translator