import re
import requests
import datetime
from config import OLLAMA_URL, MODEL_NAME, ASSISTANT_NAME, CREATOR_NAME
from memory_manager import get_all_memory

# RoboAyna'nın Sistem Prompt'u (Kişiliği)
SYSTEM_PROMPT = f"""Rol: Sen {ASSISTANT_NAME}.
Yaratıcı: {CREATOR_NAME} takımı.
Görev: Kullanıcının gündelik işlerine yardımcı olan yerel bir akıllı ayna.
Dil: Sadece Türkçe.

Kurallar:
- Kendinden bahsederken her zaman birinci tekil şahıs kullan (Örn: "Ben RoboAyna").
- Çok kısa, net ve samimi cevaplar ver.
- Asla emoji kullanma, sadece saf metin üret.
"""

def generate_chat_response(user_input: str) -> str:
    """
    Kullanıcı ile doğal sohbet için Ollama'dan cevap üretir.
    Hafızadaki bilgileri de prompt'a ekler.
    """
    memory_context = get_all_memory()
    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    
    chat_url = OLLAMA_URL
    if chat_url.endswith("/api/generate"):
        chat_url = chat_url.replace("/api/generate", "/api/chat")
        
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nŞu Anki Sistem Zamanı: {current_time}\n\nHafıza kayıtları:\n{memory_context}"},
            {"role": "user", "content": user_input}
        ],
        "stream": False,
        "options": {
            "num_predict": 100,
            "temperature": 0.4
        }
    }
    
    try:
        response = requests.post(chat_url, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
        text = result.get("message", {}).get("content", "").strip()
        
        # Olası emojileri ve istenmeyen sembolleri kesin olarak filtrele
        text = re.sub(r'[^\w\s.,!?\'"()\-:;]', '', text)
        return text.strip()
    except Exception as e:
        print(f"Chat generation hatası: {e}")
        return "Şu anda bağlantımda bir sorun var, daha sonra tekrar dener misin?"
