import json
from flask import Flask, request, jsonify
from abuse_filter import check_abuse, get_safe_response
from intent_parser import parse_intent
from chat_engine import generate_chat_response
from tts_engine import speak_text
from memory_manager import set_memory
from reminder_manager import add_reminder

# Şimdilik stub servisleri import etmeye gerek yok, stub iskeletlerini çağırıyoruz varsayalım.
# İleriki adımlarda spotify_service ve weather_service eklendiğinde buraya dahil edeceğiz.
import spotify_service
import weather_service

app = Flask(__name__)

def process_user_input(text: str) -> str:
    """Ana işlem akışı: Filtre -> Intent -> Aksiyon veya Chat -> TTS -> Sonuç"""
    print(f"Kullanıcı: {text}")
    
    # 1. Küfür/Hakaret Kontrolü
    if check_abuse(text):
        safe_reply = get_safe_response()
        speak_text(safe_reply)
        return safe_reply
        
    # 2. Intent Analizi
    print("[Sistem] Niyet analizi yapılıyor...")
    intent_result = parse_intent(text)
    intent = intent_result.get("intent", "unknown")
    reply = intent_result.get("reply", "")
    data = intent_result.get("data", {})
    
    print(f"[Sistem] Bulunan Niyet: {intent}")
    
    final_response = ""
    
    # 3. Aksiyon Akışı
    if intent == "memory_save":
        key = data.get("memory_key")
        val = data.get("memory_value")
        if key and val:
            set_memory(key, val)
            final_response = reply if reply else "Bunu hafızama kaydettim."
        else:
            final_response = "Neyi kaydetmem gerektiğini tam anlayamadım."
            
    elif intent == "create_reminder":
        time_str = data.get("time", "Bilinmeyen Zaman")
        reminder_text = data.get("text", "Hatırlatıcı")
        add_reminder(time_str, reminder_text)
        final_response = reply if reply else f"{time_str} için hatırlatıcı kurdum."
        
    elif intent == "spotify_play":
        song = data.get("song", "")
        spotify_service.play_music(song)
        final_response = reply if reply else "Müziği başlatıyorum."
        
    elif intent == "spotify_pause":
        spotify_service.pause_music()
        final_response = reply if reply else "Müziği durdurdum."
        
    elif intent == "weather":
        # Şimdilik hava durumu iskeletini çağır
        final_response = weather_service.get_weather()
        
    elif intent in ["chat", "unknown"]:
        # Sadece sohbet veya anlaşılamayan durumda doğal dil motoruna git
        print("[Sistem] Doğal sohbete yönlendiriliyor...")
        final_response = generate_chat_response(text)
    
    # 4. Sesli Yanıt (Eğer bir cevap üretilmişse)
    if final_response:
        print(f"RoboAyna: {final_response}")
        speak_text(final_response)
        
    return final_response

# MagicMirror'dan gelen istekleri karşılayacak API Endpoint'i
@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "text parametresi eksik"}), 400
        
    user_text = data["text"]
    response_text = process_user_input(user_text)
    
    return jsonify({
        "status": "success",
        "response": response_text
    })

if __name__ == "__main__":
    print("RoboAyna Çekirdek Servisi Başlatılıyor...")
    # Sadece Windows/Dev modunda terminal testi için basit bir döngü
    # Gerçek kullanımda Flask arkada çalışacak.
    # Flask sunucusunu başlat:
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
