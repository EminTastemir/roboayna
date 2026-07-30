import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
REMINDERS_FILE = os.path.join(DATA_DIR, "reminders.json")


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma2:2b"


TTS_VOICE = "tr-TR-AhmetNeural"
TTS_MUTE = False  


ASSISTANT_NAME = "RoboAyna"
CREATOR_NAME = "Robozen"
