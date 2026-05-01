import os
import asyncio
import edge_tts
from config import TTS_VOICE, TTS_MUTE
import pygame
import time

def speak_text(text: str):
    """
    Verilen metni Türkçe olarak seslendirir.
    Eğer metnin başında 'RoboAyna:' varsa bu kısmı okumadan atlar.
    """
    if TTS_MUTE:
        print(f"(SESSİZ MOD) RoboAyna: {text}")
        return

    # "RoboAyna:" önekini sesten temizleyelim
    text_to_speak = text.replace("RoboAyna:", "").strip()

    if not text_to_speak:
        return

    audio_file = "temp_response.mp3"

    # Async işlemi senkron şekilde çalıştırmak için event loop
    async def _generate_audio():
        communicate = edge_tts.Communicate(text_to_speak, TTS_VOICE)
        await communicate.save(audio_file)

    asyncio.run(_generate_audio())

    # Ses dosyasını oynatma (Pygame kullanıyoruz, Raspberry Pi'de de iyi çalışır)
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        pygame.mixer.quit()
    except Exception as e:
        print(f"Ses oynatma hatası: {e}")
    finally:
        # Geçici dosyayı sil
        if os.path.exists(audio_file):
            try:
                os.remove(audio_file)
            except:
                pass
