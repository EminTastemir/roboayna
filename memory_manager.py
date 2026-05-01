import os
import json
from config import MEMORY_FILE

def load_memory() -> dict:
    """Hafıza dosyasını yükler, yoksa boş sözlük döner."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Hafıza yüklenirken hata: {e}")
            return {}
    return {}

def save_memory(data: dict):
    """Hafızayı dosyaya kaydeder."""
    # Dosyanın bulunduğu klasörü garanti altına al
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Hafıza kaydedilirken hata: {e}")

def set_memory(key: str, value: str):
    """Hafızaya yeni bir bilgi ekler veya günceller."""
    memory = load_memory()
    memory[key] = value
    save_memory(memory)
    return True

def get_memory(key: str) -> str:
    """Hafızadan bilgi çeker, yoksa None döner."""
    memory = load_memory()
    return memory.get(key)

def get_all_memory() -> str:
    """Chat engine için hafızayı okunabilir string formatında döner."""
    memory = load_memory()
    if not memory:
        return "Henüz hafızamda özel bir bilgi yok."
    
    info = []
    for k, v in memory.items():
        info.append(f"{k}: {v}")
    return ", ".join(info)
