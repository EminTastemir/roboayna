import os

# Proje Kök Dizini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Veri Dosyaları
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
REMINDERS_FILE = os.path.join(DATA_DIR, "reminders.json")

# Ollama Ayarları
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma2:2b"

# TTS Ayarları
TTS_VOICE = "tr-TR-AhmetNeural"
TTS_MUTE = False  # Geliştirme sırasında True yaparak sessiz moda geçilebilir

# Asistan Karakter Bilgileri
ASSISTANT_NAME = "RoboAyna"
CREATOR_NAME = "Robozen"
