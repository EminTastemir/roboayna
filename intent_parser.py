import requests
import json
from config import OLLAMA_URL, MODEL_NAME

import requests
import json
from config import OLLAMA_URL, MODEL_NAME

INTENT_PROMPT = """Sen bir komut analiz motorusun (intent parser).
Görevin kullanıcının söylediği cümleyi analiz edip SADECE GEÇERLİ BİR JSON döndürmektir.
Asla JSON dışında metin, açıklama, markdown veya kod bloğu yazma.

Intent türleri:
1. chat
2. create_reminder
3. memory_save
4. spotify_play
5. spotify_pause
6. weather
7. unknown

Döndürmen gereken JSON formatı:
{
  "intent": "bulunan_intent",
  "reply": "Kullanıcıya verilecek kısa onay mesajı",
  "data": {
    "text": "Hatırlatıcı metni",
    "time": "Zaman bilgisi",
    "song": "Şarkı adı",
    "artist": "Sanatçı adı",
    "memory_key": "Kaydedilecek bilginin konusu",
    "memory_value": "Kaydedilecek değer"
  }
}

Kurallar:
- Genel sohbet, kimlik soruları, günlük konuşma = "chat"
- Hatırlatıcı/alarm/uyandırma = "create_reminder"
- "Benim adım X", "bunu hatırla", "unutma" = "memory_save"
- Müzik açma = "spotify_play"
- Müziği durdurma = "spotify_pause"
- Hava durumu sorma = "weather"
- Emin değilsen = "unknown"

Önemli:
- reply kısa ve Türkçe olsun.
- Gerekli olmayan alanları boş string bırak.
- Sadece JSON döndür.

Kullanıcı girdisi:
{user_input}
"""


def _build_chat_url(url: str) -> str:
    url = url.rstrip("/")

    if url.endswith("/api/chat"):
        return url

    if url.endswith("/api/generate"):
        return url[:-len("/api/generate")] + "/api/chat"

    if "/api/" not in url:
        return url + "/api/chat"

    return url


def _clean_json_text(text: str) -> str:
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1).strip()

    if text.startswith("```"):
        text = text.replace("```", "", 1).strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


def parse_intent(user_input: str) -> dict:
    """
    Kullanıcı girdisini Ollama üzerinden analiz eder ve bir sözlük (JSON) döndürür.
    """
    chat_url = _build_chat_url(OLLAMA_URL)
    prompt = INTENT_PROMPT.replace("{user_input}", user_input)

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        "stream": False,
        "format": "json",
        "keep_alive": "10m",
        "options": {
            "temperature": 0.1,
            "num_predict": 150
        }
    }

    try:
        response = requests.post(chat_url, json=payload, timeout=20)
        response.raise_for_status()

        result = response.json()
        response_text = result.get("message", {}).get("content", "{}")
        response_text = _clean_json_text(response_text)

        intent_data = json.loads(response_text)

        if "intent" not in intent_data:
            raise ValueError("intent alanı eksik")

        if "reply" not in intent_data:
            intent_data["reply"] = ""

        if "data" not in intent_data or not isinstance(intent_data["data"], dict):
            intent_data["data"] = {}

        default_data = {
            "text": "",
            "time": "",
            "song": "",
            "artist": "",
            "memory_key": "",
            "memory_value": ""
        }

        for key, value in default_data.items():
            intent_data["data"].setdefault(key, value)

        return intent_data

    except Exception as e:
        print(f"Intent parsing hatası: {e}")
        return {
            "intent": "unknown",
            "reply": "Sistemsel bir hata oluştu.",
            "data": {
                "text": "",
                "time": "",
                "song": "",
                "artist": "",
                "memory_key": "",
                "memory_value": ""
            }
        }