import random

def get_weather() -> str:
    """
    Geçerli hava durumu bilgisini döner.
    Şimdilik rastgele bir durum döner (stub).
    İleride OpenWeatherMap veya AccuWeather API'si eklenecek.
    """
    
    durumlar = [
        "Bugün hava güneşli ve 25 derece görünüyor.",
        "Şu an hava hafif bulutlu ve 20 derece.",
        "Dışarısı yağmurlu, çıkarken şemsiyeni almayı unutma. Sıcaklık 15 derece."
    ]
    
    secilen_durum = random.choice(durumlar)
    print(f"[Hava Durumu Modülü] Sorgulandı: {secilen_durum}")
    return secilen_durum
